"""Declare all class mapping database autoscaling in mariadb and several function utility

author: cuongnb14@gmail.com
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from config import *

Base = declarative_base()
class App(Base):
	"""Mapping with table apps"""

	__tablename__ = 'apps'
	Id = Column(Integer, primary_key=True)
	app_uuid = Column(String)
	name = Column(String)
	min_instances = Column(Integer)
	max_instances = Column(Integer)
	enabled = Column(Integer)
	locked = Column(Integer)
	next_time = Column(Integer)
	policies = relationship("Policy", order_by="Policy.Id", backref="app", cascade="all, delete, delete-orphan")
	crons = relationship("Cron", order_by="Cron.Id", backref="app", cascade="all, delete, delete-orphan")
	def __repr__(self):
		return '{"Id": '+str(self.Id)+', "app_uuid": "'+str(self.app_uuid)+'","name": "'+str(self.name)+'","min_instances": '+str(self.min_instances)+',"max_instances": '+str(self.max_instances)+',"enabled": '+str(self.enabled)+',"locked": '+str(self.locked)+',"next_time": '+str(self.next_time)+'}'	

class Policy(Base):
	"""Mapping with table policies"""

	__tablename__ = 'policies'
	Id = Column(Integer, primary_key=True)
	app_uuid = Column(String, ForeignKey('apps.app_uuid'))
	policy_uuid = Column(String)
	metric_type = Column(Integer)
	upper_threshold = Column(Integer)
	lower_threshold = Column(Integer)
	instances_out = Column(Integer)
	instances_in = Column(Integer)
	cooldown_period = Column(Integer)
	measurement_period = Column(Integer)
	deleted = Column(Integer)
	def __repr__(self):
		return '{"Id": '+str(self.Id)+', "app_uuid": "'+str(self.app_uuid)+'","metric_type": '+str(self.metric_type)+',"upper_threshold": '+str(self.upper_threshold)+',"lower_threshold": '+str(self.lower_threshold)+',"instances_out": '+str(self.instances_out)+',"instances_in": '+str(self.instances_in)+',"cooldown_period": '+str(self.cooldown_period)+', "measurement_period": '+str(self.measurement_period)+', "deleted": '+str(self.deleted)+'}'

class Cron(Base):
	"""Mapping with table crons"""

	__tablename__ = 'crons'
	Id = Column(Integer, primary_key=True)
	app_uuid = Column(String, ForeignKey('apps.Id'))
	cron_uuid = Column(String)
	min_instances = Column(Integer)
	max_instances = Column(Integer)
	cron_string = Column(String)
	deleted = Column(Integer)

	def __repr__(self):
		return '{"Id": '+str(self.Id)+', "app_uuid": "'+str(self.app_uuid)+'","cron_uuid": '+str(self.cron_uuid)+',"min_instances": '+str(self.min_instances)+',"max_instances": '+str(self.max_instances)+',"cron_string": '+str(self.cron_string)+',"deleted": '+str(self.deleted)+'}'	

engine = create_engine("mysql://"+MARIADB['username']+":"+MARIADB['password']+"@"+MARIADB['host']+":"+MARIADB['port']+"/"+MARIADB['dbname'], encoding='utf-8', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def get_by_id(table_class, id):
	"""Return record of table_class have id is $id
		
	@param Base table_class Class of table. Ex: models.Apps
	@param int id id of record
	"""
	result = session.query(table_class).filter_by(Id=id).first()
	return result

def get_all(table_class):
	"""Return all record of table_class

	@param Base table_class Class of table. Ex: models.Apps
	"""
	result = session.query(table_class)
	return result

def get_app_by_appname(app_name):
	"""Return App have name is app_name
	
	@param string app_name
	@return App 
	"""
	app = session.query(App).filter_by(name=app_name).first()
	return app
		
def get_policies_of_appuuid(app_uuid):
	"""Return all policies of app_uuid
	
	@param string app_uuid
	@return iter Policy
	"""
	policies = session.query(Policy).filter_by(app_uuid=app_uuid)
	return policies

def get_policies_of_appname(app_name):
	"""Return all policies of app_name
	
	@param string app_name
	@return iter Policy
	"""
	app = session.query(App).filter_by(name=app_name).first()
	return app.policies

def add_row(table_class, data):
	"""Add a new record in table mapping with table_class
	
	@param Base table_class, ex: models.App ...
	@param dict data
	"""
	try:
		new_row = table_class()
		for key in data:
			setattr(new_row, key, data[key])
		session.add(new_row)
		session.commit()
		return True
	except Exception:
		return False

def update_app(app_name, new_data):
	app = session.query(App).filter_by(name=app_name).first()
	for key in new_data.keys():
		setattr(app, key, new_data[key])
	session.commit()

def update_pilocy(policy_uuid, new_data):
	policy = session.query(Policy).filter_by(policy_uuid=policy_uuid).first()
	for key in new_data.keys():
		setattr(policy, key, new_data[key])
	session.commit()

def update_cron(cron_uuid, new_data):
	cron = session.query(Cron).filter_by(cron_uuid=cron_uuid).first()
	for key in new_data.keys():
		setattr(cron, key, new_data[key])
	session.commit()

def delete_app_by_name(app_name):
	"""Delete app (and app's policies app's cron) have name app_app.

	@param string app_name
	"""
	app = session.query(App).filter_by(name=app_name).first()
	session.delete(app)
	session.commit()

def delete_policy_by_policy_uuid(policy_uuid):
	"""Delete policy have uuid is policy_uuid
	
	@param string policy_uuid
	"""
	policy = session.query(Policy).filter_by(policy_uuid=policy_uuid).first()
	session.delete(policy)
	session.commit()


def delete_cron_by_cron_uuid(cron_uuid):
	"""Delete cron have uuid is cron_uuid
	
	@param string cron_uuid
	"""
	cron = session.query(Cron).filter_by(cron_uuid=cron_uuid).first()
	session.delete(cron)
	session.commit()

def to_json(result):
 	"""Return json string of result query
	
 	@param Base result result query
 	@return string string json
 	"""
 	list_record = []
 	for record in result:
 		list_record.append(str(record))
 	json_record = "["+",".join(list_record)+"]"
 	return json_record
