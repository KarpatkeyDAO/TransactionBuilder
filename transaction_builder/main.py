"""Main module."""
from typing import Dict, List, Tuple, Union

import os
from gnosis.safe.multi_send import MultiSend, MultiSendOperation, MultiSendTx
from gnosis.eth import EthereumClient

from transaction_builder.util.enums import Chain
from transaction_builder.util.function_data import ContractFunction
from transaction_builder.util.roles_class import RolesMod
from transaction_builder.util.functions import get_node

MULTISEND_CALL_ONLY = '0x40A2aCCbd92BCA938b02010E17A5b8929b49130D'
multisends = {
    'ethereum': '0x998739BFdAAdde7C933B942a68053933098f9EDa',
    'gnosisChain': '0xA238CBeb142c10Ef7Ad8442C6D1f9E89e07e7761'
}


def make_onesend(tx: Dict) -> ContractFunction:
    """returns a ContractFunction class from transaction dict

    Args:
        tx (Dict): Dictionary of transactions

    Returns:
        ContractFunction: returns cf object
    """
    cf = ContractFunction(
        tx["blockchain"],
        tx["function_args"],
        tx["function_name"],
        tx["contract_address"],
        tx["contract_abi"],
        tx['operation'],
        tx['value']
    )
    return cf


def make_multisend(txs: List[Dict], blockchain: str, multisend: str) -> str:
    """create the data for a multisend tx

    Args:
        txs (List[Dict]): list of transaction dictionaries
        blockchain (str): name of the blockchain to execute
        multisend (str): address of the multisend contract

    Returns:
        str: hexstring of the data
    """
    web3 = get_node(blockchain).manager.provider.__dict__['endpoint_uri']
    txs = [make_onesend(tx) for tx in txs]
    transactions = [
        MultiSendTx(
            MultiSendOperation.CALL,
            tx.contract_address,
            tx.value,
            tx.data_input()
        ) for tx in txs
    ]
    data = MultiSend(
        ethereum_client=EthereumClient(web3),
        address=multisend
    ).build_tx_data(transactions)
    return data


def multi_or_one(txs: List[Dict]) -> Tuple[int, str, str, str]:
    """Checks if tx list needs multisend or not

    Args:
        txs (List[Dict]): list with transactions dictionaries

    Returns:
        Tuple[int, str, str, str]: necessary variables for making transaction
    """
    blockchain = txs[0]["blockchain"]
    if len(txs) > 1:
        contract_address = multisends.get(blockchain, MULTISEND_CALL_ONLY)
        data = make_multisend(txs, blockchain, contract_address)
        operation = MultiSendOperation.DELEGATE_CALL.value
    elif len(txs) == 1:
        tx = make_onesend(txs[0])
        contract_address = tx.contract_address
        data = tx.data_input()
        if tx.operation == 0:
            operation = MultiSendOperation.CALL.value
        else:
            operation = MultiSendOperation.DELEGATE_CALL.value
    else:
        print('no transaction found')
    return operation, contract_address, data, blockchain


def test_it(
    txs: List[Dict],
    role: int,
    account: str,
    roles_mod_address: str
    ) -> bool:
    """Test the transaction with static call

    Args:
        txs (List[Dict]): list of transaction dictionaries
        role (int): role that wants to execute
        account (str): account that wants to execute
        roles_mod_address (str): address to call execTransactionWithRole

    Returns:
        bool: True or False
    """
    operation, contract_address, data, blockchain = multi_or_one(txs)
    roles_mod = RolesMod(
        blockchain,
        role,
        contract_address=roles_mod_address,
        account=account,
        operation=operation
    )
    check_transaction = roles_mod.check_roles_transaction(contract_address, data)
    return check_transaction


def send_it(
    txs: List[Dict],
    role: int,
    private_key: str,
    roles_mod_address: str
) -> int:
    """send transaction to the blockchain

    Args:
        txs (List[Dict]): list of transactions dictionaries
        role (int): role that wants to execute
        private_key (str): to access the EOA
        roles_mod_address (str): address to call execTransactionWithRole

    Returns:
        int: 0 (fail) or 1 (success)
    """
    operation, contract_address, data, blockchain = multi_or_one(txs)
    roles_mod = RolesMod(
        blockchain,
        role,
        roles_mod_address,
        private_key,
        operation=operation
    )
    roles_mod_execute = roles_mod.roles_transaction(contract_address, data)
    print('building receipt....')
    roles_mod_tx1 = roles_mod.get_tx_receipt(roles_mod_execute)
    print(roles_mod_tx1)
    return roles_mod_tx1.status
