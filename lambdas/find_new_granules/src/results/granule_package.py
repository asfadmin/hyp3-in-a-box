import collections

GranuleMetadata = collections.namedtuple('GranuleMetadata', [
    'name',
    'polygon',
    'download_url'
])


class GranulePackage(GranuleMetadata):
    def to_dict(self):
        return {
            'polygon': self.polygon,
            'name': self.name,
            'download_url': self.download_url
        }
