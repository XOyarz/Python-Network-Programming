#!/usr/bin/env python3

import email.message, email.policy, sys

text = """\
cumpleaños feliz"""

def main():
    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'Iñaki <recipient@example.com>'
    message['From'] = 'Eadstapa <sender@example.com>'
    message['Subject'] = 'Four lines from poetry'
    message['Date'] = email.utils.formatdate(localtime=True)
    message.set_content(text, cte='quoted-printable')
    sys.stdout.buffer.write(message.as_bytes())

if __name__ == '__main__':
    main()