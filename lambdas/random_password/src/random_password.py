import random
import string

import custom_resource


def send_response(event):
    response = RandomPassword(event) \
        .get_response()

    return custom_resource.send(event, response)


class RandomPassword(custom_resource.Base):
    def _process(self):
        random_password = self._get_random_string()

        return {
            'Data': {'Password': random_password},
            'Reason': 'Successfully generated a random string'
        }

    def _get_random_string(self):
        length = self._get_length()

        characters = string.digits + string.ascii_letters

        random_string = ''.join(
            random.SystemRandom().choice(characters) for _ in range(length)
        )

        return random_string

    def _get_length(self):
        try:
            length = int(self.event['ResourceProperties']['Length'])
        except KeyError:
            raise custom_resource.CustomResourceException(
                'Must specify a length'
            )
        except ValueError:
            raise custom_resource.CustomResourceException(
                'Length not an integer'
            )

        return length
