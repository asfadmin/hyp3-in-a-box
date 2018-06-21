"""
    This module defines an interface for wrapping granule seach api's.
    This is so that the search api for hyp3 can be easily swapped if a
    different one is desired (e.g. CMR, ASF API)
"""

from .cmr import CMR
from .search_api import GranuleSearchAPI, QueryLimitError

__all__ = ['GranuleSearchAPI', 'CMR', 'QueryLimitError']
