"""Declare all class mapping database autoscaling in mariadb and several function utility

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




