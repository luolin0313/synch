# mysql2ch

![pypi](https://img.shields.io/pypi/v/mysql2ch.svg?style=flat)
![docker](https://img.shields.io/docker/cloud/build/long2ice/mysql2ch)
![license](https://img.shields.io/github/license/long2ice/mysql2ch)
![workflows](https://github.com/long2ice/mysql2ch/workflows/pypi/badge.svg)

[中文文档](https://blog.long2ice.cn/2020/05/mysql2ch%E4%B8%80%E4%B8%AA%E5%90%8C%E6%AD%A5mysql%E6%95%B0%E6%8D%AE%E5%88%B0clickhouse%E7%9A%84%E9%A1%B9%E7%9B%AE/)

## Introduction

Sync data from MySQL to ClickHouse, support full and increment ETL.

![mysql2ch](https://github.com/long2ice/mysql2ch/raw/master/images/mysql2ch.png)

## Features

- Full data etl and real time increment etl.
- Support DDL and DML sync, current support `add column` and `drop column` of DDL, and full support of DML also.
- Rich configurable items.

## Requirements

- [redis](https://redis.io), cache mysql binlog file and position and transfe mysql binlog event.

## Install

```shell
> pip install mysql2ch
```

## Usage

### Config

```ini
[sentry]
# sentry environment
environment = development
# sentry dsn
dsn = https://xxxxxxxx@sentry.test.com/1

[redis]
host = 127.0.0.1
port = 6379
password =
db = 0
prefix = mysql2ch

[mysql]
host = 127.0.0.1
port = 3306
user = root
password = 123456

# sync schema test from mysql
[mysql.test]
# multiple separated with comma
tables = test

[clickhouse]
host = 127.0.0.1
port = 9000
user = default
password =

[sync]
mysql_server_id = 1
init_binlog_file = binlog.000088
init_binlog_pos = 2238
# these tables skip delete,multiple separated with comma
skip_delete_tables =
# these tables skip update,multiple separated with comma
skip_update_tables =
# skip delete or update dmls,multiple separated with comma
skip_dmls =
# how many num to submit,recommend set 20000 when production
insert_num = 1
# how many seconds to submit,recommend set 60 when production
insert_interval = 1

```

### Full data etl

Maybe you need make full data etl before continuous sync data from MySQL to ClickHouse or redo data etl with `--renew`.

```shell
> mysql2ch etl -h

usage: mysql2ch etl [-h] --schema SCHEMA [--tables TABLES] [--renew]

optional arguments:
  -h, --help       show this help message and exit
  --schema SCHEMA  Schema to full etl.
  --tables TABLES  Tables to full etl,multiple tables split with comma,default read from environment.
  --renew          Etl after try to drop the target tables.
```

Full etl from table `test.test`:

```shell
> mysql2ch etl --schema test --tables test
```

### Produce

Listen all MySQL binlog and produce to kafka.

```shell
> mysql2ch produce
```

### Consume

Consume message from kafka and insert to ClickHouse,and you can skip error with `--skip-error`.

```shell
> mysql2ch consume -h

usage: mysql2ch consume [-h] --schema SCHEMA [--skip-error] [--last-msg-id LAST_MSG_ID]

optional arguments:
  -h, --help            show this help message and exit
  --schema SCHEMA       Schema to consume.
  --skip-error          Skip error rows.
  --last-msg-id LAST_MSG_ID
                        Redis stream last msg id.
```

Consume schema `test` and insert into `ClickHouse`:

```shell
> mysql2ch consume --schema test
```

## Use docker-compose(recommended)

```yaml
version: "3"
services:
  producer:
    depends_on:
      - redis
    image: long2ice/mysql2ch
    command: mysql2ch produce
    volumes:
      - ./mysql2ch.ini:/src/mysql2ch.ini
  consumer.test:
    depends_on:
      - redis
    image: long2ice/mysql2ch
    command: mysql2ch consume --schema test
    volumes:
      - ./mysql2ch.ini:/src/mysql2ch.ini
  redis:
    hostname: redis
    image: redis:latest
    volumes:
      - redis
volumes:
  redis:
```

## Optional

[Sentry](https://github.com/getsentry/sentry), error reporting, worked if set `dsn` in config.

## Communication

### QQ Group

![qq_group](https://github.com/long2ice/mysql2ch/raw/master/images/qq_group.svg)

## ThanksTo

Powerful Python IDE [Pycharm](https://www.jetbrains.com/pycharm/?from=mysql2ch) from [Jetbrains](https://www.jetbrains.com/?from=mysql2ch).

![jetbrains](https://github.com/long2ice/mysql2ch/raw/master/images/jetbrains.svg)

## License

This project is licensed under the [MIT](https://github.com/long2ice/mysql2ch/blob/master/LICENSE) License.