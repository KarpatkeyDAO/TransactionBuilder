#!/usr/bin/env python

"""Tests for `transactionbuilder` package."""

import pytest

from click.testing import CliRunner

from transactionbuilder import transactionbuilder
from transactionbuilder import cli
from utils.addressAbi import address_and_abi
from transactionbuilder.util.function_data import ContractFunction
from transactionbuilder.util.roles_class import RolesMod

BLOCKCHAIN = 'gnosisChain'

USDT_CONTRACT_ADDRESS = address_and_abi['usdt_address']
USDT_CONTRACT_ABI = address_and_abi['usdt_address_abi']
USDT_FUNCTION_NAME = 'approve'
USDT_FUNCTION_ARGS = [address_and_abi['curve_address'],100000000]

cf = ContractFunction(blockchain= 'gnosisChain', function_args=USDT_FUNCTION_ARGS, function_name=USDT_FUNCTION_NAME, contract_address=USDT_CONTRACT_ADDRESS, contract_abi=USDT_CONTRACT_ABI)

@pytest.fixture
def roles_mod(blockchain,role,private_key,roles_contract_address,roles_contract_abi):
    yield RolesMod(
        blockchain=blockchain,
        role=role,
        private_key=private_key,
        contract_address=roles_contract_address,
        contract_abi=roles_contract_abi
    )

def test_roles_transaction(roles_mod):

    tx_hash = roles_mod.roles_transaction(cf)

    assert cf.data_input() == '0x095ea7b30000000000000000000000007f90122bf0700f9e7e1f688fe926940e8839f3530000000000000000000000000000000000000000000000000000000005f5e100'
    assert 0 <= tx_hash.gas_limit <= 500000, "gas_limit must be between 0 and 500000"
    assert tx_hash.base_fee > 0, "Base-fee must be above 0"

    assert isinstance(tx_hash, str), "Transaction hash must be a string."
    assert len(tx_hash) == 66, "Transaction hash must be 66 characters long."
    assert tx_hash.startswith("0x"), "Transaction hash must start with '0x'."
    assert all(c in "0123456789abcdefABCDEF" for c in tx_hash[2:]), "Transaction hash must only include numbers 0-9 and letters a-f."

def test_get_tx_receipt(roles_mod, tx_hash):
    
    tx_receipt = roles_mod.get_tx_receipt(tx_hash)
    assert isinstance(tx_receipt, dict), "tx_receipt must be a dict"
    assert tx_receipt["status"] == 1, "tx_receipt must have status of 1 (successful)"

# @pytest.fixture
# def response():
#     """Sample pytest fixture.

#     See more at: http://doc.pytest.org/en/latest/fixture.html
#     """
#     # import requests
#     # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


# def test_content(response):
#     """Sample pytest test function with the pytest fixture as an argument."""
#     # from bs4 import BeautifulSoup
#     # assert 'GitHub' in BeautifulSoup(response.content).title.string


# def test_command_line_interface():
#     """Test the CLI."""
#     runner = CliRunner()
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert 'transactionbuilder.cli.main' in result.output
#     help_result = runner.invoke(cli.main, ['--help'])
#     assert help_result.exit_code == 0
#     assert '--help  Show this message and exit.' in help_result.output
