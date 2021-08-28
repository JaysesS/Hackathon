import random
from dataclasses import asdict
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, max_error, r2_score

import consts
from dto import TaskRawData


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


def generate_dataset():
    task_list = []
    
    # 1 type
    process_name = "Заказ товара"
    task_name = "проверка склада"
    task_priority = 5
    task_var_count = 1
    task_due_minutes = 60
    owner = "BOSS"
    assigner_list = [{"name":"Соня", "dev_pos":(10, None)},
                     {"name":"Миша", "dev_pos":(10, True)},
                     {"name":"Глеб", "dev_pos":(5, None)}]

    
    for i in range(300):
        assigner = random.choice(assigner_list)
        start, due, end = get_task_dates(task_due_minutes, *assigner['dev_pos'])
        task_list.append(TaskRawData(process_name, task_name, owner, assigner['name'], start, end, due, task_priority, task_var_count))

    
    # 2 type
    process_name = "закупка"
    task_name = "Оформить заявку"
    task_priority = 5
    task_var_count = 3
    task_due_minutes = 60
    owner = "BOSS"
    assigner_list = [{"name":"Соня", "dev_pos":(10, None)},
                     {"name":"Миша", "dev_pos":(15, False)},
                     {"name":"Глеб", "dev_pos":(3, True)}]

    
    for i in range(300):
        assigner = random.choice(assigner_list)
        start, due, end = get_task_dates(task_due_minutes, *assigner['dev_pos'])
        task_list.append(TaskRawData(process_name, task_name, owner, assigner['name'], start, end, due, task_priority, task_var_count))

    # 3 type
    process_name = "информирование"
    task_name = "обзвон покупателей"
    task_priority = 4
    task_var_count = 8
    task_due_minutes = 67
    owner = "BOSS"
    assigner_list = [{"name":"Соня", "dev_pos":(13, True)},
                     {"name":"Миша", "dev_pos":(8, False)},
                     {"name":"Глеб", "dev_pos":(20, None)}]

    for i in range(300):
        assigner = random.choice(assigner_list)
        start, due, end = get_task_dates(task_due_minutes, *assigner['dev_pos'])
        task_list.append(TaskRawData(process_name, task_name, owner, assigner['name'], start, end, due, task_priority, task_var_count))
    
    # 4 type
    process_name = "договор"
    task_name = "оформление договора"
    task_priority = 6
    task_var_count = 12
    task_due_minutes = 10
    owner = "BOSS"
    assigner_list = [{"name":"Соня", "dev_pos":(3, None)},
                     {"name":"Миша", "dev_pos":(7, True)},
                     {"name":"Глеб", "dev_pos":(10, False)}]

    for i in range(300):
        assigner = random.choice(assigner_list)
        start, due, end = get_task_dates(task_due_minutes, *assigner['dev_pos'])
        task_list.append(TaskRawData(process_name, task_name, owner, assigner['name'], start, end, due, task_priority, task_var_count))
    
    return task_list


def calculate_target_with_noise(df):
    elapsed = []
    
    for row_index, row in df.iterrows():
        start_time = row.start_time
        end_time = row.end_time
        task_count_on_start = row.other_task_on_start
        # increase elapsed if task_count_on_start > 0
        elapsed.append(int((end_time - start_time).total_seconds()*(1+task_count_on_start/10)))
    return elapsed


def other_task_on_start(df):
    other_task_on_start = []

    for row_index, row in df.iterrows():
        start_time = row.start_time
        end_time = row.end_time
        assigner = row.assigner
        task_count_on_start = df[(df.assigner == assigner) & (df.start_time < start_time) & (df.end_time > end_time)].shape[0]
        other_task_on_start.append(task_count_on_start)
    return other_task_on_start


def date_preprocessing(df):
    # start day of week
    df['start_dow'] = df['start_time'].apply(lambda x: x.date().weekday())
    df['start_is_weekend'] = df['start_time'].apply(lambda x: 1 if x.date().weekday() in (5, 6) else 0)
    # due day of week
    df['due_dow'] = df['due_time'].apply(lambda x: x.date().weekday())
    df['due_is_weekend'] = df['due_time'].apply(lambda x: 1 if x.date().weekday() in (5, 6) else 0)

    return df


def fit_model(model, X_scaled, Y, split_index):
    model_mse = []
    model_mae = []
    model_me = []
    model_score = []
    for train_index, test_index in split_index:
        print("######")
        X_train, X_test = X_scaled[train_index], X_scaled[test_index]
        y_train, y_test = Y[train_index], Y[test_index]
    #     
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        model_mse.append(mean_squared_error(y_test, y_pred))
        model_mae.append(mean_absolute_error(y_test, y_pred))
        model_me.append(max_error(y_test, y_pred))
        model_score.append(model.score(X_test, y_test))
    print(f"{model}:")
    print("score:", model_score)
    print("mse:", model_mse)
    print("mae", model_mae)
    print("me", model_me)
   
    return model


def processing_val(task_set, active_task_count, model, scaler):
    task_df = pd.DataFrame.from_records([asdict(task) for task in task_set])
    task_df = date_preprocessing(task_df)
    task_df['other_task_on_start'] = active_task_count
    for sign in consts.categorial_sign:
        tmp = pd.get_dummies(task_df[sign], prefix=sign)
        task_df = pd.concat([task_df,tmp], axis=1)
    task_df = task_df.drop(columns=consts.need_drop)

    proc_vals = []
    for i, col in enumerate(model.feature_names):
        if col not in task_df:
            proc_vals.append(0)
        else:
            proc_vals.append(task_df[col].values[0])

    proc_vals = np.array(proc_vals).reshape(1, -1)

    proc_vals_scaled = scaler.transform(proc_vals)
    return proc_vals_scaled
    
    

    

        
