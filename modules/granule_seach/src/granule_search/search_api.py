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

    @abc.abstractmethod
    def before(self, before_time):
        return NotImplemented

    @abc.abstractmethod
    def after(self, after_time):
        return NotImplemented

    @abc.abstractmethod
    def between(self, start_time, end_time):
        return NotImplemented

    @abc.abstractmethod
    def limit(self, amount):
        return NotImplemented


class QueryLimitError(Exception):
    pass
