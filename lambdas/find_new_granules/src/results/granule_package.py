class GranulePackage:
    """Object to hold relevant granule information for the scheduler lambda"""
    def __init__(self, name, polygon):
        """
            :param str name: name of the granule
            :param list[float] polygon: points representing the granules shape
        """
        self.name = name
        self.polygon = polygon

    def to_dict(self):
        return {
            'polygon': self.polygon,
            'name': self.name
        }
