class GranulePackage:
    """Object to hold relevant granule information for the scheduler lambda"""
    def __init__(self, name, polygon, download_url):
        """
            :param str name: name of the granule
            :param list[float] polygon: points representing the granules shape
            :param str download_url: The url to download the granule
        """
        self.name = name
        self.polygon = polygon
        self.download_url = download_url

    def to_dict(self):
        return self.__dict__
