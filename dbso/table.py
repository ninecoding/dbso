# -*- coding: UTF-8 -*-
from .core import SO
from .core import Condition


class Table(SO):
    def __init__(self, name: str, conn):
        self._name = name
        self._conn = conn
        self._cursor = conn.cursor()

    def __getitem__(self, cond):
        return self._select(cond)

    def __setitem__(self, cond, value):
        self._update(cond, value)

    def __delitem__(self, cond):
        self._delete(cond)

    def __len__(self):
        return self.length

    def __str__(self):
        return f"<DBSO.Table>"

    @property
    def length(self):
        """
        查询数据表长度
        :return: 数据表长度
        """
        sql = f"SELECT COUNT(*) FROM {self._name}"
        self._execute(sql)
        return self._cursor.fetchone()[0]

    @property
    def index(self):
        """
        查询索引名称
        :return: 索引名称列表
        """
        sql = f"SHOW INDEX FROM {self._name}"
        self._execute(sql)
        indexes = self._cursor.fetchall()
        return [x[2] for x in indexes]

    @property
    def desc(self):
        """
        查询表结构
        :return: 表结构
        """
        sql = f"DESC {self._name}"
        self._execute(sql)
        description = {x[0]: {"type": x[1], "null": x[2], "index": x[3], "default": x[4], "extra": x[5]}
                       for x in self._cursor.fetchall()}
        return description

    @property
    def sql(self):
        """
        查询表创建语句
        :return: 表创建语句
        """
        sql = f"SHOW CREATE TABLE {self._name}"
        self._execute(sql)
        return self._cursor.fetchone()[1]

    @property
    def references(self):
        """
        查询表外键信息
        :return: 外键信息
        """
        sql = (f"SELECT COLUMN_NAME,CONSTRAINT_NAME,REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME "
               f"FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{self._name.split('.')[0]}' "
               f"AND TABLE_NAME = '{self._name.split('.')[1]}' AND REFERENCED_TABLE_NAME IS NOT NULL")
        self._execute(sql)
        return {x[1]: {"col": x[0], "referenced_table": x[2], "referenced_col": x[3]} for x in self._cursor.fetchall()}

    def _select(self, cond):
        """
        查询数据
        :param cond: 条件
        :return: 数据
        """
        sql = ""
        if isinstance(cond, str) and cond == "*":
            sql = f"SELECT * FROM {self._name}"
        elif isinstance(cond, str):
            sql = f"SELECT * FROM {self._name} WHERE {cond}"
        elif isinstance(cond, Condition):
            sql = f"SELECT {','.join(cond.cols)} FROM {self._name} {cond.sql}"
        elif isinstance(cond, list) or isinstance(cond, tuple):
            sql = f"SELECT {','.join(cond)} FROM {self._name}"
        else:
            assert "Select condition is a unknown type"
        self._execute(sql)
        return self._cursor.fetchall()

    def _update(self, cond, value_dict: dict):
        """
        更新
        :param cond: 条件
        :param value_dict: 值字典
        """
        sql = ""
        values = [name + '=\'' + value_dict[name] + "\'" for name in value_dict]
        if isinstance(cond, str) and cond == "*":
            sql = f"UPDATE {self._name} SET {','.join(values)}"
        elif isinstance(cond, str):
            sql = f"UPDATE {self._name} SET {','.join(values)} WHERE {cond}"
        elif isinstance(cond, Condition):
            sql = f"UPDATE {self._name} SET {','.join(values)} {cond.sql}"
        else:
            assert "Update condition is a unknown type"
        self._execute(sql)
        self._commit()

    def _delete(self, cond):
        """
        删除
        :param cond: 条件
        """
        sql = ""
        if isinstance(cond, str) and cond == "*":
            sql = f"DELETE FROM {self._name}"
        elif isinstance(cond, str):
            sql = f"DELETE FROM {self._name} WHERE {cond}"
        elif isinstance(cond, Condition):
            sql = f"DELETE FROM {self._name} {cond.sql}"
        else:
            assert "Delete condition is a unknown type"
        self._execute(sql)
        self._commit()

    def append(self, *args):
        """
        添加数据行
        """
        sql = f"INSERT INTO {self._name}"
        if isinstance(args[0], dict):
            row = args[0]
            values = [row[x] for x in row]
            values = [(('\'' + x + '\'') if isinstance(x, str) else str(x)) for x in values]
            sql += f"({','.join([str(x) for x in row])}) VALUES ({','.join(values)})"
        else:
            rows = [(('\'' + x + '\'') if isinstance(x, str) else str(x)) for x in args]
            rows = [('NULL' if not x else x) for x in rows]
            sql += f" VALUES ({','.join(rows)})"
        self._execute(sql)
        self._commit()

    def clear(self):
        """
        清空表
        """
        sql = f"TRUNCATE TABLE {self._name}"
        self._execute(sql)
        self._commit()

    def add(self, col):
        """
        添加字段
        :param col: 字段
        """
        sql = f"ALTER TABLE {self._name} ADD COLUMN {col.sql}"
        self._execute(sql)

    def modify(self, col):
        """
        修改数据列
        :param col: 字段
        """
        sql = f"ALTER TABLE {self._name} MODIFY COLUMN {col.sql}"
        self._execute(sql)

    def drop(self, col_name: str):
        """
        删除数据列
        :param col_name: 字段名
        """
        sql = f"ALTER TABLE {self._name} DROP COLUMN {col_name}"
        self._execute(sql)

    def primary(self, col_name: str):
        """
        设置主键约束
        :param col_name: 字段名
        """
        sql = f"ALTER TABLE {self._name} ADD PRIMARY KEY ({col_name})"
        self._execute(sql)

    def foreign(self, constraint_name: str, col_name: str, foreign_table_name: str, foreign_col_name: str):
        """
        设置外键约束
        :param constraint_name: 约束名
        :param col_name: 字段名
        :param foreign_table_name: 外键表名
        :param foreign_col_name: 外键字段名
        """
        sql = (f"ALTER TABLE {self._name} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({col_name}) "
               f"REFERENCES {self._name.split('.')[0] + '.' + foreign_table_name} ({foreign_col_name})")
        self._execute(sql)

    def drop_foreign(self, constraint_name: str):
        """
        删除外键约束
        :param constraint_name: 外键约束名
        """
        sql = f"ALTER TABLE {self._name} DROP FOREIGN KEY {constraint_name}"
        self._execute(sql)

    def rename(self, name: str, new_name: str = ""):
        """?
        重命名数据表或字段
        :param name: 表新名称或字段名称
        :param new_name: 字段新名称
        """
        if not new_name:
            sql = f"ALTER TABLE {self._name} RENAME TO {self._name.split('.')[0]}.{name}"
        else:
            col_type = self.desc[name]['type']
            sql = f"ALTER TABLE {self._name} CHANGE COLUMN {name} {new_name} {col_type}"
        self._execute(sql)

    def create_index(self, name: str, col_dict: dict, unique: bool = False):
        """
        创建索引
        :param name: 索引名称
        :param col_dict: 字段字典
        :param unique: 是否唯一
        """
        sql = (f"CREATE {'UNIQUE ' if unique else ''}INDEX {name} ON "
               f"{self._name} ({','.join([x + ' ' + col_dict[x] for x in col_dict])})")
        self._execute(sql)

    def drop_index(self, name: str):
        """
        删除索引
        :param name: 索引名称
        """
        sql = f"DROP INDEX {name} ON {self._name}"
        self._execute(sql)
