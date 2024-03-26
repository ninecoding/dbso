class Condition:
    def __init__(self, cols: list = None, check: str = "", offset: int = 0, step: int = 0, order_col: str = "",
                 asc: bool = True, null: bool = False, group_col: str = "", having: str = "", addition: str = ""):
        self._cols = cols if cols else ["*"]
        self._sqls = []
        self._sqls.append("WHERE " + check)

        if offset and step:
            self._sqls.append(f"LIMIT {offset},{step}")
        elif offset:
            self._sqls.append(f"OFFSET {offset}")
        elif step:
            self._sqls.append(f"LIMIT {step}")
        if order_col and asc:
            self._sqls.append(f"ORDER BY {order_col} ASC")
        elif order_col:
            self._sqls.append(f"ORDER BY {order_col} DESC")
        if null:
            self._sqls.append("NULLS FIRST")
        if group_col and having:
            self._sqls.append(f"GROUP BY {group_col} HAVING {having}")
        elif group_col:
            self._sqls.append(f"GROUP BY {group_col}")

        self._sqls.append(addition) if addition else None

    @property
    def cols(self):
        return self._cols

    @property
    def sql(self):
        return " ".join(self._sqls)

    def __str__(self):
        return f"<DBSO.Condition>"


def cond(cols: list = None, check: str = "", offset: int = 0, step: int = 0, order_col: str = "", asc: bool = True,
         null: bool = False, group_col: str = "", having: str = "", addition: str = ""):
    """
    条件对象
    :param cols: 数据列列表
    :param check: 约束
    :param offset: 偏移量
    :param step: 步数
    :param order_col: 排序依赖列列名
    :param asc: 是否升序
    :param null: NULL是否置顶
    :param group_col: 分组依赖列列名
    :param having: 分组约束
    :param addition: 附加SQL语句
    :return: 条件对象
    """
    return Condition(cols, check, offset, step, order_col, asc, null, group_col, having, addition)
