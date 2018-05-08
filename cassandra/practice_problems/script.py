from cassandra.cluster import Cluster
from datetime import datetime
import os
import json

cluster = Cluster()
session = cluster.connect()
session.execute("""
	CREATE KEYSPACE IF NOT EXISTS project 
	WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
	""")
session.set_keyspace("project")

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
		author_screen_name TEXT,
		datetime TIMESTAMP,
		tid TEXT,
		tweet_text TEXT,
		author_id TEXT,
		location TEXT,
		lang TEXT,
		PRIMARY KEY(author_screen_name,datetime,tid)
	) WITH CLUSTERING ORDER BY (datetime DESC)
	""")
for data in tweets:
	session.execute("""INSERT INTO query1(author_screen_name,datetime,tid,tweet_text,author_id,location,lang)
		VALUES (%s,%s,%s,%s,%s,%s,%s)""",
		(data['author_screen_name'],data['datetime'],data['tid'],data['tweet_text'],data['author_id'],data['location'],data['lang']))

first_query_select=session.execute("""
	SELECT author,tid,tweet_text,author_id,location,lang
	FROM query1
	WHERE author='Lyn'
	""")
for row in first_query_select:
	print(row.tweet_text.encode('utf-8'))


#second query
session.execute("DROP TABLE IF EXISTS query2")
session.execute("""
	CREATE TABLE query2 (
		keyword TEXT,
		like_count INT,
		tid TEXT,
		author TEXT,
		datetime TIMESTAMP,
		tweet_text TEXT,
		PRIMARY KEY(keyword,like_count,tid)
	) WITH CLUSTERING ORDER BY (like_count DESC)
	""")
for data in tweets:
	if not data['keywords_processed_list']:
		continue
	for each in data['keywords_processed_list']:
		if each=='':
			continue
		session.execute("""INSERT INTO query2(keyword,like_count,tid,author,datetime,tweet_text)
		VALUES (%s,%s,%s,%s,%s,%s)""",
		(each,data['like_count'],data['tid'],data['author'],data['datetime'],data['tweet_text']))

#third query
session.execute("DROP TABLE IF EXISTS query3")
session.execute("""
	CREATE TABLE query3 (
		hashtag TEXT,
		datetime TIMESTAMP,
		tid TEXT,
		author TEXT,
		tweet_text TEXT,
		PRIMARY KEY(hashtag,datetime,tid)
	) WITH CLUSTERING ORDER BY (datetime DESC)
	""")
for data in tweets:
	if not data['hashtags']:
		continue
	for each in data['hashtags']:
		if each=='':
			continue
		session.execute("""INSERT INTO query3(hashtag,datetime,tid,author,tweet_text)
		VALUES (%s,%s,%s,%s,%s)""",
		(each,data['datetime'],data['tid'],data['author'],data['tweet_text']))

#fourth query
session.execute("DROP TABLE IF EXISTS query4")
session.execute("""
	CREATE TABLE query4 (
		author_name_mentioned TEXT,
		datetime TIMESTAMP,
		tid TEXT,
		author_of_the_tweet TEXT,
		tweet_text TEXT,
		PRIMARY KEY(author_name_mentioned,datetime,tid)
	) WITH CLUSTERING ORDER BY (datetime DESC)
	""")
for data in tweets:
	if not data['mentions']:
		continue
	for each in data['mentions']:
		if each=='':
			continue
		session.execute("""INSERT INTO query4(author_name_mentioned,datetime,tid,author_of_the_tweet,tweet_text)
		VALUES (%s,%s,%s,%s,%s)""",
		(each,data['datetime'],data['tid'],data['author'],data['tweet_text']))

#fifth query
session.execute("DROP TABLE IF EXISTS query5")
session.execute("""
	CREATE TABLE query5 (
		date TEXT,
		like_count INT,
		tid TEXT,
		author TEXT,
		tweet_text TEXT,
		PRIMARY KEY(date,like_count,tid)
	) WITH CLUSTERING ORDER BY (like_count DESC)
	""")
for data in tweets:
	session.execute("""INSERT INTO query5(date,like_count,tid,author,tweet_text)
	VALUES (%s,%s,%s,%s,%s)""",
	(data['date'],data['like_count'],data['tid'],data['author'],data['tweet_text']))

#sixth query
session.execute("DROP TABLE IF EXISTS query6")
session.execute("""
	CREATE TABLE query6 (
		location TEXT,
		tid TEXT,
		author TEXT,
		datetime TIMESTAMP,
		tweet_text TEXT,
		PRIMARY KEY(location,tid)
	)
	""")
for data in tweets:
	if not data['location']:
		continue
	session.execute("""INSERT INTO query6(location,tid,author,datetime,tweet_text)
	VALUES (%s,%s,%s,%s,%s)""",
	(data['location'],data['tid'],data['author'],data['datetime'],data['tweet_text']))

# seventh query
# session.execute("DROP TABLE IF EXISTS query7")
# session.execute("""
# 	CREATE TABLE query7 (
# 		date TEXT,
# 		hashtag TEXT,
# 		tid TEXT,
# 		PRIMARY KEY(date,hashtag,tid)
# 	)
# 	""")
# for data in tweets:
# 	if not data['hashtags']:
# 		continue
# 	for each in data['hashtags']:
# 		if each=='':
# 			continue
# 		session.execute("""INSERT INTO query7(date,hashtag,tid)
# 		VALUES (%s,%s,%s)""",
# 		(data['date'],each,data['tid']))
	
# eigth query
# session.execute("DROP TABLE IF EXISTS query8")
# session.execute("""
# 	CREATE TABLE query8(
# 		tid TEXT,
# 		date TEXT,
# 		datetime TIMESTAMP,
# 		author TEXT,
# 		location TEXT,
# 		lang TEXT,
# 		tweet_text TEXT,
# 		PRIMARY KEY(date,tid)
# 	)
# 	""")
# for data in tweets:
# 	session.execute("""INSERT INTO query8(tid,date,datetime,author,location,lang,tweet_text)
# 		VALUES (%s,%s,%s,%s,%s,%s,%s)""",
# 		(data['tid'],data['date'],data['datetime'],data['author'],data['location'],data['lang'],data['tweet_text']))
