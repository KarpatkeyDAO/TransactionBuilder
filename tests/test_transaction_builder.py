#!/usr/bin/env python

"""Tests for `transactionbuilder` package."""

import pytest

#from click.testing import CliRunner

from transaction_builder import main
from transaction_builder.util.enums import Chain

BLOCKCHAIN = Chain.GNOSIS.value
FUNCTION_ARGS = ['0x7f90122BF0700F9E7e1F688fe926940E8839F353',100000000]
FUNCTION_NAME = 'approve'
CONTRACT_ADDRESS = '0x4ECaBa5870353805a9F068101A40E0f32ed605C6'
CONTRACT_ABI = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},\
                 {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
ROLE = 2  
ROLES_MOD_ADDRESS = '0xB6CeDb9603e7992A5d42ea2246B3ba0a21342503'
ACCOUNT = '0x7e19DE37A31E40eec58977CEA36ef7fB70e2c5CD'

def test_test_it():
    data = main.test_it(BLOCKCHAIN,FUNCTION_ARGS,FUNCTION_NAME,CONTRACT_ADDRESS,CONTRACT_ABI,ROLE,ACCOUNT,ROLES_MOD_ADDRESS)
    assert data == True

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
