from __future__ import print_function
from os import path
from data_methods.twitter_data_methods import twitter_database
from data_methods.preprocess_methods import *
from datetime import datetime
import pickle
import multiprocessing as mp

current_path = path.dirname(path.abspath(__file__))
parent_path = path.dirname(path.dirname(current_path))
db_path = path.join(parent_path, 'resources/twitter_database.db')

# parameters
query = "SELECT Date,text from Tweets WHERE followers_count > 100000 " \
        "AND DATETIME(Date) >= '2018-04-23 09:00:00' AND DATETIME(Date) <= '2018-04-27 16:00:00'"

start_time = datetime.strptime('9:30AM', '%I:%M%p').time()
end_time = datetime.strptime('4:00PM', '%I:%M%p').time()
minutes_in_day = 390
seconds_in_minute = 60

# get data from database
db = twitter_database(db_path=db_path)


# query result should be a list of (data, text)
def time_convert(x):
    time = datetime.strptime(x[0], '%Y-%m-%d %H:%M:%S')
    if time.time() < start_time:
        time = time.replace(hour=9, minute=30)
    if time.time() > end_time:
        time = time.replace(hour=16, minute=0)
    time = time.replace(second=0)
    y = [time, x[1]]
    return y


query_result = db.query(query)

# format data to a certain length list
query_result = map(time_convert, query_result)
time_series = map(lambda x: x[0], query_result)
max_time = max(time_series)
min_time = min(time_series)
time_duration = max_time - min_time
bucket_num = time_duration.days * minutes_in_day + time_duration.seconds / seconds_in_minute
bucket_num = max(bucket_num, 1)


def date_to_key(x):
    time = x[0]
    delta_date = max_time.date() - time.date()
    delta_day = delta_date.days
    delta_min = delta_date.seconds / seconds_in_minute
    key = delta_day * minutes_in_day + delta_min
    y = [key, x[1]]
    return y


query_result = map(date_to_key, query_result)
text_list = [[]] * bucket_num

for item in query_result:
    text_list[item[0]].append(item[1])

event_vectors = []
threads = mp.Pool(processes=8)
print("map working...")
text_list = threads.map(texts2vectors, text_list)
# list_len = len(text_list)
# j = 0
# for i in range(0, len(text_list)):
#     text_list[i] = p.texts2vectors(text_list[i])
#     j += 1
#     if j % 10 == 0:
#         print(str(j) + " completed")
print("map done...")
for texts in text_list:
    text_vectors = map(vectors_mean, texts)
    event_vector = vectors_mix(text_vectors)
    event_vectors.append(event_vector)
pickle.dump(event_vectors, open(path.join(parent_path, "resources/training_data/event_vectors.p"), "wb"))
