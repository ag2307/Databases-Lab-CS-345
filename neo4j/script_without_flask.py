import os
import requests
import json
from py2neo import Graph
from py2neo import Path, authenticate

authenticate("localhost:7474", "neo4j", "'")
graph=Graph()
tx = graph.begin()
tx.evaluate("match(n) detach delete n")
tx.commit()

tx=graph.begin()

try:
	tx.evaluate( "CREATE CONSTRAINT ON (t:Tweet) ASSERT t.id IS UNIQUE;")
	tx.evaluate( "CREATE CONSTRAINT ON (u:User) ASSERT u.screen_name IS UNIQUE;")
	tx.evaluate( "CREATE CONSTRAINT ON (h:Hashtag) ASSERT h.tag IS UNIQUE;")
except:
	pass
tx.commit()

add_user="""
	merge(user:User{screen_name:{author_screen_name}})
	set user.id={author_id},
		user.name={author},
		user.profile_image={author_profile_image}
"""

add_tweet="""
	merge(tweet:Tweet{id:{tid}})
	set tweet.quote_count={author_id},
		tweet.reply_count={author},
		tweet.datetime={datetime},
		tweet.location={location},
		tweet.language={lang},
		tweet.date={date},
		tweet.like_count={like_count},
		tweet.verified={verified},
		tweet.sentiment={sentiment},
		tweet.retweet_count={retweet_count},
		tweet.type={type},
		tweet.url_list={url_list},
		tweet.tweet_text={tweet_text}
"""
add_hashtag="""
	merge(tag:Hashtag{tag:{hashtag}})
"""

add_user_tweet_rel="""
	match (u:User),(t:Tweet)
	where u.screen_name={author_screen_name} and t.id={tid}
	create (u)-[p:posts]->(t)
	create (u)<-[b:by]-(t)
"""

add_hashtag_tweet_rel="""
	match (h:Hashtag),(t:Tweet)
	where h.tag={hashtag} and t.id={tid}
	create (h)-[i:in]->(t)
	create (h)<-[c:contains]-(t)
"""

match_mention_name="""
	match (u:User)
	where u.screen_name={name}
	return u
"""
create_mention_name="""
	create (u:User{screen_name:{name}})
"""
add_mention_rel="""
	match (u:User),(t:Tweet)
	where u.screen_name={name} and t.id={tid}
	create (t)-[m:mentions]->(u)
"""
match_quote_id="""
	match (t:Tweet)
	where t.id={quoted_source_id}
	return t
"""
create_quote_id="""
	create (t:Tweet{id:{quoted_source_id}})
"""

add_quote_rel="""
	match (t1:Tweet),(t2:Tweet)
	where t1.id={tid} and t2.id={quoted_source_id}
	create (t1)-[q:quotes]->(t2)
"""

match_reply_id="""
	match (t:Tweet)
	where t.id={replyto_source_id}
	return t
"""
create_reply_id="""
	create (t:Tweet{id:{replyto_source_id}})
"""

add_reply_rel="""
	match (t1:Tweet),(t2:Tweet)
	where t1.id={tid} and t2.id={replyto_source_id}
	create (t1)-[q:replies]->(t2)
"""

match_retweet_id="""
	match (t:Tweet)
	where t.id={retweet_source_id}
	return t
"""
create_retweet_id="""
	create (t:Tweet{id:{retweet_source_id}})
"""

add_retweet_rel="""
	match (t1:Tweet),(t2:Tweet)
	where t1.id={tid} and t2.id={retweet_source_id}
	create (t1)-[q:retweets]->(t2)
"""

j=0
path='.'
filename='dataset.json'
print(filename)
with open(path+'/'+filename) as data_file:
	data=json.load(data_file)
	tx=graph.begin()
	for objects in data:
		j=j+1
		tweet=data[objects]
		print(j)

		tx.evaluate(add_user,tweet)
		tx.evaluate(add_tweet,tweet)

		if tweet["hashtags"]:
			for each in tweet["hashtags"]:
				tx.evaluate(add_hashtag,{'hashtag':each})
				tx.evaluate(add_hashtag_tweet_rel,{'hashtag':each,'tid':tweet["tid"]})

		tx.evaluate(add_user_tweet_rel,tweet)

		if tweet["mentions"]:
			for each in tweet["mentions"]:
				if not tx.evaluate(match_mention_name,{'name':each}):
					tx.evaluate(create_mention_name,{'name':each})
				tx.evaluate(add_mention_rel,{'name':each,'tid':tweet["tid"]})

		if tweet["quoted_source_id"]:
			if not tx.evaluate(match_quote_id,tweet):
				tx.evaluate(create_quote_id,tweet)
			tx.evaluate(add_quote_rel,tweet)

		if tweet["replyto_source_id"]:
			if not tx.evaluate(match_reply_id,tweet):
				tx.evaluate(create_reply_id,tweet)
			tx.evaluate(add_reply_rel,tweet)

		if tweet["retweet_source_id"]:
			if not tx.evaluate(match_retweet_id,tweet):
				tx.evaluate(create_retweet_id,tweet)
			tx.evaluate(add_retweet_rel,tweet)

	tx.commit()

print(json.dumps(graph.data("match (u1:User)-[:posts]->(t:Tweet)-[:mentions]->(u2:User) where u2.screen_name={name} return u2.screen_name as User_Mention,u1.screen_name as User_Mentioning_User_Mention,count(t.id) as count order by count desc limit 2",{'name':'narendramodi'})))
print()
print(json.dumps(graph.data("match (u1:User)-[:posts]->(t:Tweet)-[:replies]->(t1:Tweet)-[:by]->(u2:User) where u2.screen_name={name} return u2.screen_name as User1,collect(t1.id) as Tweet_id_of_tweet_posted_by_user1,u1.screen_name as User_Replying_to_this_Tweet,collect(t.id) as Tweet_id_of_the_replies,count(t.id) as count order by count desc",{'name':'SrBachchan'})))
print()