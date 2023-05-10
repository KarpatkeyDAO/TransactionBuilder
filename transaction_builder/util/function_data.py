from typing import Optional, Union
from dataclasses import dataclass
import json

from web3 import Web3
from web3._utils.abi import get_abi_input_types, filter_by_name
from eth_abi import encode

from .functions import get_node


@dataclass
class ContractFunction:
    blockchain: str
    function_args: list
    function_name: str
    contract_address: str
    contract_abi: str
    operation: Optional[int] = 0
    value: Optional[int] = 0
    web3: Optional[Web3] = None
    contract_instance: Optional[Web3] = None
    function_instance: Optional[Web3] = None

    def __post_init__(self):
        if not self.web3:
            self.web3 = get_node(self.blockchain)
        self.contract_address = self.web3.to_checksum_address(self.contract_address)
        self.contract_instance = self.web3.eth.contract(
            address=self.contract_address, abi=self.contract_abi
        )
        self.function_instance = self.contract_instance.functions[self.function_name]

    def call_function(self) -> Union[list, str, int]:
        """Call the contract function with the given arguments."""
        result = self.function_instance(*self.function_args).call()
        return result

    def data_input(self) -> str:
        """Create the data input for the contract function."""
        name = filter_by_name(self.function_name, json.loads(self.contract_abi))[0]
        types = get_abi_input_types(name)
        signature = (
            Web3.keccak(text=f"{self.function_name}({','.join(types)})").hex()[:10]
        )
        result = f"{signature}{encode(types, self.function_args).hex()}"
        return result
