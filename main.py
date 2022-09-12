import yagmail
import pandas

from news import NewsFeed

from secret.google_app_password import USER, PASSWORD
from secret.mail_recipients import RECIPIENTS


df = pandas.read_excel('data/people.xlsx')
for index, row in df.iterrows():
    newsfeed = NewsFeed(
                        interest=row['interest'],
                        from_date='2022-09-11',
                        to_date='2022-09-12',
    )

    email = yagmail.SMTP(user=USER, password=PASSWORD)
    print(f'sending mail about "{row["interest"]}" to "{row["email"]}"')
    email.send(
        # to=RECIPIENTS,
        to=row['email'],
        subject=f'Your {row["interest"]} news for today!',
        contents=f'Hi, {row["name"]}, see what\'s on about {row["interest"]} today.\n'
                 f'{newsfeed.get_mailbody(use_cache=False)}\n'
                 f'Ardit'
    )
