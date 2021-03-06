from enum import Enum


class BrokerType(str, Enum):
    redis = "redis"
    kafka = "kafka"


class SourceDatabase(str, Enum):
    mysql = "mysql"
    postgres = "postgres"


class ClickHouseEngine(str, Enum):
    merge_tree = "MergeTree"
    collapsing_merge_tree = "CollapsingMergeTree"
