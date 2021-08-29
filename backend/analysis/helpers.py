import random
from dataclasses import asdict
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, max_error, r2_score, mean_absolute_percentage_error

from analysis import consts
from analysis.dto import TaskRawData


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


users_pressets = {
    "Василёк": {"Фикс чего-то там": (100, True), "Оформить заявку": (100, True), "проверка склада": (100, True), "Перепиши весь десигн": (100, True), "Сделай гугл": (100, True)},
    "Петя":  {"Фикс чего-то там": (50, False), "Оформить заявку": (1000, True), "проверка склада": (500, True), "Перепиши весь десигн": (10, False), "Сделай гугл": (40, True)},
    "Глеб":  {"Фикс чего-то там": (30, False), "Оформить заявку": (400, True), "проверка склада": (600, True), "Перепиши весь десигн": (200, True), "Сделай гугл": (30, False)},
    "Соня":  {"Фикс чего-то там": (1000, True), "Оформить заявку": (50, False), "проверка склада": (50, False), "Перепиши весь десигн": (400, True), "Сделай гугл": (600, True)},
    "Ванёк":  {"Фикс чего-то там": (30, False), "Оформить заявку": (1000, True), "проверка склада": (500, True), "Перепиши весь десигн": (300, True), "Сделай гугл": (20, False)},
    "Ден":  {"Фикс чего-то там": (300, True), "Оформить заявку": (500, True), "проверка склада": (500, True), "Перепиши весь десигн": (50, False), "Сделай гугл": (500, True)},
    "Игорь":  {"Фикс чего-то там": (50, False), "Оформить заявку": (1000, True), "проверка склада": (500, True), "Перепиши весь десигн": (200, True), "Сделай гугл": (10, False)},
    "Абстрактный тестировщик":  {"Фикс чего-то там": (10, False), "Оформить заявку": (1000, True), "проверка склада": (500, True), "Перепиши весь десигн": (400, True), "Сделай гугл": (1000, True)},
    "Еремей":  {"Фикс чего-то там": (30, False), "Оформить заявку": (1000, True), "проверка склада": (500, True), "Перепиши весь десигн": (30, False), "Сделай гугл": (400, True)},
    "Абстрактный джун питона":  {"Фикс чего-то там": (10, True), "Оформить заявку": (1000, True), "проверка склада": (1000, True), "Перепиши весь десигн": (400, True), "Сделай гугл": (500, True)},
    "Абстрактный джун JS\'a":  {"Фикс чего-то там": (30, False), "Оформить заявку": (1000, True), "проверка склада": (1000, True), "Перепиши весь десигн": (100, True), "Сделай гугл": (1000, True)},
    "Абстрактный джун devopa":  {"Фикс чего-то там": (30, False), "Оформить заявку": (1000, True), "проверка склада": (1000, True), "Перепиши весь десигн": (400, True), "Сделай гугл": (1000, True)}
}



def generate_dataset():
    task_list = []
    n_samples = 1000
    
    # 1 type
    process_name = "Поддержка"
    task_name = "Фикс чего-то там"
    task_priority = 8
    task_var_count = 2
    task_due_minutes = 60 * 3
    owner = "Василёк"
#    assigner_list = [{"name":"Еремей", "dev_pos":(30, False)},
#                     {"name":"Игорь", "dev_pos":(50, True)},
#                     {"name":"Глеб", "dev_pos":(20, False)},
#                     {"name": "Абстрактный джун питона", "dev_pos": (30, True)}]

    
    for i in range(n_samples):
        assigner = random.choice(list(users_pressets.keys()))
        assigner_task_preset =  users_pressets.get(assigner, {}).get(task_name)
        if assigner_task_preset is None:
            assigner_task_preset = (10000, True)
        start, due, end = get_task_dates(task_due_minutes, *assigner_task_preset)
        task_list.append(TaskRawData(process_name, task_name, owner, assigner, start, end, due, task_priority, task_var_count))

    
    # 2 type
    process_name = "закупка"
    task_name = "Оформить заявку"
    task_priority = 5
    task_var_count = 1
    task_due_minutes = 60 * 4
    owner = "Василёк"
    assigner_list = [{"name":"Соня", "dev_pos":(15, False)},
                     {"name":"Ден", "dev_pos":(15, True)}]

    
    for i in range(n_samples):
        assigner = random.choice(list(users_pressets.keys()))
        assigner_task_preset =  users_pressets.get(assigner, {}).get(task_name)
        if assigner_task_preset is None:
            assigner_task_preset = (10000, True)
        start, due, end = get_task_dates(task_due_minutes, *assigner_task_preset)
        task_list.append(TaskRawData(process_name, task_name, owner, assigner, start, end, due, task_priority, task_var_count))

    # 3 type
    process_name = "Заказ товара"
    task_name = "проверка склада"
    task_priority = 7
    task_var_count = 1
    task_due_minutes = 60 * 3
    owner = "Василёк"
    assigner_list = [{"name":"Соня", "dev_pos":(20, False)},
                     {"name":"Ден", "dev_pos":(15, None)}]

    
    for i in range(n_samples):
        assigner = random.choice(list(users_pressets.keys()))
        assigner_task_preset =  users_pressets.get(assigner, {}).get(task_name)
        if assigner_task_preset is None:
            assigner_task_preset = (10000, True)
        start, due, end = get_task_dates(task_due_minutes, *assigner_task_preset)
        task_list.append(TaskRawData(process_name, task_name, owner, assigner, start, end, due, task_priority, task_var_count))
    
    # 4 type
    process_name = "Поддержка"
    task_name = "Перепиши весь десигн"
    task_priority = 9
    task_var_count = 9
    task_due_minutes = 60 * 5
    owner = "Василёк"
    assigner_list = [{"name":"Ден", "dev_pos":(30, False)},
                     {"name":"Петр", "dev_pos":(8, False)},
                     {"name":"Еремей", "dev_pos":(20, None)},
                     {"name":"Абстрактный джун JS\'a", "dev_pos": (30, True)}]

    for i in range(n_samples):
        assigner = random.choice(list(users_pressets.keys()))
        assigner_task_preset =  users_pressets.get(assigner, {}).get(task_name)
        if assigner_task_preset is None:
            assigner_task_preset = (10000, True)
        start, due, end = get_task_dates(task_due_minutes, *assigner_task_preset)
        task_list.append(TaskRawData(process_name, task_name, owner, assigner, start, end, due, task_priority, task_var_count))

    # 5 type
    process_name = "Разработка"
    task_name = "Сделай гугл"
    task_priority = 6
    task_var_count = 228
    task_due_minutes = 60 * 4
    owner = "Василёк"
    assigner_list = [{"name":"Игорь", "dev_pos":(50, False)},
                     {"name":"Абстрактный джун питона", "dev_pos":(30, True)},
                     {"name":"Глеб", "dev_pos":(10, None)}]

    for i in range(n_samples):
        assigner = random.choice(list(users_pressets.keys()))
        assigner_task_preset =  users_pressets.get(assigner, {}).get(task_name)
        if assigner_task_preset is None:
            assigner_task_preset = (10000, True)
        start, due, end = get_task_dates(task_due_minutes, *assigner_task_preset)
        task_list.append(TaskRawData(process_name, task_name, owner, assigner, start, end, due, task_priority, task_var_count))

    return task_list


def calculate_target_with_noise(df):
    elapsed = []
    
    for row_index, row in df.iterrows():
        start_time = row.start_time
        end_time = row.end_time
        task_count_on_start = row.other_task_on_start
       
        weekday_corr = 0
#        if row.start_dow in (0,4):
#            weekday_noise = random.random()
#            weekday_corr = weekday_noise if weekday_noise > 0.5 else 0 
         # increase elapsed if task_count_on_start > 0
        task_count_corr = 0
        if task_count_on_start >= 5:
            task_count_corr = task_count_on_start/10

        elapsed_with_noise = int((end_time - start_time).total_seconds()*(1 + task_count_corr)*(1 + weekday_corr))
        elapsed.append(elapsed_with_noise)
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
    model_mape = []
    print("######")
    for train_index, test_index in split_index:
        
        X_train, X_test = X_scaled[train_index], X_scaled[test_index]
        y_train, y_test = Y[train_index], Y[test_index]
    #     
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        model_mse.append(mean_squared_error(y_test, y_pred))
        model_mae.append(mean_absolute_error(y_test, y_pred))
        model_me.append(max_error(y_test, y_pred))
        model_score.append(model.score(X_test, y_test))
        model_mape.append(mean_absolute_percentage_error(y_test, y_pred))
    print(f"{model}:")
    print("score:", model_score)
    print("mse:", model_mse)
    print("mae", model_mae)
    print("me", model_me)
    print("mape", model_mape)
   
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
