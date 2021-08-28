import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
period_days = 2


def get_global_start_end():
    t_start = datetime.now()
    t_end =  t_start + timedelta(days = period_days)
    return t_start, t_end


def generate_random_val(target, rel_dev, only_positive=None):
    sign = 1
    shift = 0
    if only_positive is None:
        shift = 0.5
    elif only_positive:
        pass
    else:
        sign = -1
        
    abs_max_dev = rel_dev * target/100
    dev = abs_max_dev * (random.gammavariate(1,3)%1 - shift) * sign
    return target + dev

def get_task_dates(due, dev, only_positive=None):
    t_start, t_end = get_global_start_end()
    while True:
        start_time = fake.date_time_between_dates(t_start, t_end)
        if 20 > start_time.hour > 6:
            due_time = start_time + timedelta(minutes=due)
            end_time = start_time + timedelta(minutes=generate_random_val(due, dev, only_positive))
            return start_time, due_time, end_time
