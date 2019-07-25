'''
1153875964855648257



'''





import tweepy
import psycopg2
import time
import os


def connect_to_database():
	global c
	global con
	DATABASE_URL = os.getenv('DATABASE_URL' , 'postgresql://postgres:1234@localhost/askprocoders')
	con = psycopg2.connect(DATABASE_URL , sslmode='require')
	c = con.cursor()
	print('connected to database')


def disconnect():
	c.close()
	con.close()
	print('disconnected')




# def create_table():
# 	c.execute('''CREATE TABLE IF NOT EXISTS QA(
# 	   SNO BIGSERIAL PRIMARY KEY     NOT NULL,
# 	   ID           BIGINT    NOT NULL,
# 	   NAME            TEXT     NOT NULL,
# 	   QUESTIONS      TEXT,
# 	   ANSWERS         TEXT,
# 	   SEND            TEXT )''')
# 	con.commit()
# 	print('Table is created')


print("this bot is working")
CONSUMER_KEY = '7di1l1zH2exr1LwrlC9fbt9Fp'
CONSUMER_SECRET = 'sqwgFgssleBF7LyikH9eAjKsEsj2F2Ggqvdk3LLLqXZxFGkLsU'
ACCESS_KEY = '1132924430143905792-QQhRZjWMzEpUSbSTGXG65hBwalwz3H'
ACCESS_SECRET = 'uOg33UdvMLHwwnDgA5b1WLtoyhK7DK55ppvT5wN0Av58L'
auth = tweepy.OAuthHandler(CONSUMER_KEY , CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY , ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)



def writeMentions(user_info):
	c.execute('''INSERT INTO qa(id , name , questions) VALUES(%s , %s , %s)''' , (user_info[0] , user_info[1] ,user_info[2]))
	con.commit()
	print('inserted')




def retrieve_last_seen_id():
	c.execute('SELECT lastseen FROM lst WHERE hack = 1')
	last_seen_id = c.fetchall()[0][0]
	print(last_seen_id)
	return last_seen_id

def store_last_seen_id(last_seen_id):
	print('!')
	lst = last_seen_id
	c.execute('SELECT lastseen FROM lst WHERE hack = 1')
	if c.rowcount == 0:
		c.execute(''' INSERT INTO lst(hack , lastseen) VALUES(%s, %s)''', [1 , lst])
		con.commit()
	else:
		c.execute(''' UPDATE lst SET lastseen =(%s) WHERE hack = 1''', [lst] )
		con.commit()
	


def reply_and_store():
	last_seen_id = retrieve_last_seen_id()
	try:
		mentions = api.mentions_timeline(last_seen_id , tweet_mode = 'extended')
		print('mention incomig')
		for mention in reversed(mentions):
			print(str(mention.id) +' - '+ mention.user.screen_name +' - ' + mention.full_text)
			user_info = [mention.id , mention.user.screen_name, mention.full_text]
			writeMentions(user_info)
			last_seen_id = mention.id
			store_last_seen_id(last_seen_id)
			try:
				api.update_status('@' + mention.user.screen_name + ''' Hey There , you are doing great! You will soon have your answer here!''', mention.id)
				print('texted')
			except:
				print('not texted')


	except:
		print('not working now')

connect_to_database()
store_last_seen_id(1153875964855648257)
# create_table()
while True:
	reply_and_store()
	time.sleep(5)
disconnect()

    

