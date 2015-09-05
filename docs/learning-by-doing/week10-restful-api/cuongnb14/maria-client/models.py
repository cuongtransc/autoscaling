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
		return '{"Id": '+str(self.Id)+', "app_uuid": "'+str(self.app_uuid)+'","name": '+str(self.name)+',"min_instances": '+str(self.min_instances)+',"max_instances": '+str(self.max_instances)+',"enabled": '+str(self.enabled)+',"locked": '+str(self.locked)+',"next_time": '+str(self.next_time)+'}'	

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

def get_policie(id):
	"""Return policie have id = id
	
	@param Integer id
	@return Policie
	"""
	policie = session.query(Policie).filter_by(Id=id).first() 
	return policie

def get_app(id):
	"""Return app have id = id
	
	@param Integer id
	@return App
	"""
	app = session.query(App).filter_by(Id=id).first() 
	return app

def get_cron(id):
	"""Return cron have id = id
	
	@param Integer id
	@return Cron
	"""
	cron = session.query(Cron).filter_by(Id=id).first() 
	return cron
		
def get_policies():
	"""Return all policies"""
	policies = session.query(Policie)
	return policies

def get_apps():
	"""Return all apps"""
	apps = session.query(App)
	return apps

def get_crons():
	"""Return all crons"""
	apps = session.query(Cron)
	return apps
