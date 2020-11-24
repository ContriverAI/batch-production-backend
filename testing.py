import datetime
target_date_time_ms = 1602892800000 # or whatever
base_datetime = datetime.datetime( 1970, 1, 1 )
delta = datetime.timedelta( 0, 0, 0, target_date_time_ms )
target_date = base_datetime + delta
print(target_date.date())