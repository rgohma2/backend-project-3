import os
from peewee import *
from flask_login import UserMixin
import datetime
from playhouse.db_url import connect

if 'ON_HEROKU' in os.environ: 
	DATABASE = connect(os.environ.get('DATABASE_URL'))                                                   # Heroku Postgres Add-on
else:
	DATABASE = SqliteDatabase('tips.sqlite')

class User(UserMixin, Model):
  email = CharField(unique=True) 
  name = CharField()
  password = CharField()

  class Meta:
  	database = DATABASE


class Tip(Model):
	creator = ForeignKeyField(User, backref='tips')
	category = CharField()
	tip = CharField()
	description = CharField()
	time_stamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

class Favorite(Model):
	user = ForeignKeyField(User, backref='favorites')
	tip = ForeignKeyField(Tip, backref='favorites')

	class Meta:
		database = DATABASE



def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Tip, Favorite], safe=True)
	print('connected to DB')
	DATABASE.close()
