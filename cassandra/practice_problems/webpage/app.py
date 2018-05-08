from flask import Flask, render_template, request
from datetime import datetime
from cassandra.cluster import Cluster
import os
import json

cluster = Cluster()
session = cluster.connect('project')

app = Flask(__name__)

def query1(author):
	statement = session.prepare("SELECT * FROM query1 where author_screen_name = ?");
	rows = session.execute(statement,[author])
	ans=""
	# ans+="<b>Number of Tweets: "+len(rows)+"</b><br><br>"
	i=0
	for row in rows:
		i=i+1
		ans+="Author Screen Name:&nbsp&nbsp&nbsp<b>"+ row.author_screen_name + "</b><br>"
		ans+="Tweet ID:&nbsp&nbsp&nbsp<b>"+ row.tid + "</b><br>"
		ans+="DateTime:&nbsp&nbsp&nbsp<b>"+ str(row.datetime) + "</b><br>"
		ans+="Tweet Text:&nbsp&nbsp&nbsp<b>"+ row.tweet_text + "</b><br>"
		ans+="Author ID:&nbsp&nbsp&nbsp<b>"+ row.author_id + "</b><br>"
		ans+="Location:&nbsp&nbsp&nbsp<b>"+ row.location + "</b><br>"
		ans+="Language:&nbsp&nbsp&nbsp<b>"+ row.lang + "</b><br><br>"
		ans+="##################################################<br><br>"
	ans="<b>	Number of Tweets: "+str(i)+"</b><br><br>"+ans
	return ans

def query2(keyword):
	statement = session.prepare("SELECT * FROM query2 where keyword = ?");
	rows = session.execute(statement,[keyword])
	ans=""
	# ans+="<b>Number of Tweets: "+len(rows)+"</b><br><br>"
	i=0
	for row in rows:
		i=i+1
		ans+="Keyword:&nbsp&nbsp&nbsp<b>"+ row.keyword + "</b><br>"
		ans+="Tweet ID:&nbsp&nbsp&nbsp<b>"+ row.tid + "</b><br>"
		ans+="Like Count:&nbsp&nbsp&nbsp<b>"+ str(row.like_count) + "</b><br>"
		ans+="DateTime:&nbsp&nbsp&nbsp<b>"+ str(row.datetime) + "</b><br>"
		ans+="Author:&nbsp&nbsp&nbsp<b>"+ row.author + "</b><br>"
		ans+="Tweet Text:&nbsp&nbsp&nbsp<b>"+ row.tweet_text + "</b><br><br>"
		ans+="##################################################<br><br>"
	ans="<b>	Number of Tweets: "+str(i)+"</b><br><br>"+ans
	return ans

def query3(hashtag):
	statement = session.prepare("SELECT * FROM query3 where hashtag = ?");
	rows = session.execute(statement,[hashtag])
	ans=""
	# ans+="<b>Number of Tweets: "+len(rows)+"</b><br><br>"
	i=0
	for row in rows:
		i=i+1
		ans+="Hashtag:&nbsp&nbsp&nbsp<b>"+ row.hashtag + "</b><br>"
		ans+="Tweet ID:&nbsp&nbsp&nbsp<b>"+ row.tid + "</b><br>"
		ans+="DateTime:&nbsp&nbsp&nbsp<b>"+ str(row.datetime) + "</b><br>"
		ans+="Author:&nbsp&nbsp&nbsp<b>"+ row.author + "</b><br>"
		ans+="Tweet Text:&nbsp&nbsp&nbsp<b>"+ row.tweet_text + "</b><br><br>"
		ans+="##################################################<br><br>"
	ans="<b>	Number of Tweets: "+str(i)+"</b><br><br>"+ans
	return ans

def query4(author_screen_name):
	statement = session.prepare("SELECT * FROM query4 where author_name_mentioned = ?");
	rows = session.execute(statement,[author_screen_name])
	ans=""
	# ans+="<b>Number of Tweets: "+len(rows)+"</b><br><br>"
	i=0
	for row in rows:
		i=i+1
		ans+="Mentioned Author Screen Name:&nbsp&nbsp&nbsp<b>"+ row.author_name_mentioned + "</b><br>"
		ans+="Tweet ID:&nbsp&nbsp&nbsp<b>"+ row.tid + "</b><br>"
		ans+="DateTime:&nbsp&nbsp&nbsp<b>"+ str(row.datetime) + "</b><br>"
		ans+="Author of the Tweet:&nbsp&nbsp&nbsp<b>"+ row.author_of_the_tweet + "</b><br>"
		ans+="Tweet Text:&nbsp&nbsp&nbsp<b>"+ row.tweet_text + "</b><br><br>"
		ans+="##################################################<br><br>"
	ans="<b>	Number of Tweets: "+str(i)+"</b><br><br>"+ans
	return ans

def query5(date):
	statement = session.prepare("SELECT * FROM query5 where date = ?");
	rows = session.execute(statement,[date])
	ans=""
	# ans+="<b>Number of Tweets: "+len(rows)+"</b><br><br>"
	i=0
	for row in rows:
		i=i+1
		ans+="Date:&nbsp&nbsp&nbsp<b>"+ row.date + "</b><br>"
		ans+="Tweet ID:&nbsp&nbsp&nbsp<b>"+ row.tid + "</b><br>"
		ans+="Like Count:&nbsp&nbsp&nbsp<b>"+ str(row.like_count) + "</b><br>"
		ans+="Author:&nbsp&nbsp&nbsp<b>"+ row.author + "</b><br>"
		ans+="Tweet Text:&nbsp&nbsp&nbsp<b>"+ row.tweet_text + "</b><br><br>"
		ans+="##################################################<br><br>"
	ans="<b>	Number of Tweets: "+str(i)+"</b><br><br>"+ans
	return ans

def query6(location):
	statement = session.prepare("SELECT * FROM query6 where location = ?");
	rows = session.execute(statement,[location])
	ans=""
	# ans+="<b>Number of Tweets: "+len(rows)+"</b><br><br>"
	i=0
	for row in rows:
		i=i+1
		ans+="Location:&nbsp&nbsp&nbsp<b>"+ row.location + "</b><br>"
		ans+="Tweet ID:&nbsp&nbsp&nbsp<b>"+ row.tid + "</b><br>"
		ans+="DateTime:&nbsp&nbsp&nbsp<b>"+ str(row.datetime) + "</b><br>"
		ans+="Author:&nbsp&nbsp&nbsp<b>"+ row.author + "</b><br>"
		ans+="Tweet Text:&nbsp&nbsp&nbsp<b>"+ row.tweet_text + "</b><br><br>"
		ans+="##################################################<br><br>"
	ans="<b>	Number of Tweets: "+str(i)+"</b><br><br>"+ans
	return ans

def query7(date):
	object=datetime.strptime(date,'%Y-%m-%d')
	other_dates=[object,object-timedelta(days=1),object-timedelta(days=2),object-timedelta(days=3),
	object-timedelta(days=4)object-timedelta(days=5)object-timedelta(days=6)]
	other_dates=other_dates.strftime("%Y-%m-%d")
	
	statement = session.prepare("SELECT * FROM query7 where date = ?");
	rows = session.execute(statement,[date])
	ans=""
	# ans+="<b>Number of Tweets: "+len(rows)+"</b><br><br>"
	i=0
	for row in rows:
		i=i+1
		ans+="Hashtag:&nbsp&nbsp&nbsp<b>"+ row.hashtag + "</b><br>"
		ans+="Tweet ID:&nbsp&nbsp&nbsp<b>"+ row.tid + "</b><br>"
		ans+="DateTime:&nbsp&nbsp&nbsp<b>"+ str(row.datetime) + "</b><br>"
		ans+="Author:&nbsp&nbsp&nbsp<b>"+ row.author + "</b><br>"
		ans+="Tweet Text:&nbsp&nbsp&nbsp<b>"+ row.tweet_text + "</b><br><br>"
		ans+="##################################################<br><br>"
	ans="<b>	Number of Tweets: "+str(i)+"</b><br><br>"+ans
	return ans

def query8(date):
	statement = session.prepare("DELETE FROM query8 where date = ?");
	rows = session.execute(statement,[date])
	ans=""
	# ans+="<b>Number of Tweets: "+len(rows)+"</b><br><br>"
	i=0
	for row in rows:
		i=i+1
		ans+="DateTime:&nbsp&nbsp&nbsp<b>"+ str(row.datetime) + "</b><br>"
		ans+="Tweet ID:&nbsp&nbsp&nbsp<b>"+ row.tid + "</b><br>"
		ans+="location:&nbsp&nbsp&nbsp<b>"+ str.location + "</b><br>"
		ans+="lang:&nbsp&nbsp&nbsp<b>"+ str.lang + "</b><br>"
		ans+="Author:&nbsp&nbsp&nbsp<b>"+ row.author + "</b><br>"
		ans+="Tweet Text:&nbsp&nbsp&nbsp<b>"+ row.tweet_text + "</b><br><br>"
		ans+="##################################################<br><br>"
	ans="<b>	Number of Tweets: "+str(i)+"</b><br><br>"+ans
	return ans

@app.route('/')
def student():
	return render_template('index.html')

@app.route('/',methods = ['POST','GET'])
def result():
	if request.method == 'POST':
		if request.form['submit']=='answer1':
			return query1(request.form['textbox1'])
		elif request.form['submit']=='answer2':
			return query2(request.form['textbox2'])
		elif request.form['submit']=='answer3':
			return query3(request.form['textbox3'])
		elif request.form['submit']=='answer4':
			return query4(request.form['textbox4'])
		elif request.form['submit']=='answer5':
			return query5(request.form['textbox5'])
		elif request.form['submit']=='answer6':
			return query6(request.form['textbox6'])
		elif request.form['submit']=='answer7':
			return query7(request.form['textbox7'])
		elif request.form['submit']=='answer8':
			return query8(request.form['textbox8'])

if __name__ == '__main__':
	app.run(debug = True)

match (u:User)-[posts]->(t:Tweet) 
where u.screen_name='jgirl66' 
return u.screen_name as Author,t.id as Tweet_ID;

match (u1:User)-[:posts]->(t:Tweet)-[:mentioned]->(u2:User)
where u1.screen_name='jgirl66' 
return u1.screen_name as Author,u2.screen_name as Mentioned_Author;

match(h1:Hashtag)-[:in]->(t:Tweet)-[:contains]->(h2:Hashtag)
where h1.tag<h2.tag
return count(t.id) as count,h1.tag as Tag_1,h2.tag as Tag_2
order by count desc
limit 20;

match(h1:Hashtag)-[:in]->(t:Tweet)-[:quotes]->(u1:User)
where h1.tag='Win'
return count(t.id) as count,h1.tag as Tag_1,u1.screen_name as mention
order by count desc
limit 20;