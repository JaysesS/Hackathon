# Hacaton)

Как запустить бд?

```sh
cd psqlltree
docker-compose up -d
```

Креды:

    - POSTGRES_USER=flash
    - POSTGRES_PASSWORD=dydka
    - POSTGRES_DB=database
    - ALLOW_EMPTY_PASSWORD=yes

Приложение разберёшься)0

Если вдруг есть ошибка с psql ltree, то

В терминале:

```sh
psql postgresql://flash:dydka@localhost:5432/database

create extension ltree;

если написать еще раз create extension ltree; то напишет, мол уже установлено.
```

Тесты:

```
python -m unittest app.tests.test_database -v
```

Прости за flask.g :hand_over_mouth:, завтра объясню :shushing_face:


## Endpoints

- *Healcheck GET /api/*


- *Structure tree GET /api/structure/*

    *Check return format :arrow_down:*

- *Get node by id GET /api/tree*

    *args: **id(int)***

    *Check return format :arrow_down:*

- *Insert node POST /api/tree*

    *json: {
        "parent_id":106,
        "name":"koban`eze"
    }*

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
                    "children": [
                        {
                            "children": [],
                            "id": 105,
                            "name": "tigers",
                            "path": "101.102.105"
                        },
                        {
                            "children": [
                                {
                                    "children": [],
                                    "id": 107,
                                    "name": "koban`eze",
                                    "path": "101.102.106.107"
                                }
                            ],
                            "id": 106,
                            "name": "bengal_tigers",
                            "path": "101.102.106"
                        }
                    ],
                    "id": 102,
                    "name": "lions",
                    "path": "101.102"
                },
                {
                    "children": [
                        {
                            "children": [],
                            "id": 104,
                            "name": "roman",
                            "path": "101.103.104"
                        }
                    ],
                    "id": 103,
                    "name": "super_cats",
                    "path": "101.103"
                }
            ],
            "id": 101,
            "name": "cats",
            "path": "101"
        }
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
        "path": "101.102.106"
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
        "path": "101.102.106.107"
    },
    "status": true
}
```