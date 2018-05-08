from flask import Flask, render_template, request
from datetime import datetime
from cassandra.cluster import Cluster
from collections import namedtuple
import operator
import os
import json

cluster = Cluster()
session = cluster.connect()
session.execute("""
	CREATE KEYSPACE IF NOT EXISTS assignment
	WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 }
	""")
session.set_keyspace("assignment")

app = Flask(__name__)

def query1(date):	
	statement = session.prepare("SELECT author_id,count(tid) FROM query1 where date = ? group by author_id,tid");
	statement1 = session.execute(statement,[date])
	mp={}
	for rows in statement1:
		if rows.author_id.encode('utf8') in mp:
			mp[rows.author_id.encode('utf8')]+=1
		else:
			mp[rows.author_id]=1
	sorted_list=sorted(mp.items(),key=operator.itemgetter(1))
	sorted_list.reverse()
	ans=""
	# ans+="<b>Number of Tweets: "+len(rows)+"</b><br><br>"
	i=0
	for row in sorted_list:
		i=i+1
		ans+="Date:&nbsp&nbsp&nbsp<b>"+ date + "</b><br>"
		ans+="Author ID:&nbsp&nbsp&nbsp<b>"+ row[0]+ "</b><br>"
		ans+="Number of times the userID has posted a tweet on that date:&nbsp&nbsp&nbsp<b>"+ str(row[1]) + "</b><br><br><br>"
		ans+="##################################################<br><br>"
	ans="<b>Date:&nbsp&nbsp&nbsp"+date+"</b><br><br>"+ans
	ans=ans+"<b>Number of Rows:&nbsp&nbsp&nbsp"+str(i)+"</b><br><br>"
	return ans

def query2(date):	
	statement = session.prepare("SELECT mention,hashtag,count(tid) FROM query2 where date = ? group by mention,hashtag,tid");
	statement1 = session.execute(statement,[date])
	mp={}
	temp={}
	for rows in statement1:
		first="z^"+rows[0]
		second="z^"+rows[1]
		trial = tuple([first,second])
		if trial in mp:
			mp[trial]+=1
		else:
			mp[trial]=1
	sorted_list=sorted(mp.items(),key=operator.itemgetter(1))
	sorted_list.reverse()
	ans=""
	# ans+="<b>Number of Tweets: "+len(rows)+"</b><br><br>"
	i=0
	for row in sorted_list:
		i=i+1
		first=row[0][0]
		second=row[0][1]
		first=(row[0][0].split('^'))[1]
		second=(row[0][1].split('^'))[1]
		ans+="Date:&nbsp&nbsp&nbsp<b>"+ date + "</b><br>"
		ans+="Mention:&nbsp&nbsp&nbsp<b>"+ first+ "</b><br>"
		ans+="Hashtag:&nbsp&nbsp&nbsp<b>"+ second + "</b><br>"
		ans+="Number of times the mention-hashtag pair is cooccurringon this date:&nbsp&nbsp&nbsp<b>"+ str(row[1]) + "</b><br><br><br>"
		ans+="##################################################<br><br>"
	ans="<b>Date:&nbsp&nbsp&nbsp"+date+"</b><br><br>"+ans
	ans=ans+"<b>Number of Rows:&nbsp&nbsp&nbsp"+str(i)+"</b><br><br>"
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

if __name__ == '__main__':
	app.run(debug = True)