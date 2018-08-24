"""
Troposphere template responsible for creating a cloudwatch dashboard

Resources
~~~~~~~~~

* **CloudWatch Dashboard:** Dashboard to monitor HyP3 infrastructure
"""


import pathlib as pl
import json

from troposphere import Sub, Ref, Output
from troposphere.cloudwatch import Dashboard

from template import t

from .hyp3_rds import db
from .hyp3_find_new import find_new_granules
from .hyp3_scheduler import scheduler
from .hyp3_send_email import send_email
from .hyp3_setup_db import setup_db

print('  adding hyp3 dashboard')


def get_dashboard_json():
    with (pl.Path(__file__).parent / 'dashboard.json').open('r') as f:
        return minifed(f.read())


def minifed(json_str):
    return json.dumps(json.loads(json_str))


hyp3_dashboard = t.add_resource(Dashboard(
    'HyP3Dashboard',
    DashboardName=Sub(
        '${StackName}-hyp3-monitoring',
        StackName=Ref('AWS::StackName')
    ),
    DashboardBody=Sub(
        get_dashboard_json(),
        FindNewGranulesName=Ref(find_new_granules),
        SchedulerName=Ref(scheduler),
        SendEmailName=Ref(send_email),
        SetupDBName=Ref(setup_db),
        HyP3DBInsatnceIdentifier=Ref(db)
    )
))

t.add_output(Output(
    "MonitoringDashboard",
    Description="Monitoring dashboard for hyp3",
    Value=Ref(hyp3_dashboard)
))
