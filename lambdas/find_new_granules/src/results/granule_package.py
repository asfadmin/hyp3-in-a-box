class GranulePackage:
    """Object to hold relevant granule information"""
    def __init__(self, name, polygon, download_url):
        """
            :param str name: name of the granule
            :param list[float] polygon: points representing the granules shape
            :param str download_url: url to download the granule
        """
        self.name = name
        self.polygon = polygon
        self.download_url = download_url

    def to_dict(self):
        return {
            'polygon': self.polygon,
            'name': self.name,
            'download_url': self.download_url
        }
