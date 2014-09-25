from __future__ import absolute_import

from celery.task.base import periodic_task
from celery.schedules import crontab

from app.domain.authenticator import Authenticator
from app.domain.topicConfiguration import TopicConfiguration
from app.domain.digger import Digger

import time, datetime

@periodic_task(run_every=crontab(minute="*"))
def digger(count=100):
	print "Start Digger on " +time.strftime("%d/%m/%Y") + " at " +time.strftime("%H:%M:%S")
	a = Authenticator()
	d = Digger(a.authenticate())
	d.topic.saveConfiguration("Deporte","premierLeague")
	d.start = datetime.datetime.now().replace(microsecond=0)
	d.startStreaming()
	
	print "End Digger on " +time.strftime("%d/%m/%Y") + " at " +time.strftime("%H:%M:%S")
	return "Finished"
