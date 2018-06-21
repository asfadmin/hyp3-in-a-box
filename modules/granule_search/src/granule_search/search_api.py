import abc


class GranuleSearchAPI(abc.ABC):
    """A generic interface for granule search api's"""
    @property
    @abc.abstractmethod
    def api_url(self):
        """Base url for the api"""
        return NotImplemented

    @abc.abstractmethod
    def search(self):
        """ Build the query for the search api

            :returns: the results returned by the api
            :rtype: dict
        """
        return NotImplemented

    @abc.abstractmethod
    def before(self, before_time):
        """ Get granules before a date

            :param datetime.datetime before_time: Date to get granules before

            :returns: the GranuleSearchAPI object for dot chaining
            :rtype: GranuleSearchAPI
        """
        return NotImplemented

    @abc.abstractmethod
    def after(self, after_time):
        """ Get granules after a date

            :param datetime.datetime after_time: Date to get granules after

            :returns: the GranuleSearchAPI object for dot chaining
            :rtype: GranuleSearchAPI
        """
        return NotImplemented

    @abc.abstractmethod
    def between(self, before_time, after_time):
        """ Get granules after a date

            :param datetime.datetime before_time: Begining of the daterange
            :param datetime.datetime after_time:  End of the daterange

            :returns: the GranuleSearchAPI object for dot chaining
            :rtype: GranuleSearchAPI
        """
        return NotImplemented

    @abc.abstractmethod
    def limit(self, amount):
        """ Limit the amount of search results returned by the query

            :param int amount: amount of results to return

            :returns: the GranuleSearchAPI object for dot chaining
            :rtype: GranuleSearchAPI
        """
        return NotImplemented


class QueryLimitError(Exception):
    pass
