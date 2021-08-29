# Hacaton)

Start db:

```sh
cd psqlltree
docker-compose up -d
```

Start app:

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run.py
```


Если вдруг есть ошибка с psql ltree, то

В терминале:

```sh
psql postgresql://flash:dydka@localhost:5432/database

create extension ltree;

если написать еще раз create extension ltree; то напишет, мол уже установлено.
```

Тесты:

Можно использовать для заливки тестовыми данными.

```
python -m unittest app.tests.test_database -v
```


## Endpoints

- *Healcheck GET /api/*

- *Structure tree GET /api/structure/*

    - *args: **flat(bool)** - Optional*
        
        - *With **flat=True** return list of users*
        - *With **flat=None or False** return json format tree*

    - *Check return format :arrow_down:*

- *Get node by id GET /api/tree*

    - *args: **id(int)***

    - *Check return format :arrow_down:*

- *Insert node POST /api/tree*

    - args: *json: { "**parent_id**":106 "**name**":"Кобанчик", "**position**":"Помогатор"}*

    *Check return format :arrow_down:*

- *Delete node by id GET /api/tree*

    - *args: **id(int)***

    - *Return*

    ```json
    {
        "message": "Node was removed",
        "node_id": 19, // id удалённой ноды
        "status": true
    }
    ```

- *Get task GET /api/task*

    - args: **Опционально** фильтрация по..
        - **id(int)**
        - **process_name(str)** 
        - **owner_id(int)**
        - **assigner_id(int)**
        - **started(bool)**
        
    example:

        /api/task?process_name=Поддержка&id=1
        
        Отфильтровать по "process_name" и "id".


    *Check return format :arrow_down:*

- *Send task POST /api/task*

    - *json:*
    ```json
    {   
        "name": str,
        "process_name": str,
        "start_time": int,
        "due_time": int,
        "owner_id": int, // Кто ставит задачу
        "assigner_id": int, // Кому ставит
        "priority": int, 
        "var_count": int
    }
    ```

    - *Return*

    ```json
    {
        "status": true,
        "task_id": 5 // new task id
    }
    ```

- *Delete task DELETE /api/task*

    - *args: **id(int)***

    - *Return*

    ```json
    {
        "message": "Was removed",
        "status": true,
        "task_id": 6 // id удалённой задачи
    }
    ```


- *Action with task POST /api/task/manage*

    Change state task: start or stop
    Change assigner or owner
    - *json:*
    ```json
        {   
            "id": int, // required task id
            "assigner_id": int, // optional
            "owner_id": int, // optional
            "state" : "start" or "stop" // optional
        }
    ```

    *Check return format :arrow_down:*

**Structure tree** return:

    Query: /api/structure/

```json
{
    "status": true,
    "tree": [
        {
            "children": [
                {
                    "children": [],
                    "id": 3,
                    "name": "Костя",
                    "path": "1.3",
                    "position": "Архитектор",
                    "task_count": 1
                },
                {
                    "children": [],
                    "id": 2,
                    "name": "Петя",
                    "path": "1.2",
                    "position": "Фронт",
                    "task_count": 2
                },
                {
                    "children": [],
                    "id": 4,
                    "name": "Катя",
                    "path": "1.4",
                    "position": "Маркетинг",
                    "task_count": 4
                },
                {
                    "children": [
                        {
                            "children": [],
                            "id": 12,
                            "name": "Абстрактный джун devopa",
                            "path": "1.5.12",
                            "position": "devOPs",
                            "task_count": 0
                        }
                    ],
                    "id": 5,
                    "name": "Ванёк",
                    "path": "1.5",
                    "position": "devOps",
                    "task_count": 0
                },
                {
                    "children": [],
                    "id": 6,
                    "name": "Ден",
                    "path": "1.6",
                    "position": "Десигн",
                    "task_count": 0
                }
            ],
            "id": 1,
            "name": "Василёк",
            "path": "1",
            "position": "Директор",
            "task_count": 1
        }
    ]
}
```

    Query: /api/structure/flat=true

```json
{
    "status": true,
    "users": [
        {
            "id": 1,
            "name": "Кирилл А.Э.",
            "path": "1",
            "task_count": 1
        },
        {
            "id": 3,
            "name": "Роман Д.Д.",
            "path": "1.3",
            "task_count": 0
        },
        {
            "id": 7,
            "name": "Владислав В.К.",
            "path": "1.3.7",
            "task_count": 1
        },
        ...
    ]
}
```

**Get node by id** return:

    Query: /api/tree?id=106

```json
{
    "node": {
        "children": [],
        "id": 106,
        "name": "bengal_tigers",
        "path": "101.102.106",
        "task_count": 2
    },
    "status": true
}
```

**Insert node by id** return:

    Json: {
        "parent_id":106,
        "name":"koban`eze"
    }

```json
{
    "node": {
        "children": [],
        "id": 107,
        "name": "koban`eze",
        "path": "101.102.106.107",
        "task_count": 0
    },
    "status": true
}
```


**Get task with filter** return:

    Query: /api/task?process_name=Поддержка&id=1

```json
{
    "status": true,
    "tasks": [
        {
            "assigner_id": 19,
            "due_time": 1630200384,
            "end_time": 1630193184,
            "id": 1,
            "name": "Фикс чего-то там",
            "owner_id": 13,
            "priority": 75,
            "process_name": "Поддержка",
            "start_time": 1630171584,
            "started": false,
            "var_count": 2
        }
    ]
}
```


**Action with task** return:

    Json: {
        "id": 4,
        "assigner_id": 10,
        "owner_id": 7
    }

```json
{
    "status": true,
    "task": {
        "assigner_id": 10,
        "due_time": 1630185413,
        "end_time": 1630183613,
        "id": 4,
        "name": "Нарисуй красиво",
        "owner_id": 7,
        "priority": 20,
        "process_name": "Сбор урожая",
        "start_time": 1630181813,
        "started": false,
        "var_count": 1
    }
}
```

