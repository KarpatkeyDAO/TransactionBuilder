"""Location of all Enum types."""

from enum import Enum
import json
from pathlib import Path
import os

if "CONFIG_PATH" in os.environ:
    config_path = os.environ["CONFIG_PATH"]
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)
else:
    config_path = str(Path(os.path.abspath(__file__)).resolve().parents[0] / "config.json")
    with open(config_path, "r") as config_file:
        config_data = json.load(config_file)


class ExtendedEnum(Enum):
    @classmethod
    def list(cls):
        """List all the values of the Enum."""
        return list(map(lambda c: c.value, cls))


class Chain(ExtendedEnum):
    """Enum for the blockchains."""

    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    GNOSIS = "gnosisChain"
    ARBITRUM = "arbitrum"
    BINANCE = "binance"
    AVALANCHE = "avalanche"
    FANTOM = "fantom"
    OPTIMISM = "optimism"
    AVAX = "avax"
    ROPSTEN = "ropsten"
    KOVAN = "kovan"
    GOERLI = "goerli"

    def __str__(self) -> str:
        """Represent as string."""
        return self.name

    def __repr__(self) -> str:
        """Represent as string."""
        return str(self)


class Explorer(ExtendedEnum):
    """Enum for the block explorers."""

    ETHERSCAN = "etherscan.io"
    POLYSCAN = "polygonscan.com"
    GNOSISSCAN = "gnosisscan.io"
    BSCSCAN = "bscscan.com"
    AVAXSCAN = "snowtrace.io"
    FTMSCAN = "ftmscan.io"

    def __str__(self) -> str:
        """Represent as string."""
        return self.name

    def __repr__(self) -> str:
        """Represent as string."""
        return str(self)


class Apikey(ExtendedEnum):
    """Enum for API keys."""

    API_KEY_ETHERSCAN = config_data["apikeys"]["etherscan"]
    API_KEY_POLSCAN = config_data["apikeys"]["polscan"]
    API_KEY_GNOSISSCAN = config_data["apikeys"]["gnosisscan"]
    API_KEY_BINANCE = config_data["apikeys"]["binance"]
    API_KEY_AVALANCHE = config_data["apikeys"]["avalanche"]
    API_KEY_FANTOM = config_data["apikeys"]["fantom"]
    API_KEY_OPTIMISM = config_data["apikeys"]["optimism"]
    API_KEY_ZAPPER = config_data["apikeys"]["zapper"]
    API_KEY_ETHPLORER = config_data["apikeys"]["ethplorer"]
