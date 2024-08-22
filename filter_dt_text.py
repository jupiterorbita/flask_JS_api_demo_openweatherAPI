import pprint
from datetime import datetime, timezone
import pytz # convert to local time
from forecast_list_data import response as response_list

# Example response (simplified)
# response = {
#     "list": [
#         {"dt": 1661871600, "other_data": "value1"},
#         {"dt": 1661914800, "other_data": "value2"},
#         {"dt": 1661958000, "other_data": "value3"},
#         # ... more items
#     ]
# }

# pprint.pprint(response_list)

# -----------------------------------------------------------------
# Function to check if time is between 8:00 AM and 10:00 AM
# def convert_to_short_time(unix_timestamp):
#     dt_object = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
#     print(dt_object)
#     return dt_object.strftime('%A, %d %B %I:%M %p UTC')
#     # return dt_object.strftime('%Y-%m-%d UTC')
#     # return dt_object.strftime('%Y-%m-%d %H:%M:%S UTC')

# # Loop through the list and print the timestamps in short format
# for item in response_list['list']:
#     short_time = convert_to_short_time(item['dt'])
#     print(f"Timestamp: {short_time}, Other Data: blah blah")
#     # print(f"Timestamp: {short_time}, Other Data: {item['other_data']}")
# -----------------------------------------------------------------


def convert_to_local_time(unix_timestamp, local_timezone):
    # Convert UNIX timestamp to UTC datetime
    utc_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
    # Convert UTC time to the specified local timezone
    local_time = utc_time.astimezone(pytz.timezone(local_timezone))
    return local_time.strftime('%A, %d %B %I:%M %p')

# Choose your local timezone, e.g., 'America/New_York'
local_timezone = 'America/New_York'

# Convert all times in the response to local time
for item in response_list['list']:
    item['local_time'] = convert_to_local_time(item['dt'], local_timezone)
    print(item['local_time'])





