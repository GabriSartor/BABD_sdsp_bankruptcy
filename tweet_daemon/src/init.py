import os
MONGO_PYTHON_DAEMON_USERNAME = os.environ['MONGO_PYTHON_DAEMON_USERNAME']
MONGO_PYTHON_DAEMON_PASSWORD = os.environ['MONGO_PYTHON_DAEMON_PASSWORD']
MONGO_INITDB_DATABASE = os.environ['MONGO_INITDB_DATABASE']
DEV_MODE = os.environ['DEV_MODE']

import pandas as pd

# FOR TESTING NROW MAX
import random
print("Reading csv ..")
print(os.listdir('/usr/app/data/init'))
file_list = [name for name in os.listdir('/usr/app/data/init')]
print("Found {} files".format(len(file_list)))
df_list = list()

for file in file_list:
    print("Reading {} ..".format(file))
    df_list.append(pd.read_csv('/usr/app/data/init/{}'.format(file)))

print("CSVs have been read")
print("Number of files: {}".format(len(df_list)))

if DEV_MODE:
    print("Sampling 500.000 tweets ....")
    df_list = random.sample (df_list, 10)

df = pd.concat(df_list, axis=0)

print("Dropping Flag column ...")
df = df.drop(columns=['Flag'])
print("Formatting date ...")
df['DateTime'] = df['DateTime'].str.replace("PDT", "-0700", regex=True)
df['DateTime'] = pd.to_datetime(df['DateTime'], format="%a %b %d %H:%M:%S %z %Y")
my_list = df.to_dict('records')

l =  len(my_list)
chunk_size = 1000
ran = range(l)
steps=list(ran[chunk_size::chunk_size])
steps.extend([l])

print("DATA SUCCESSFULLY PARSED !")
print("Number of records: {}".format(l))
print("Dimension of chunk: {}".format(chunk_size))
print("Number of steps: {}".format(len(steps)))

from pymongo import MongoClient
from time import sleep
sleep(10)
print("Trying to connect to Localhost")
print("User: {} pass: {} and db {}".format(MONGO_PYTHON_DAEMON_USERNAME, MONGO_PYTHON_DAEMON_PASSWORD, MONGO_INITDB_DATABASE))

client = MongoClient('mongo',
                      username=MONGO_PYTHON_DAEMON_USERNAME,
                      password=MONGO_PYTHON_DAEMON_PASSWORD,
                      authSource=MONGO_INITDB_DATABASE,
                      authMechanism='SCRAM-SHA-1')

db = client[MONGO_INITDB_DATABASE]
collection = db['tweets']
# To write
collection.delete_many({})  # Destroy the collection

# Inser chunks of the dataframe
i = 0
for j in steps:
    print("{:4.2f}%".format(j/l*100))
    collection.insert_many(my_list[i:j]) # fill de collection
    i = j

print('Done')
