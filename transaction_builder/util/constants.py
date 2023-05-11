from pathlib import Path
import os
import json
from .enums import Chain

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NODES
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if 'CONFIG_PATH' in os.environ:
    config_path = os.environ['CONFIG_PATH']
    with open(config_path, 'r') as config_file:
        config_data = json.load(config_file)
else:
    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0])+'/config.json', 'r') as config_file:
        config_data = json.load(config_file)

NODE_ETH = {
    'latest': config_data['nodes'][Chain.ETHEREUM.value]['latest'],
    'archival': config_data['nodes'][Chain.ETHEREUM.value]['archival']
}

NODE_POL = {
    'latest': config_data['nodes'][Chain.POLYGON.value]['latest'],
    'archival': config_data['nodes'][Chain.POLYGON.value]['archival']
}

NODE_XDAI = {
    'latest': config_data['nodes'][Chain.GNOSIS.value]['latest'],
    'archival': config_data['nodes'][Chain.GNOSIS.value]['archival']
}

NODE_BINANCE = {
    'latest': config_data['nodes'][Chain.BINANCE.value]['latest'],
    'archival': config_data['nodes'][Chain.BINANCE.value]['archival']
}

NODE_AVALANCHE = {
    'latest': config_data['nodes'][Chain.AVALANCHE.value]['latest'],
    'archival': config_data['nodes'][Chain.AVALANCHE.value]['archival']
}

NODE_FANTOM = {
    'latest': config_data['nodes'][Chain.FANTOM.value]['latest'],
    'archival': config_data['nodes'][Chain.FANTOM.value]['archival']
}

NODE_OPTIMISM = {
    'latest': config_data['nodes'][Chain.OPTIMISM.value]['latest'],
    'archival': config_data['nodes'][Chain.OPTIMISM.value]['archival']
}

class ETHAddr:
    AaveLendingPoolV2 = "0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7A9"
    ParaSwapRepayAdapter = "0x80Aca0C645fEdABaa20fd2Bf0Daf57885A309FE6"
    WrappedTokenGatewayV2 = "0xEFFC18fC3b7eb8E676dac549E0c693ad50D1Ce31"
    AAVE = "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
    ABPT = "0x41A08648C3766F9F9d85598fF102a08f4ef84F84"
    stkAAVE = "0x4da27a545c0c5B758a6BA100e3a049001de870f5"
    stkABPT = "0xa1116930326D21fB917d5A27F1E9943A9595fb47"
