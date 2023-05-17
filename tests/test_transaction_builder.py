#!/usr/bin/env python

"""Tests for `transactionbuilder` package."""

import pytest

from transaction_builder import main
from transaction_builder.util.enums import Chain

PRIVATE_KEY = "xxxx"
BLOCKCHAIN = Chain.GNOSIS.value
ROLE = 2
ROLES_MOD_ADDRESS = "0xB6CeDb9603e7992A5d42ea2246B3ba0a21342503"
ACCOUNT = "0x7e19DE37A31E40eec58977CEA36ef7fB70e2c5CD"
MULTISEND = "0xA238CBeb142c10Ef7Ad8442C6D1f9E89e07e7761"

TXS = [
    {
        "blockchain": Chain.GNOSIS.value,
        "function_name": "approve",
        "function_args": ["0x7f90122BF0700F9E7e1F688fe926940E8839F353", 1000],
        "contract_address": "0x4ECaBa5870353805a9F068101A40E0f32ed605C6",
        "contract_abi": (
            '[{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve",'
            '"outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
            ),
        "operation": 0,
        "value": 0
    },
    {
        "blockchain": Chain.GNOSIS.value,
        "function_name": "add_liquidity",
        "function_args": [[0, 0, 100], 0],
        "contract_address": "0x7f90122bf0700f9e7e1f688fe926940e8839f353",
        "contract_abi": (
            '[{"stateMutability":"nonpayable","type":"function","name":"add_liquidity","inputs":[{"name":"_amounts","type":"uint256[3]"},'
            '{"name":"_min_mint_amount","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}],"gas":7295966}]'),
        "operation": 0,
        "value": 0
    },
]


def test_make_onesend():
    data = main.make_onesend(TXS[0])
    assert hasattr(data, "function_args")
    assert data.function_args == [
        "0x7f90122BF0700F9E7e1F688fe926940E8839F353",
        1000,
    ]
    assert hasattr(data, "function_name")
    assert data.function_name == "approve"


def test_make_multisend():
    data = main.make_multisend(TXS, BLOCKCHAIN, MULTISEND)
    assert data == ("0x8d80ff0a00000000000000000000000000000000000000000000000000000000000000200000000000000000000000000"
                    "000000000000000000000000000000000000172004ecaba5870353805a9f068101a40e0f32ed605c6000000000000000000"
                    "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                    "00000000044095ea7b30000000000000000000000007f90122bf0700f9e7e1f688fe926940e8839f3530000000000000000"
                    "0000000000000000000000000000000000000000000003e8007f90122bf0700f9e7e1f688fe926940e8839f353000000000"
                    "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                    "000000000000000000844515cef300000000000000000000000000000000000000000000000000000000000000000000000"
                    "000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
                    "000000000000000000006400000000000000000000000000000000000000000000000000000000000000000000000000000"
                    "000000000000000"
                    )


def test_multi_or_one():
    v, x, y, z = main.multi_or_one(TXS)
    assert v == 1
    assert x == "0xA238CBeb142c10Ef7Ad8442C6D1f9E89e07e7761"
    assert y == ('0x8d80ff0a000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000'
                 '00000000000000000000000000000000172004ecaba5870353805a9f068101a40e0f32ed605c600000000000000000000000000'
                 '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000440'
                 '95ea7b30000000000000000000000007f90122bf0700f9e7e1f688fe926940e8839f35300000000000000000000000000000000'
                 '000000000000000000000000000003e8007f90122bf0700f9e7e1f688fe926940e8839f35300000000000000000000000000000'
                 '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000844515'
                 'cef3000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                 '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000640000000000'
                 '0000000000000000000000000000000000000000000000000000000000000000000000000000000000'
                 )
    assert z == "gnosisChain"


def test_test_it():
    data = main.test_it(TXS, ROLE, ACCOUNT, ROLES_MOD_ADDRESS)
    assert data == True

# def test_send_it():
#     data = main.send_it(TXS,ROLE,PRIVATE_KEY,ROLES_MOD_ADDRESS)
#     assert data == 1
