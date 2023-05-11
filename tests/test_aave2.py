from transaction_builder.protocols.aave2 import deposit, approve_for_aave_lending_poolv2
from transaction_builder.util.constants import ETHAddr

USDT_CONTRACT = '0x4ECaBa5870353805a9F068101A40E0f32ed605C6'
AVATAR_ACCOUNT = '0x7e19DE37A31E40eec58977CEA36ef7fB70e2c5CD'

def test_deposit_method_as_instance():
    method = deposit.with_args(asset=USDT_CONTRACT, amount=100, avatar=AVATAR_ACCOUNT)
    referral_code = 0
    assert method.args == [USDT_CONTRACT, 100, AVATAR_ACCOUNT, referral_code]
    assert method.target_address == ETHAddr.AaveLendingPoolV2

def test_approve_for_aave_lending_poolv2():
    method = approve_for_aave_lending_poolv2.with_args(amount=123, target_address=USDT_CONTRACT)
    assert method.target_address == USDT_CONTRACT
    assert method.args == [ETHAddr.AaveLendingPoolV2, 123]
    assert method.data == "0x095ea7b30000000000000000000000007d2768de32b0b80b7a3454c06bdac94a69ddc7a9000000000000000000000000000000000000000000000000000000000000007b"

