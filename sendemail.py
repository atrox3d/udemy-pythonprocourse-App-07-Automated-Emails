import yagmail

from secret.google_app_password import USER, PASSWORD
from secret.mail_recipients import RECIPIENTS

email = yagmail.SMTP(
    user=USER,
    password=PASSWORD
)

email.send(
    to=RECIPIENTS,
    subject='testing, testing',
    contents="hello from yagmail",
    attachments='newsfeed.py'
)
