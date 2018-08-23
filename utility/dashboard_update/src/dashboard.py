def update(dashboard_str, replace_values):
    for val, replacement in replace_values:
        dashboard_str = dashboard_str.replace(val, '${' + replacement + '}')

    return dashboard_str
