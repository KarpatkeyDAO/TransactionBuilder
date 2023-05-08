from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import json

from web3 import Web3, exceptions
from eth_account import Account

from util.function_data import ContractFunction
from util.functions import get_node


@dataclass
class RolesMod:
    """A class to handle role-based transactions on a blockchain."""

    blockchain: str
    role: int
    contract_address: str
    private_key: Optional[str] = None
    account: Optional[str] = None
    contract_abi: Optional[str] = None 
    operation: Optional[int] = 0
    value: Optional[int] = 0
    should_revert: Optional[bool] = False
    chain_id: Optional[int] = None
    nonce: Optional[int] = None

    def __post_init__(self):
        if not self.private_key and not self.account:
            raise ValueError("Either 'private_key' or 'account' must be filled.")
        if not self.web3:
            self.web3 = get_node(self.blockchain)
        if self.private_key:
            self.account = Account.from_key(self.private_key)
        self.contract_instance = self.web3.eth.contract(
            address=self.contract_address, abi=self.contract_abi
        )

    def get_base_fee(self) -> int:
        """Get the base fee.

        Returns:
            int: The base fee.
        """
        latest_block = self.web3.eth.get_block('latest')
        gas_used = latest_block['gasUsed']
        base_fee_per_gas = latest_block['baseFeePerGas']
        base_fee = gas_used * base_fee_per_gas
        return base_fee * 2

    def get_gas_limit(self, function_hex: str) -> int:
        """Get the gas limit for a specific function.

        Args:
            function_hex (str): The function hex string.

        Returns:
            int: The gas limit.
        """
        db_file_path = Path(__file__).resolve().parent.parent / 'db' / 'gaslimit.json'
        with open(db_file_path) as db_file:
            gas_limit_db = json.load(db_file)

        for x in gas_limit_db:
            if x['function'] == function_hex and x['blockchain'] == self.blockchain:
                return int(x['gas_limit']) + 100000
        return 500000

    def check_roles_transaction(self, cf: ContractFunction):
        """make static call to validate transaction

        Args:
            cf (ContractFunction): The contract function to execute
        """
        try:
            self.contract_instance.functions.execTransactionWithRole(
            cf.contract_address, self.value, cf.data_input(), self.operation, self.role, self.should_revert
            ).call({'from': self.account.address})
            return True
        except exceptions.ContractLogicError:
            return False

    def roles_transaction(self, cf: ContractFunction, max_prio: int = None, max_gas: int = None, gas_limit: int = None) -> str:
        """Execute a role-based transaction.

        Args:
            cf (ContractFunction): The contract function to execute.
            max_prio (int, optional): The maximum priority fee.
            max_gas (int, optional): The maximum gas fee.
            gas_limit (int, optional): The gas limit.

        Returns:
            str: The transaction hash.
        """
        if not max_prio:
            max_prio = self.web3.eth.max_priority_fee

        if not max_gas:
            max_gas = max_prio + self.get_base_fee()

        if not gas_limit:
            gas_limit = self.get_gas_limit(cf.data_input()[:10])
        
        if not self.check_roles_transaction(cf):
            print('transaction will be reverted')

        tx = self.contract_instance.functions.execTransactionWithRole(
            cf.contract_address, self.value, cf.data_input(), self.operation, self.role, self.should_revert
        ).build_transaction({
            'chainId': self.chain_id or self.web3.eth.chain_id,
            'gas': gas_limit,
            'maxFeePerGas': max_gas,
            'maxPriorityFeePerGas': max_prio,
            'nonce': self.nonce or self.web3.eth.getTransactionCount(self.account.address),
        })

        signed_txn = self.web3.eth.account.sign_transaction(tx, self.private_key)
        executed_txn = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return executed_txn.hex()

    def get_tx_receipt(self, tx_hash: str):
        try:
            transaction_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return  transaction_receipt
        except exceptions.TransactionNotFound:
            return 'Transaction not yet on blockchain'
