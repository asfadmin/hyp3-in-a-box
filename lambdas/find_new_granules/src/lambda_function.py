import find_new
from find_new import environment as env
import results


def lambda_handler(event, context):
    env.set_is_production(True)

    search_results = find_new.granules()

    return results.package(search_results)
