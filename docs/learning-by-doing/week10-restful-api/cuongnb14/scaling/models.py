"""Declare all class mapping database autoscaling in mariadb

author: cuongnb14@gmail.com
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
class App(Base):
	"""mapping with table apps"""

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
	"""mapping with table policies"""

	__tablename__ = 'policies'
	Id = Column(Integer, primary_key=True)
	app_uuid = Column(String, ForeignKey('apps.Id'))
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
	"""mapping with table crons"""

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

engine = create_engine("mysql://autoscaling:autoscaling@123@172.17.42.1:3306/autoscaling", encoding='utf-8', echo=True)
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

def get_app_of_appname(app_name):
	app = session.query(App).filter_by(name=app_name).first()
	return app
		
def get_policies_of_appuuid(app_uuid):
	"""Return all policies of app_uuid
	
	@param string app_uuid
	"""
	policies = session.query(Policie).filter_by(app_uuid=app_uuid)
	return policies

def get_policies_of_appname(app_name):
	"""Return all policies of app_name
	
	@param string app_name
	"""
	app = session.query(App).filter_by(name=app_name).first()
	policies = session.query(Policie).filter_by(app_uuid=app.app_uuid)
	return policies

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
