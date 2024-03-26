# -*- coding: UTF-8 -*-
from .core import SO
from .table import Table


class Database(SO):
    def __init__(self, name: str, conn):
        self._name = name
        self._conn = conn
        self._cursor = conn.cursor()

    @property
    def tables(self):
        """
        查询数据库下数据表名称
        :return: 数据表名称列表
        """
        self._execute(f"USE {self._name}")
        self._execute("SHOW TABLES")
        tbs = self._cursor.fetchall()
        return [x[0] for x in tbs]

    @property
    def desc(self):
        """
        获取数据库结构
        :return: 连接信息
        """
        sql = f"SELECT * FROM information_schema.TABLES WHERE TABLE_SCHEMA = '{self._name}'"
        self._execute(sql)
        return {x[2]: {"engine": x[4], "collate": x[-4]} for x in self._cursor.fetchall()}

    def __getitem__(self, name: str) -> Table:
        return Table(self._name + "." + name, self._conn)

    def __delitem__(self, name: str):
        self._drop(name)

    def __len__(self):
        return len(self.tables)

    def __str__(self):
        return f"<DBSO.Database>"

    def _drop(self, name: str):
        """
        删除数据表
        :param name: 数据表名
        """
        self._execute(f"DROP TABLE [IF EXISTS] {name}")

    def create(self, name: str, title: list, auto: int = 0, engine: str = "", charset: str = ""):
        """
        创建数据表
        :param name: 数据表名称
        :param title: 字段列表
        :param engine: 存储引擎
        :param charset: 默认字符集
        :param auto: 自动增长初始值
        :return: 数据表对象
        """
        sql = f"CREATE TABLE IF NOT EXISTS {self._name}.{name}({','.join([col.sql for col in title])})"
        sql += f"ENGINE={engine}" if engine else ""
        sql += f" AUTO_INCREMENT={auto}" if auto else ""
        sql += f" DEFAULT CHARSET={charset}" if charset else ""
        self._execute(sql)
        return self[name]

    def rename(self, name: str):
        """
        重命名数据库(仅支持 MySQL 5.1.23及以前版本)
        :param name: 名称
        """
        sql = f"ALTER DATABASE {self._name} RENAME TO {name}"
        self._execute(sql)
