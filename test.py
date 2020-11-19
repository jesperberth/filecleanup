import time

timestamp1 = 'Tue Nov 10 11:07:03 2020'
timestamp2 = 'Thu Nov 19 11:07:03 2020'

pattern = '%a %b %d %H:%M:%S %Y'

epoch_timestamp1 = int(time.mktime(time.strptime(timestamp1, pattern)))
epoch_timestamp2 = int(time.mktime(time.strptime(timestamp2, pattern)))
print(epoch_timestamp1)
print(epoch_timestamp2)
if epoch_timestamp1 > epoch_timestamp2:
  print ("Timestamp1 is the latest")
  print(epoch_timestamp2)
else:
  print ("Timestamp2 is the latest")
  print(epoch_timestamp2)