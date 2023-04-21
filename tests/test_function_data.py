from transactionbuilder.util.function_data import ContractFunction
from test_abi import roles_mod_abi

BLOCKCHAIN = 'gnosisChain'
ROLES_CONTRACT_ADDRESS = '0xb6cedb9603e7992a5d42ea2246b3ba0a21342503'
ROLES_MOD_ABI = roles_mod_abi
FUNCTION_NAME = 'decimals'

cf = ContractFunction(blockchain= 'gnosisChain', function_args=[curve_contract_address,100000000], function_name='approve', contract_address=usdt_contract_address, contract_abi=usdt_contract_abi)
cf2 = ContractFunction(blockchain= 'gnosisChain', function_args=[amounts,0], function_name='add_liquidity', contract_address=curve_contract_address, contract_abi=curve_contract_abi)

def test_call_function():
    
    assert

