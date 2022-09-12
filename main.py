import yagmail
import pandas

from news import NewsFeed

from secret.google_app_password import USER, PASSWORD
# from secret.mail_recipients import RECIPIENTS

#
# !!!open dropmail.me and update xlsx!!!
#
df = pandas.read_excel('data/people.xlsx')                      # !!!open dropmail.me and update xlsx!!!
for index, row in df.iterrows():                                # loop through rows of xlsx
    newsfeed = NewsFeed(                                        # for each row create a newsapi request
                        interest=row['interest'],
                        from_date=NewsFeed.yesterday(),
                        to_date=NewsFeed.today(),
    )

    email = yagmail.SMTP(user=USER, password=PASSWORD)          # connect to gmail sender
    print(
        f'{"MAIN":<14.14} | sending mail :'
        f'MAIN | about "{row["interest"]}" '
        f'MAIN | to "{row["name"]}"'
        f'MAIN | at "{row["email"]}"'
    )

    mailbody = newsfeed.get_mailbody(use_cache=False)
    email.send(                                                 # send newsletter
        to=row['email'],
        subject=f'Your {row["interest"]} news for today!',
        contents=f'Hi, {row["name"]}, see what\'s on about {row["interest"]} today.\n'
                 f'{mailbody}\n'
                 f'Ardit'
    )
