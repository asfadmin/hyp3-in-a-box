def send_mock(address, subject, message):
    with open('output.html', 'w') as f:
        f.write(message)
