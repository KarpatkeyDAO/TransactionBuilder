from pathlib import Path
import os
import json

from dataclasses import dataclass
from typing import Optional, List, Dict

from web3 import Web3

from util.api import RequestFromScan
from util.functions import get_node


@dataclass
class UpdateDB:
    """A class to update ABI and Gas Limit databases."""

    blockchain: str
    roles_mod_address: str
    start_block: Optional[int] = 0
    result: Optional[List[Dict]] = None

    def __post_init__(self):
        self.result = RequestFromScan('account', 'txlist', self.blockchain,
                                      kwargs={'address': self.roles_mod_address, 'startblock': self.start_block}).request()['result']

    def decode_input(self, input_data: str) -> str:
        """Decode input data.

        Args:
            input_data (str): The input data to decode.

        Returns:
            str: The decoded input data.
        """
        data_start = input_data[138:202]
        data_input = input_data[10:]
        starts_at = int('0x' + data_start, 16) * 2
        data_length = data_input[starts_at:starts_at + 64]
        length = int('0x' + data_length, 16) * 2
        starts_data = data_input[starts_at + 64:starts_at + 64 + length]
        return '0x' + starts_data[:8]

    def update_abi_db(self):
        """Update the ABI database."""
        db_file_path = Path(__file__).resolve().parent.parent / 'db' / 'functionabis.json'
        with open(db_file_path) as db_file:
            abi_db = json.load(db_file)

        for result in self.result:
            existing_addresses = [d['address'] for d in abi_db]
            address = '0x' + result['input'][34:74]

            if address not in existing_addresses:
                abi = RequestFromScan(blockchain=self.blockchain, module='contract', action='getabi',
                                      kwargs={'address': address}).request()['result']
                new_dict = {"blockchain": self.blockchain, "address": address, "abi": abi}
                abi_db.append(new_dict)

        with open(db_file_path, 'w') as f:
            json.dump(abi_db, f)

    def update_gaslimit_db(self):
        """Update the Gas Limit database."""
        db_file_path = Path(__file__).resolve().parent.parent / 'db' / 'gaslimit.json'
        with open(db_file_path) as db_file:
            abi_db = json.load(db_file)

        for result in self.result:
            if result['txreceipt_status'] == '1':
                existing_functions = [d['function'] for d in abi_db]
                function_name = self.decode_input(result['input'])
                gas_limit = result['gasUsed']

                if function_name not in existing_functions:
                    new_dict = {"blockchain": self.blockchain, "function": function_name, "gas_limit": gas_limit}
                    abi_db.append(new_dict)

        with open(db_file_path, 'w') as f:
            json.dump(abi_db, f)


