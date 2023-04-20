from dataclasses import dataclass
from util.enums import Chain, Explorer, Apikey
import os

# Mapping of blockchains to their respective block explorers and API keys
blockexplorers = {
    Chain.ETHEREUM.value: [Explorer.ETHERSCAN.value, Apikey.API_KEY_ETHERSCAN.value],
    Chain.POLYGON.value: [Explorer.POLYSCAN.value, Apikey.API_KEY_POLSCAN.value],
    Chain.GNOSIS.value: [Explorer.GNOSISSCAN.value, Apikey.API_KEY_GNOSISSCAN.value],
    Chain.BINANCE.value: [Explorer.BSCSCAN.value, Apikey.API_KEY_BINANCE.value],
    Chain.AVALANCHE.value: [Explorer.AVAXSCAN.value, Apikey.API_KEY_AVALANCHE.value],
    Chain.FANTOM.value: [Explorer.FTMSCAN.value, Apikey.API_KEY_FANTOM.value],
}

print(blockexplorers)


@dataclass
class Explorer:
    """
    A data class for handling blockchain explorers and their API keys.

    Attributes:
        blockchain (str): The blockchain identifier.
    """
    blockchain: str

    def get_explorer(self) -> str:
        """
        Get the block explorer URL for the given blockchain.

        Returns:
            str: The block explorer URL.
        """
        for k, v in blockexplorers.items():
            if k == self.blockchain:
                return v[0]

    def get_private_key(self) -> str:
        """
        Get the API key for the given blockchain.

        Returns:
            str: The API key.
        """
        for k, v in blockexplorers.items():
            if k == self.blockchain:
                return v[1]
