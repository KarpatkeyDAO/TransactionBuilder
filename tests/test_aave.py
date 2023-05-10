from transaction_builder.util.enums import Chain
from transaction_builder.util.roles_class import RolesMod

from transaction_builder.protocols.aave import ApproveForAaveLendingPoolV2, ApproveForStkAAVE, ETHAddr, DeposiToken, DepositETH
from eth_abi import abi

BLOCKCHAIN = Chain.GNOSIS.value
USDT_CONTRACT = '0x4ECaBa5870353805a9F068101A40E0f32ed605C6'
AVATAR_ACCOUNT = '0x7e19DE37A31E40eec58977CEA36ef7fB70e2c5CD'

def decode_data_input(arg_types, data_input):
    return abi.decode(arg_types, bytes.fromhex(data_input[10:]))


def test_approve_method():
    method = ApproveForAaveLendingPoolV2(token=USDT_CONTRACT, amount=100000000)
    assert method.get_args_list() == [ETHAddr.AaveLendingPoolV2, 100000000]
    assert method.target_address == USDT_CONTRACT

    amount = 10000
    method = ApproveForStkAAVE(amount=amount)
    assert method.get_args_list() == [ETHAddr.stkAAVE, amount]
    assert method.as_data_input() == '0x095ea7b30000000000000000000000004da27a545c0c5b758a6ba100e3a049001de870f50000000000000000000000000000000000000000000000000000000000002710'
    decoded = decode_data_input(method.arg_types, method.as_data_input())
    assert decoded == (ETHAddr.stkAAVE, amount)


def test_approve_method_with_roles():
    method = ApproveForStkAAVE(amount=1000)
    ROLE = 2
    ROLES_MOD_ADDRESS = '0xB6CeDb9603e7992A5d42ea2246B3ba0a21342503'
    roles_mod = RolesMod(BLOCKCHAIN, ROLE, contract_address=ROLES_MOD_ADDRESS, account=AVATAR_ACCOUNT)
    check_transaction = roles_mod.check_roles_transaction(method.target_address, method.as_data_input())
    assert check_transaction


def test_deposit_method():
    method = DeposiToken(asset=USDT_CONTRACT, amount=100, avatar=AVATAR_ACCOUNT)
    referral_code = 0
    assert method.get_args_list() == [USDT_CONTRACT, 100, AVATAR_ACCOUNT, referral_code]
    assert method.target_address == ETHAddr.AaveLendingPoolV2


def test_deposit_eth():
    method = DepositETH(amount=100, avatar=AVATAR_ACCOUNT)
    referral_code = 0
    assert method.get_args_list() == [ETHAddr.AaveLendingPoolV2, AVATAR_ACCOUNT, referral_code]
    assert method.target_address == ETHAddr.WrappedTokenGatewayV2
    assert method.eth_value
