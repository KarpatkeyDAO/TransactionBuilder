"""Main module."""
import os
from util.function_data import ContractFunction
from util.roles_class import RolesMod



from util.update_db import UpdateDB


update_db = UpdateDB('gnosisChain','0xb6cedb9603e7992a5d42ea2246b3ba0a21342503')
abis = update_db.update_abi_db()
gas_limits = update_db.update_gaslimit_db()
print(abis)
print(gas_limits)

curve_contract_address = '0x7f90122BF0700F9E7e1F688fe926940E8839F353'
curve_contract_abi = '[{"stateMutability":"nonpayable","type":"function","name":"add_liquidity","inputs":[{"name":"_amounts","type":"uint256[3]"},{"name":"_min_mint_amount","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}],"gas":7295966}]'
#amounts = [xdai, usdc, usdt ]
amounts = [0,0,10]

usdt_contract_address = '0x4ECaBa5870353805a9F068101A40E0f32ed605C6'
usdt_contract_abi = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},\
                {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

roles_mod_contract = '0xB6CeDb9603e7992A5d42ea2246B3ba0a21342503'
roles_mod_abi = '[{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"success","internalType":"bool"}],"name":"execTransactionWithRole","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"},{"type":"bytes","name":"data","internalType":"bytes"},{"type":"uint8","name":"operation","internalType":"enum Enum.Operation"},{"type":"uint16","name":"role","internalType":"uint16"},{"type":"bool","name":"shouldRevert","internalType":"bool"}]}]'

private_key='xxxx'
print('making tx 1')

cf = ContractFunction(blockchain= 'gnosisChain', function_args=[curve_contract_address,100000000], function_name='approve', contract_address=usdt_contract_address, contract_abi=usdt_contract_abi)
print(cf.data_input())
cf2 = ContractFunction(blockchain= 'gnosisChain', function_args=[amounts,0], function_name='add_liquidity', contract_address=curve_contract_address, contract_abi=curve_contract_abi)
roles_mod = RolesMod(blockchain='gnosisChain', role=2, private_key=private_key,contract_address=roles_mod_contract, contract_abi=roles_mod_abi)
roles_mod_execute1 = roles_mod.roles_transaction(cf)
print('printing receipt 1.....')
roles_mod_tx1 = roles_mod.get_tx_receipt(roles_mod_execute1)
print(roles_mod_tx1.status)
print('next tx')
roles_mod_execute2 = roles_mod.roles_transaction(cf2)
print('printing receipt....')

roles_mod_tx2 = roles_mod.get_tx_receipt(roles_mod_execute2)
print(roles_mod_tx2.status)