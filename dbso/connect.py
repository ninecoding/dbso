# -*- coding: UTF-8 -*-
import pymysql
from .core import SO
from .database import Database


class Connect(SO):
    def __init__(self, host: str, username: str, password: str, port: int = 3306, charset: str = 'utf8'):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._charset = charset
        self._conn = pymysql.connect(host=host, user=username, password=password, port=port, charset=charset)
        self._cursor = self._conn.cursor()

    @property
    def state(self):
        """
        检查连接状态
        """
        try:
            self._conn.ping(reconnect=False)
        except Exception as e:
            assert e
            return False
        else:
            return True

    @property
    def databases(self):
        """
        查询连接下数据库名称
        :return: 数据库名称列表
        """
        self._execute("SHOW DATABASES")
        dbs = self._cursor.fetchall()
        return [x[0] for x in dbs]

    @property
    def desc(self):
        """
            获取连接信息
        :return: 连接信息
        """
        sql = "SELECT * FROM information_schema.SCHEMATA"
        self._execute(sql)
        return [{"database": x[1], "charset": x[2], "collate": x[3]} for x in self._cursor.fetchall()]

    @property
    def version(self):
        """
        查询服务器版本信息
        :return: 服务器版本信息
        """
        sql = "SELECT VERSION()"
        self._execute(sql)
        return self._cursor.fetchone()[0]

    @property
    def status(self):
        """
        查询服务器状态
        :return: 服务器状态
        """
        sql = "SHOW STATUS"
        self._execute(sql)
        return {x[0]: x[1] for x in self._cursor.fetchall()}

    @property
    def variables(self):
        """
        查询服务器配置变量
        :return: 服务器配置变量列表
        """
        sql = "SHOW VARIABLES"
        self._execute(sql)
        return {x[0]: x[1] for x in self._cursor.fetchall()}

    def __getitem__(self, name: str) -> Database:
        return Database(name, conn=self._conn)

    def __delitem__(self, name: str):
        self._drop(name)

    def __len__(self):
        return len(self.databases)

    def __str__(self):
        return f"<DBSO.Connect {self._host}:{self._port} {self._username}>"

    def __del__(self):
        if self.state:
            self.disconnect()

    def _drop(self, name: str):
        """
        删除数据库
        :param name: 数据库名称
        """
        self._execute(f"DROP DATABASE IF EXISTS {name}")

    def create(self, name: str, charset: str = 'utf8', collate: str = "utf8_general_ci"):
        """
        创建数据库
        :param name: 数据库名称
        :param charset: 字符集
        :param collate: 排序规则
        :return 数据库对象
        """
        self._execute(f"CREATE DATABASE IF NOT EXISTS {name} CHARACTER SET {charset} COLLATE {collate}")
        return self[name]

    def reconnect(self):
        """
        重新连接
        """
        self._conn = pymysql.connect(host=self._host, user=self._username, password=self._password,
                                     port=self._port, charset=self._charset)
        self._cursor = self._conn.cursor()

    def disconnect(self):
        """
        断开连接
        """
        self._cursor.close()
        self._conn.close()

    def cmd(self, sql: str):
        """
        执行命令并提交
        :param sql: SQL语句
        :return 命令返回结果
        """
        self._execute(sql)
        self._commit()
        return self._cursor.fetchall()

    def rollback(self):
        """
        回滚
        """
        self._conn.rollback()


def connect(host: str, username: str, password: str, port: int = 3306, charset: str = 'utf8'):
    """
    生成连接对象
    :param host: 主机名
    :param port: 端口号
    :param username: 用户名
    :param password: 密码
    :param charset: 字符集
    :return: 连接对象
    """
    return Connect(host, port, username, password, charset)
