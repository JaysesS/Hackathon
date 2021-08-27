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