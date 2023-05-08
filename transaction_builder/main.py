"""Main module."""
import os

from transaction_builder.util.enums import Chain
from transaction_builder.util.function_data import ContractFunction
from transaction_builder.util.roles_class import RolesMod

def test_it(blockchain: str,function_args: list,function_name:list,contract_address:str,contract_abi:str,role:int,account:str,roles_mod_address:str) -> dict:
    cf = ContractFunction(blockchain, function_args, function_name, contract_address, contract_abi)
    roles_mod = RolesMod(blockchain, role, contract_address=roles_mod_address,account=account)
    roles_mod.check_roles_transaction(cf)   


# def send_it(blockchain: str,function_args: list,function_name:list,contract_address:str,contract_abi:str,role:int,private_key:str,roles_mod_address:str) -> dict:

#     cf = ContractFunction(blockchain, function_args, function_name, contract_address, contract_abi)
#     roles_mod = RolesMod(blockchain, role, private_key, roles_mod_address)
#     roles_mod_execute = roles_mod.roles_transaction(cf)
#     print('building receipt....')
#     roles_mod_tx1 = roles_mod.get_tx_receipt(roles_mod_execute)
#     print(roles_mod_tx1.status)

def main():
    pass
    # blockchain = Chain.ETHEREUM.value
    # function_args = [13591818202360617192285,False]
    # function_name = ['withdrawAndUnwrap']
    # contract_address = '0xe4683Fe8F53da14cA5DAc4251EaDFb3aa614d528'
    # contract_abi = ''
    # role = 2
    # private_key = ''
    # roles_mod_address = ''

    #send_it(blockchain,function_args,function_name,contract_address,contract_abi,role,private_key,roles_mod_address)

if __name__ == "__main__":
    main()