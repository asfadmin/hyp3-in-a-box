def send_mock(*args, **kwargs):
    with open('email-output.html', 'w') as f:
        f.write(args[2])
