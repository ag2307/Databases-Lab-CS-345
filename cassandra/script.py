from cassandra.cluster import Cluster
from datetime import datetime
import os
import json

cluster = Cluster()
session = cluster.connect()
session.execute("""
	CREATE KEYSPACE IF NOT EXISTS assignment
	WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
	""")
session.set_keyspace("assignment")

# i=0
tweets=[]
path='./dataset_cassandra'
for filename in os.listdir(path):
	# i=i+1
	with open(path+'/'+filename) as data_file:
		data=json.load(data_file)
		for objects in data:
			tweets.append(data[objects])

#first query
session.execute("DROP TABLE IF EXISTS query1")
session.execute("""
	CREATE TABLE query1 (
		date TEXT,
		author_id TEXT,
		tid TEXT,
		PRIMARY KEY(date,author_id,tid)
	)
	""")
for data in tweets:
	session.execute("""INSERT INTO query1(date,author_id,tid)
		VALUES (%s,%s,%s)""",
		(data['date'],data['author_id'],data['tid']))

# second query
session.execute("DROP TABLE IF EXISTS query2")
session.execute("""
	CREATE TABLE query2 (
		hashtag TEXT,
		mention TEXT,
		date TEXT,
		tid TEXT,
		PRIMARY KEY(date,mention,hashtag,tid)
	)
	""")
for data in tweets:
	if not data['hashtags']:
		continue
	for tag in data['hashtags']:
		if tag=='':
			continue
		if not data['mentions']:
			break
		for mention_name in data['mentions']:
			if mention_name=='':
				continue
			session.execute("""INSERT INTO query2(hashtag,mention,date,tid)
			VALUES (%s,%s,%s,%s)""",
			(tag,mention_name,data['date'],data['tid']))

# session.execute("""
# 	CREATE TABLE IF NOT EXISTS tweets(
# 		quote_count INT, 
# 		reply_count INT, 
# 		hashtags LIST<TEXT>, 
# 		datetime TIMESTAMP, 
# 		date TIMESTAMP, 
# 		like_count INT, 
# 		verified BOOLEAN, 
# 		sentiment INT, 
# 		author TEXT, 
# 		location TEXT, 
# 		tid TEXT, 
# 		retweet_count INT, 
# 		type TEXT, 
# 		media_list MAP<INT,frozen<MAP<TEXT,TEXT>>>, 
# 		quoted_source_id TEXT, 
# 		url_list LIST<TEXT>, 
# 		tweet_text TEXT,
# 		author_profile_image TEXT,
# 		author_screen_name TEXT, 
# 		author_id TEXT, 
# 		lang TEXT, 
# 		keywords_processed_list LIST<TEXT>, 
# 		retweet_source_id TEXT, 
# 		mentions LIST<TEXT>, 
# 		replyto_source_id TEXT,
# 		PRIMARY KEY(tid)
# 	)
# 	""")
