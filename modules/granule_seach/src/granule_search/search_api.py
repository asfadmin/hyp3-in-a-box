import abc


class GranuleSearchAPI(abc.ABC):
    """ Class to wrap generic granule seach api"""

    @property
    @abc.abstractmethod
    def api_url(self):
        """Base url for the api"""
        return NotImplemented

    @abc.abstractmethod
    def search(self):
        """Build the query for the search api"""
        return NotImplemented
