from __future__ import print_function
from flask import request
from blinker import Namespace
from . import models
from ..config import BlogSettings
import random

signals = Namespace()

post_visited = signals.signal('post-visited')
post_pubished = signals.signal('post-pubished')

# post visited signal
@post_visited.connect
def on_post_visited(sender, post, **extra):
    tracker = models.Tracker()
    tracker.post = post

    if request.headers.getlist("X-Forwarded-For"):
        tracker.ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        tracker.ip = request.remote_addr

    tracker.user_agent = request.headers.get('User-Agent')
    tracker.save()


    try:
        post_statistic = models.PostStatistics.objects().get(post=post)
    except models.PostStatistics.DoesNotExist:
        post_statistic = models.PostStatistics()
        post_statistic.post = post

        post_statistic.verbose_count_base = random.randint(500, 5000)
        post_statistic.save()

    post_statistic.modify(inc__visit_count=1)


