# -*- coding: UTF-8 -*-
from .tool import warn


class SO:
    _conn = None
    _cursor = None

    def _execute(self, command: str):
        """
        执行数据库命令
        :param command: 命令
        """
        try:
            self._cursor.execute(command)
        except Exception as e:
            warn(str(e))
            self._conn.rollback()

    def _commit(self):
        """
        提交数据库命令
        """
        self._conn.commit()
