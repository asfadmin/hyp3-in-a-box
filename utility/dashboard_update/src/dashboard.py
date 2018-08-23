from typing import List, Tuple


def update(dashboard: str, stack: str) -> str:
    items = [
        (f"{stack}_hyp3_find_new_granules", "FindNewGranulesName"),
        (f"{stack}_hyp3_scheduler", "SchedulerName"),
        (f"{stack}_hyp3_send_email", "SendEmailName"),
        (f"{stack}-hyp3-rds-instance", "HyP3DBInsatnceIdentifier"),
        (f"{stack}_hyp3_setup_db", "SetupDBName"),
        (f"{stack}-Hyp3StartEvents-1C128S3RPSFB4.fifo", "StartEventQueue"),
        (f"{stack}-HyP3AutoscalingGroup-1QQ8WGQU4WQIG", "AutoscalingGroup"),
        ('us-west-2', 'AWS::Region')
    ]

    return update_values(dashboard, replace_values=items)


def update_values(dashboard_str, replace_values: List[Tuple[str, str]]) -> str:
    for val, replacement in replace_values:
        dashboard_str = dashboard_str.replace(val, '${' + replacement + '}')

    return dashboard_str
