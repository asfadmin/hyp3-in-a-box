import pathlib as pl

from troposphere import Parameter, Sub, Ref, Output
from troposphere.cloudwatch import Dashboard

from template import t

from hyp3_rds import db
from hyp3_find_new import find_new_granules
from hyp3_scheduler import scheduler
from hyp3_send_email import send_email

print('  adding hyp3 dashboard')

with (pl.Path(__file__).parent / 'dashboard.json').open('r') as f:
    dashboard_json = f.read()

dashboad_name = t.add_parameter(Parameter(
    'DashBoardName',
    Description="Name of the hyp3 monitoring dashboard",
    Default='hyp3-monitoring',
    Type="String"
))

hyp3_dashboard = t.add_resource(Dashboard(
    'Hyp3Dashboard',
    DashboardName=Ref(dashboad_name),
    DashboardBody=Sub(
        dashboard_json,
        FindNewGranulesName=Ref(find_new_granules),
        SchedulerName=Ref(scheduler),
        SendEmailName=Ref(send_email),
        Hyp3DBInsatnceIdentifier=Ref(db)
    )
))

t.add_output(Output(
    "MonitoringDashboard",
    Description="Monitoring dashboard for hyp3",
    Value=Ref(hyp3_dashboard)
))
