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