import pandas,smtplib,random,os,sys
import datetime as dt
#info for smtp
#TODO allow the user to set these when the code is first ran
# #TODO maybe some cli functionality won't hurt (if the user wants to change his info)

smtp_server = 'smtp.gmail.com'

#secrets
my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("MY_PASSWORD")

compatible = {}

data = pandas.read_csv('birthdays.csv')
data_months = data.month.values

date = dt.datetime.now()
today = {'month':date.month,'day':date.day}

for month in data_months:
    #check if same month
    if month == today['month']:
        #check if same day
        days = data[data.month == month].day.values
        #for all compatible days
        for day in days:
            if day == today['day']:
                name = data[data.day == day].name.values #list of items
                email = data[data.day == day].email.values #list of items:
                compatible['names'] = list(name)
                compatible['emails'] = list(email)
                

random_file_nb = random.randint(1,3)
with open(f"./letter_templates/letter_{random_file_nb}.txt", 'r') as letter:
    text = letter.read()
    try:
        for name,email in zip(compatible['names'],compatible['emails']):
            new_text = text.replace('[NAME]',name)
            #start smtp send new_text as msg and use email as to_addrs
            with smtplib.SMTP(smtp_server,port=587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=email,
                    msg=f"Subject:Happy Birthday {name}\n\n"+new_text
                )
    except KeyError:
        print("No birthdays today")
        sys.exit(1)

