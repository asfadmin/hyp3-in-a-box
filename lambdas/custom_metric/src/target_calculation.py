import math


def calculate_metric(num_messages, num_instances):
    target_jobs_per_instance = 10

    if num_instances == 0:
        if num_messages <= target_jobs_per_instance:
            return math.ceil(num_messages / target_jobs_per_instance) * 2
        else:
            return math.ceil(num_messages / target_jobs_per_instance)
    else:
        return math.ceil(
            num_messages / (num_instances * target_jobs_per_instance)
        )
