import datetime


s= '.'.join(datetime.date.today().strftime("%d/%m/%Y").split('/'))
print(s)


yesterday = '.'.join((datetime.date.today() - datetime.timedelta(days=3)).strftime("%d/%m/%Y").split('/'))

print(yesterday)