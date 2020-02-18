from peewee import *
import datetime

DATABASE = SqliteDatabase('tips.sqlite')

class Tip(Model):
	user = CharField()
	category = CharField()
	tip = CharField()
	description = CharField()
	time_stamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Tip], safe=True)
	print('connected to DB')
	DATABASE.close()
