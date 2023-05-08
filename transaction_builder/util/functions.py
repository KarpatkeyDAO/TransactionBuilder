import functools
import lru
import logging
from decimal import *

from web3 import Web3
from web3.middleware import construct_simple_cache_middleware

from .enums import Chain
from .constants import NODE_ETH,NODE_POL,NODE_XDAI,NODE_FANTOM,NODE_OPTIMISM,NODE_BINANCE,NODE_AVALANCHE

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CUSTOM EXCEPTIONS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class GetNodeIndexError(Exception):
    """

    """
    pass


class abiNotVerified(Exception):
    """

    """

    def __init__(self, message='Contract source code not verified') -> None:
        self.message = message
        super().__init__(self.message)


def get_web3_provider(endpoint):
    provider = Web3.HTTPProvider(endpoint)

    web3 = Web3(provider)

    # enable simple web3 cache, for example to cache eth_chainId calls
    # more methods can be cached after analysing whether they are safe to cache
    simple_cache = construct_simple_cache_middleware(
        cache_class=functools.partial(lru.LRU, 4096),
        rpc_whitelist={'eth_chainId'},
    )

    class CallCounterMiddleware:
        call_count = 0

        def __init__(self, make_request, w3):
            self.w3 = w3
            self.make_request = make_request

        @classmethod
        def increment(cls):
            cls.call_count += 1

        def __call__(self, method, params):
            self.increment()
            logger.debug('Web3 call count: %d', self.call_count)
            response = self.make_request(method, params)
            return response

    web3.middleware_onion.add(CallCounterMiddleware, 'call_counter')
    # adding the cache after to get only effective calls counted by the counter
    web3.middleware_onion.add(simple_cache, 'simple_cache')
    return web3

def get_web3_call_count(web3):
    """Obtain the total number of calls that have been made by a web3 instance."""
    return web3.middleware_onion['call_counter'].call_count


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_node
# 'block' = 'latest' -> retrieves a Full Node / 'block' = block or not passed onto the function -> retrieves an Archival Node
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_node(blockchain, block='latest', index=0):
    """

    :param blockchain:
    :param block:
    :param index:
    :return:
    """
    if blockchain == Chain.ETHEREUM.value:
        node = NODE_ETH

    elif blockchain == Chain.POLYGON.value:
        node = NODE_POL

    elif blockchain == Chain.GNOSIS.value:
        node = NODE_XDAI

    elif blockchain == Chain.BINANCE.value:
        node = NODE_BINANCE

    elif blockchain == Chain.AVALANCHE.value:
        node = NODE_AVALANCHE

    elif blockchain == Chain.FANTOM.value:
        node = NODE_FANTOM

    elif blockchain == Chain.OPTIMISM.value:
        node = NODE_OPTIMISM

    else:
        raise Exception

    if isinstance(block, str):
        if block == 'latest':
            if index > (len(node['latest']) - 1):
                if index > (len(node['latest']) + len(node['archival']) - 1):
                    raise GetNodeIndexError
                else:
                    web3 = get_web3_provider(node['archival'][index - len(node['latest'])])
            else:
                web3 = get_web3_provider(node['latest'][index])
        else:
            raise ValueError('Incorrect block.')

    else:
        if index > (len(node['archival']) - 1):
            raise GetNodeIndexError
        else:
            web3 = get_web3_provider(node['archival'][index])


    # enable simple web3 cache, for example to cache eth_chainId calls
    # more methods can be cached after analysing whether they are safe to cache
    simple_cache = construct_simple_cache_middleware(
        cache_class=functools.partial(lru.LRU, 4096),
        rpc_whitelist={'eth_chainId'},
    )
    web3.middleware_onion.add(simple_cache)
    return web3