import smtplib


class NotificationManager:
    def __init__(self, from_email, password, smtp):
        self.from_email = from_email
        self.password = password
        self.smtp = smtp

    def send_email(self, message, to_email):
        with smtplib.SMTP(self.smtp, port=587) as connection:
            connection.starttls()
            connection.login(user=self.from_email, password=self.password)
            connection.sendmail(
                from_addr=self.from_email,
                to_addrs=to_email,
                msg=message
            )