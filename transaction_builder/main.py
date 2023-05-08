"""Main module."""
import os

from transaction_builder.util.enums import Chain
from transaction_builder.util.function_data import ContractFunction
from transaction_builder.util.roles_class import RolesMod

# blockchain = Chain.GNOSIS.value
# function_args = ['0x7f90122BF0700F9E7e1F688fe926940E8839F353',100000000]
# function_name = 'approve'
# contract_address = '0x4ECaBa5870353805a9F068101A40E0f32ed605C6'
# contract_abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},\
#                 {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

# role = 2
# account = '0x7e19DE37A31E40eec58977CEA36ef7fB70e2c5CD'
# roles_mod_address = '0xB6CeDb9603e7992A5d42ea2246B3ba0a21342503'

def test_it(blockchain: str,function_args: list,function_name:list,contract_address:str,contract_abi:str,role:int,account:str,roles_mod_address:str) -> dict:
    cf = ContractFunction(blockchain, function_args, function_name, contract_address, contract_abi)
    roles_mod = RolesMod(blockchain, role, contract_address=roles_mod_address,account=account)
    check_transaction = roles_mod.check_roles_transaction(cf)
    return check_transaction


def send_it(blockchain: str,function_args: list,function_name:list,contract_address:str,contract_abi:str,role:int,private_key:str,roles_mod_address:str) -> dict:

    cf = ContractFunction(blockchain, function_args, function_name, contract_address, contract_abi)
    roles_mod = RolesMod(blockchain, role, private_key, roles_mod_address)
    roles_mod_execute = roles_mod.roles_transaction(cf)
    print('building receipt....')
    roles_mod_tx1 = roles_mod.get_tx_receipt(roles_mod_execute)
    print(roles_mod_tx1.status)

# def main():
#     pass
#     blockchain = Chain.GNOSIS.value
#     function_args = ['0x7f90122BF0700F9E7e1F688fe926940E8839F353',100000000]
#     function_name = 'approve'
#     contract_address = '0x4ECaBa5870353805a9F068101A40E0f32ed605C6'
#     contract_abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},\
#                 {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

#     role = 2
#     account = '0x7e19DE37A31E40eec58977CEA36ef7fB70e2c5CD'
#     roles_mod_address = '0xB6CeDb9603e7992A5d42ea2246B3ba0a21342503'

#     test_it(blockchain,function_args,function_name,contract_address,contract_abi,role,account,roles_mod_address)

# if __name__ == "__main__":
#     main()