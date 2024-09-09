import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(to, subject, body_params):
    """
    :param to: recipients email address - string
    :param subject: email subject
    :param body_params: mail body parameters - json object
    :return:
    """
    message = Mail(
        from_email='Askante<no-reply@askante.net>',
        to_emails=to,
        subject=subject,
    )
    message.dynamic_template_data = body_params
    message.template_id = 'd-7ab3828519fd42259a4369de79f9d832'
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)
    except Exception as e:
        print(str(e))
