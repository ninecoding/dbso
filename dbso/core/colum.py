# -*- coding: UTF-8 -*-
class Colum:
    def __init__(self, name: str, col_type: str = "VARCHAR", length: int or str = 0, unsigned: bool = False,
                 auto: bool = False, primary: bool = False, null: bool = True,
                 unique: bool = False, default: int or str = "", check: str = "", foreign_table: str = "",
                 foreign_col: str = "", constraint: str = "", addition: str = ""):
        self._sqls = []
        if not constraint:
            self._sqls = [name, col_type]
            self._sqls.append(f"({length})") if length else None
            self._sqls.append("UNSIGNED") if unsigned else None
            self._sqls.append("AUTO_INCREMENT") if auto else None
            self._sqls.append("PRIMARY KEY") if primary else None
            self._sqls.append("NOT NULL") if not null else None
            self._sqls.append("UNIQUE") if unique else None
            self._sqls.append(f"DEFAULT '{default}'") if default else None
            self._sqls.append(f"CHECK ({check})") if check else None
            self._sqls.append(addition) if addition else None
            if foreign_table and foreign_col:
                self._sqls.append("REFERENCES")
                self._sqls.append(f"{foreign_table}({foreign_col})")
        else:
            self._sqls.append("CONSTRAINT")
            self._sqls.append(constraint)
            self._sqls.append("FOREIGN KEY")
            self._sqls.append(f"({name})")
            self._sqls.append("REFERENCES")
            self._sqls.append(f"{foreign_table}({foreign_col})")

    @property
    def sql(self):
        return " ".join(self._sqls)

    def __str__(self):
        return f"<DBSO.Colum>"


def col(name: str, col_type: str = "VARCHAR", length: int or str = 0, unsigned: bool = False, auto: bool = False,
        primary: bool = False, null: bool = True, unique: bool = False, default: int or str = "", check: str = "",
        foreign_table: str = "", foreign_col: str = "", constraint: str = "", addition: str = ""):
    """
    生成列表对象
    :param name: 数据列名
    :param col_type: 数据列类型
    :param length: 数据列长度
    :param unsigned: 是否无符号
    :param auto: 是否自动增长
    :param primary: 是否为主键
    :param null: 是否可空
    :param unique: 是否唯一
    :param default: 默认值
    :param check: 检查约束
    :param foreign_table: 外键表名
    :param foreign_col: 外键数据列名
    :param constraint: 外键约束名
    :param addition: 附加SQL语句
    :return: 数据列对象
    """
    return Colum(name, col_type, length, unsigned, auto, primary, null, unique, default, check,
                 foreign_table, foreign_col, constraint, addition)
