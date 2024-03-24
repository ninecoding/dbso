# -*- coding: UTF-8 -*-
class Colum:
    def __init__(self, name: str, col_type: str = "VARCHAR", length: int or str = 0, unsigned: bool = False,
                 auto_increment: bool = False, primary_key: bool = False, not_null: bool = False,
                 unique: bool = False, default="", check: str = "", reference_table: str = "",
                 reference_col: str = "", constraint: str = "", addition: str = ""):
        self._sqls = []
        if not constraint:
            self._sqls = [name, col_type]
            self._sqls.append(f"({length})") if length else None
            self._sqls.append("UNSIGNED") if unsigned else None
            self._sqls.append("AUTO_INCREMENT") if auto_increment else None
            self._sqls.append("PRIMARY KEY") if primary_key else None
            self._sqls.append("NOT NULL") if not_null else None
            self._sqls.append("UNIQUE") if unique else None
            self._sqls.append(f"DEFAULT '{default}'") if default else None
            self._sqls.append(f"CHECK ({check})") if check else None
            self._sqls.append(addition) if addition else None
            if reference_table and reference_col:
                self._sqls.append("REFERENCES")
                self._sqls.append(f"{reference_table}({reference_col})")
        else:
            self._sqls.append("CONSTRAINT")
            self._sqls.append(constraint)
            self._sqls.append("FOREIGN KEY")
            self._sqls.append(f"({name})")
            self._sqls.append("REFERENCES")
            self._sqls.append(f"{reference_table}({reference_col})")

    @property
    def sql(self):
        return " ".join(self._sqls)

    def __str__(self):
        return f"<DBSO.Colum>"


def col(name: str, col_type: str = "VARCHAR", length: int or str = 0, unsigned: bool = False,
        auto_increment: bool = False, primary_key: bool = False, not_null: bool = False, unique: bool = False,
        default="", check: str = "", reference_table: str = "", reference_col: str = "", constraint: str = "",
        addition: str = ""):
    """
    生成列表对象
    :param name: 列表名
    :param col_type: 列表类型
    :param length: 列表长度
    :param unsigned: 无符号
    :param auto_increment: 自动增长
    :param primary_key: 主键约束
    :param not_null: 非空约束
    :param unique: 唯一约束
    :param default: 默认值
    :param check: 检查约束
    :param reference_table: 外键表
    :param reference_col: 外键列名
    :param constraint: 约束名
    :param addition: 附加SQL语句
    :return: 列表对象
    """
    return Colum(name, col_type, length, unsigned, auto_increment, primary_key, not_null, unique, default, check,
                 reference_table, reference_col, constraint, addition)
