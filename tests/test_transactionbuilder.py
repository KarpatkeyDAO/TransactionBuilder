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

ROLES_MOD_ADDRESS = address_and_abi['roles_mod_address']
ROLES_MOD_ABI = address_and_abi['roles_mod_abi']
PRIVATE_KEY = 'xxxx'

cf = ContractFunction(blockchain= 'gnosisChain', function_args=USDT_FUNCTION_ARGS, function_name=USDT_FUNCTION_NAME, contract_address=USDT_CONTRACT_ADDRESS, contract_abi=USDT_CONTRACT_ABI)

def test_roles_transaction(blockchain,role,private_key,roles_contract_address,roles_contract_abi):

    roles_mod = RolesMod(blockchain,role,private_key,roles_contract_address,roles_contract_abi).roles_transaction(cf)

    assert cf.data_input() == 'hex of length ...'
    assert roles_mod.gas_limit == 'between 0 and 500000'
    assert roles_mod.base_fee == 'above 0'
    assert roles_mod == 'txhash'

def test_get_tx_receipt():



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
