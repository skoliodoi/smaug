from flask_apscheduler import APScheduler
from website.constants import *


scheduler = APScheduler()


# @scheduler.task('cron', id='task_1', minute='30', hour='23', day_of_week='*', day='*', month='*', year='*')
@scheduler.task('interval', hours=1)
def check_db_often():
    cron_updates('sm_items', db_items)
    cron_updates('sm_history', db_history)
    cron_updates('sm_paperwork', db_paperwork)


@scheduler.task('interval', hours=12)
def check_db_less_often():
    cron_updates('sm_selectables', db_collection)
    cron_updates('sm_users', db_users)
