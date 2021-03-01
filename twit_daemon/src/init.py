import os
MONGO_PYTHON_DAEMON_USERNAME = os.environ['MONGO_PYTHON_DAEMON_USERNAME']
MONGO_PYTHON_DAEMON_PASSWORD = os.environ['MONGO_PYTHON_DAEMON_PASSWORD']
MONGO_INITDB_DATABASE = os.environ['MONGO_INITDB_DATABASE']
DEV_MODE = os.environ['DEV_MODE']

import pandas as pd

# FOR TESTING NROW MAX
df = pd.read_csv("../data/init/twits.csv")

if DEV_MODE:
    df = df.sample(n=50000, random_state=1)

print("Reading csv ..")
print("Formatting date ...")

df.drop(columns=['Flag'])
df['DateTime'] = df['DateTime'].str.replace("PDT", "-0700", regex=True)
df['DateTime'] = pd.to_datetime(df['DateTime'], format="%a %b %d %H:%M:%S %z %Y")
my_list = df.to_dict('records')

l =  len(my_list)
chunk_size = 10
ran = range(l)
steps=list(ran[chunk_size::chunk_size])
steps.extend([l])

print("Date formatted and data read")
print("Number of records: {}".format(l))
print("Dimension of chunk: {}".format(chunk_size))
print("Number of steps: {}".format(len(steps)))

from pymongo import MongoClient

print("Trying to connect to Localhost")
print("User: {} pass: {} and db {}".format(MONGO_PYTHON_DAEMON_USERNAME, MONGO_PYTHON_DAEMON_PASSWORD, MONGO_INITDB_DATABASE))

client = MongoClient('mongo',
                      username=MONGO_PYTHON_DAEMON_USERNAME,
                      password=MONGO_PYTHON_DAEMON_PASSWORD,
                      authSource=MONGO_INITDB_DATABASE,
                      authMechanism='SCRAM-SHA-1')

db = client[MONGO_INITDB_DATABASE]
collection = db['TWITS']
# To write
collection.delete_many({})  # Destroy the collection

# Inser chunks of the dataframe
i = 0
for j in steps:
    print(j)
    collection.insert_many(my_list[i:j]) # fill de collection
    i = j

print('Done')
