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
	#policies = relationship("Policie", order_by="Policie.Id", backref="app")
	#crons = relationship("Cron", order_by="Cron.Id", backref="app")
	def __repr__(self):
		return '{"Id": '+str(self.Id)+', "app_uuid": "'+str(self.app_uuid)+'","name": "'+str(self.name)+'","min_instances": '+str(self.min_instances)+',"max_instances": '+str(self.max_instances)+',"enabled": '+str(self.enabled)+',"locked": '+str(self.locked)+',"next_time": '+str(self.next_time)+'}'	

class Policie(Base):
	"""Mapping with table policies"""

	__tablename__ = 'policies'
	Id = Column(Integer, primary_key=True)
	app_uuid = Column(String, ForeignKey('apps.Id'))
	policy_uuid = Column(String)
	metric_type = Column(Integer)
	upper_threshold = Column(Integer)
	lower_threshold = Column(Integer)
	instances_out = Column(Integer)
	instances_in = Column(Integer)
	cooldown_period = Column(Integer)
	measurement_period = Column(Integer)
	deleted = Column(Integer)
	#app = relationship("App", backref=backref('policies', order_by=Id))
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
	#app = relationship("App", backref=backref('crons', order_by=Id))

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
	@return iter Policie
	"""
	policies = session.query(Policie).filter_by(app_uuid=app_uuid)
	return policies

def get_policies_of_appname(app_name):
	"""Return all policies of app_name
	
	@param string app_name
	@return iter Policie
	"""
	app = session.query(App).filter_by(name=app_name).first()
	policies = session.query(Policie).filter_by(app_uuid=app.app_uuid)
	return policies

def add_app(app):
	"""Add a new record in apps table
		
	@param dict app
	@return boolean, True if success, False if else
	"""
	try:
		new_app = App()
		new_app.app_uuid = app.get("app_uuid")
		new_app.name = app.get("name")
		new_app.min_instances = app.get("min_instances")
		new_app.max_instances = app.get("max_instances")
		new_app.enabled = app.get("enabled", 0)
		new_app.locked = app.get("locked", 0)
		new_app.next_time = app.get("next_time")
		session.add(new_app)
		session.commit()
		return True
	except Exception:
		return False

def add_policie(policie):
	"""Add a new record in policies table
		
	@param dict policie
	@return boolean, True if success, False if else
	"""
	try:
		new_policie = Policie()
		new_policie.app_uuid = policie.get("app_uuid")
		new_policie.policy_uuid = policie.get("policy_uuid")
		new_policie.metric_type = policie.get("metric_type", 0)
		new_policie.upper_threshold = policie.get("upper_threshold", 0)
		new_policie.lower_threshold = policie.get("lower_threshold", 0)
		new_policie.instances_out = policie.get("instances_out", 0)
		new_policie.instances_in = policie.get("instances_in", 0)
		new_policie.cooldown_period = policie.get("cooldown_period", 0)
		new_policie.measurement_period = policie.get("measurement_period", 0)
		new_policie.deleted = policie.get("deleted", 0)
		session.add(new_policie)
		session.commit()
		return True
	except Exception:
		return False

def add_cron(cron):
	"""Add a new record in crons table
		
	@param dict cron
	@return boolean, True if success, False if else
	"""
	try:
		new_cron = Cron()
		new_cron.app_uuid = cron.get("app_uuid")
		new_cron.cron_uuid = cron.get("cron_uuid")
		new_cron.min_instances = cron.get("min_instances", 0)
		new_cron.max_instances = cron.get("max_instances", 0)
		new_cron.cron_string = cron.get("cron_string", "")
		new_cron.deleted = cron.get("deleted", 0)
		session.add(new_cron)
		session.commit()
		return True
	except Exception:
		return False

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
