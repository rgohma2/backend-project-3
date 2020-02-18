from peewee import *
from flask_login import UserMixin
import datetime

DATABASE = SqliteDatabase('tips.sqlite')

class User(UserMixin, Model):
  email = CharField(unique=True) 
  name = CharField()
  password = CharField()

  class Meta:
  	datetime = DATABASE


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
	DATABASE.create_tables([User, Tip], safe=True)
	print('connected to DB')
	DATABASE.close()
