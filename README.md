# 前言

在**Python**中使用**SQL**查询语句是一件繁琐且不便于管理的事情，但又成为几乎目前存储数据的主流方式，我们试想是否能够使对**数据库**的各种操作能像**原生对象**的操作一样简单便捷，使开发者将精力更多地投入到产品功能的研发当中，所以本文将介绍一种全新的**Python**用使用**MySQL数据库**的方式：**DBSO库**
***

# DBSO库介绍

**DBSO** (Database Select Object 数据库查询对象) 是一个以**面向对象**的方式管理**MySQL数据库**的Python第三方库，它能帮助你以调用对象的方式对数据库进行**连接、查询、插入、删除、修改**等操作，内置SQL常用**关键字**，删除对象时**自动断开连接**，以**元素**方式调用数据库、数据表和数据行，**结构化**地建立和查询数据表，使用它能极大简化Python中存储数据的开发流程，**DBSO**遵循以下原则：
 1. 将数据库的各个**组成部分**视作数据的存储**容器**
 2. SQL的**并行逻辑**拆解为**多次实现**
 3. **查询对象**只对自己的自己的结构负责
 4. SQL的**存储过程**由Python的**函数封装**代替
 5. 在存储实现中，**逻辑**永远优先于**语法**
 6. 对数据描述的**概念**不继承SQL中的概念
 
> **LICENSE许可：** 遵循 *GPL version 3* 开源协议

**未来可能的版本更新：**
 1. 支持其他如SQL Sever、Oracle、SQLite等数据库的兼容，实现跨数据库数据管理
 2. 逐步脱离依赖SQL独立为一个面向对象接口的非关系型数据库
 3. 扩充面向实际功能需要和数据计算的日期时间对象、条件判断对象和异常类
> 当前 dbso 版本为 v1.1.0
 ***

# DBSO库安装

安装
```bash
pip install dbso
```
调用

```python
import dbso
```

***

# DBSO库构成

 - Connect 用于建立和管理MySQL数据库连接
 
| 成员属性 | 属性含义 |
|--|--|
| state | 连接状态 |
| databases | 连接下数据库名称 |
| desc | 连接信息 |
| version | 服务器版本信息 |
| status | 服务器状态 |
| variables | 服务器配置变量 |

| 成员方法 | 参数 | 方法作用 |
|--|--|--|
| \_\_init\_\_ | `host: str, username: str, password: str, port: int, charset: str` | 构造函数 |
| disconnect | - | 断开连接 |
| reconnect | - | 重新连接 |
| create | `name: str, charset: str, collate: str` | 创建数据库 |
| cmd | `sql: str` | 执行命令并提交 |
| rollback | - | 回滚 |

 - Database 用于管理数据库查询对象
 
| 成员属性 | 属性含义 |
|--|--|
| tables | 数据库下数据表名称 |
| desc | 数据库结构 |

| 成员方法 | 参数 | 方法作用 |
|--|--|--|
| create | `name: str, title: list, auto: int, engine: str, charset: str` | 创建数据表 |
| rename | `name: str` | 重命名数据库 (仅支持 MySQL 5.1.23及以前版本) |
|  |  |  |

 - Table 用于管理数据表查询对象和数据

| 成员属性 | 属性含义 |
|--|--|
| length | 数据表长度 |
| index | 数据表下索引名称 |
| desc | 数据表结构 |
| sql | 数据表创建语句 |
| references | 数据表外键信息 |

| 成员方法 | 参数 | 方法作用 |
|--|--|--|
| append | `*args` | 添加数据行 |
| clear | - | 清空表 |
| add | `col:Colum` | 添加数据列 |
| modify | `col:Colum` | 修改数据列 |
| drop | `col_name: str` | 删除数据列 |
| primary | `col_name: str` | 设置主键约束 |
| foreign | `constraint_name: str, col_name: str, foreign_table_name: str, foreign_col_name: str` | 设置外键约束 |
| drop_foreign | `constraint_name: str` | 删除外键约束 |
| rename | `name: str, new_name: str` | 重命名数据表或字段 |
| create_index | `name: str, col_dict: dict, unique: bool` | 创建索引 |
| drop_index | `name: str` | 删除索引 |

 - Colum 用于创建数据列对象

| 构造参数列表 | 参数含义 | 默认值 |
|--|--|--|
| `name: str`| 数据列名 | - |
| `col_type: str`| 数据列类型 | "VARCHAR" |
| `length: int or str`| 数据列长度 | 0 |
| `unsigned: bool`| 是否无符号 | False |
| `auto: bool`| 是否自动增长 | False |
| `primary: bool`| 是否为主键 | False |
| `null: bool`| 是否可空 | True |
| `unique: bool`| 是否唯一 | False |
| `default: int or str`| 默认值 | "" |
| `check: str`| 检查约束 | "" |
| `foreign_table: str`| 外键表名 | "" |
| `foreign_col: str`| 外键数据列名 | "" |
| `constraint: str`| 外键约束名 | "" |
| `addition: str`| 附加SQL语句 | "" |

 - Condition 用于创建数据列对象

| 构造参数列表 | 参数含义 | 默认值 |
|--|--|--|
| `cols: list`| 数据列列表 | None |
| `offset: int`| 偏移量 | 0 |
| `step: int`| 步数 | 0 |
| `asc: bool`| 是否升序 | True |
| `null: bool`| NULL是否置顶 | False |
| `check: str`| 约束 | "" |
| `order_col: str`| 排序依赖列列名 | "" |
| `group_col: str`| 分组依赖列列名 | "" |
| `having: str`| 分组约束 | "" |
| `addition: str`| 附加SQL语句 | "" |
***

# 快速开始使用 (示例代码)

```python
import dbso  # 导入dbso库

conn = dbso.connect('xxx.xxx.xxx.xxx', 'root', 'root_password')  # 建立数据库连接
database_test = conn["test_db"]  # 获取名为test_db的数据库对象
table_test = database_test["test_tb"]  # 获取名为test_tb的数据表对象

table_test.append(1001, "数据1", "数据2", "2024-3-26", "true")  # 向数据表中插入数据行1
table_test.append(1002, "数据3", "数据4", "2024-3-27", "false")  # 向数据表中插入数据行2

result = table_test["id=1001"]  # 在表中查询id为1001的数据
```
以上代码完成了一个将两条记录插入了test_db库下test_tb表中，并查询id=1001的数据行的简单功能
***

# 详细教程
## 数据库操作
### 1. 连接MySQL

```python
conn = dbso.connect(服务器地址,账号,密码,[端口号],[字符集])
```

### 2. 创建数据库

```python
db = conn.create(数据库名,[字符集名],[排序规则名])
```

### 3. 删除数据库

```python
del conn[数据库名]
```

### 4. 重命名数据库

```python
db.rename(新数据库名)
```
***
## 数据表操作
### 1. 创建数据列定义对象
数据列定义对象 (简称列定义对象) 指的是通过col函数返回的对象，数据列的概念在dbso库的使用中非常重要

```python
from dbso import col  # 导入数据列定义类
from dbso import word as wd  # 导入SQL关键词包
```
创建普通列定义对象列表，多个列定义对象组成的列表在dbso中称为Header，用来定义一个数据表结构
```python
header = [col(数据列名,wd.数据类型,[数据长度],[...]),
          col(数据列名,wd.数据类型,[数据长度],[...]),
          col(数据列名,wd.数据类型,[数据长度],[...]),
          ...]
```
创建外键约束定义对象，和普通列定义对象一样，也可以放入Header中
```python
foreign_col = col(constraint=外键名,name=数据列名,foreign_table=外键数据表,foreign_col=外键数据列名)
```

### 2. 创建数据表
表中每个字段称为一个数据列

```python
tb = db.create(表名,列定义对象列表,[自动增长初始值],[引擎名],[字符集名])
```

### 3. 添加数据列
```python
tb.add(列定义对象)
```

### 4. 修改数据列
只需定义一个新的同名数据列对象作为参数即可更改原数据列
```python
tb.modify(列定义对象)
```
### 5. 删除数据列
```python
tb.drop(数据列名称)
```
### 6. 清空数据表
```python
tb.clear()
```
### 7. 设置外键约束
```python
tb.foreign(外键名,数据列名,外键数据表,外键数据列名)
```
### 8. 删除外键约束
```python
tb.drop_foreign(外键名)
```
### 9. 创建表索引
```python
{数据列1:"ASC"|"DESC",数据列2:"ASC"|"DESC",数据列3:"ASC"|"DESC"...}  # 索引字典定义格式
```
```python
table_test.create_index(索引名,索引字典,[是否唯一])
```
### 10. 删除表索引
```python
table_test.drop_index(索引名)
```
### 11. 重命名数据表
```python
table_test.rename(新数据表名)
```
***
## 数据操作
### 1. 创建约束对象
约束对象指的是cond函数返回的对象，约束对象是dbso查询中的一个重要概念

```python
from dbso import cond  # 导入约束类

cd = cond([数据列名称列表],[约束条件],[偏移量],[步数],[...])
```

### 2. 向表中添加数据
添加方式 1：快速插入数据
```python
tb.append(数据1,数据2,数据3...)
```
添加方式 2：以值字典的方式插入数据
```python
value_dict = {"列名1":数据1,"列名2":数据2,"列名3":数据3...}
tb.append(value_dict)
```

### 3. 查询表中数据
查询方式 1：用 * 符号查询表中全部数据
```python
rows = tb["*"]
```
查询方式 2：用SQL约束语句查询表中数据
```python
rows = tb[约束条件]
```
查询方式 3：以列名称列表作为参数查询表中选定列数据
```python
rows = tb[(列名称1,列名称2,列名称3...)]
```
查询方式 4：用Condition约束对象查询表中数据
```python
rows = tb[约束对象]
```

### 4. 更新表中数据
更新方式 1：用 * 符号更新表中全部数据
```python
tb["*"] = {"列名1":数据1,"列名2":数据2,"列名3":数据3...}
```
更新方式 2：用SQL约束语句更新表中数据
```python
tb[约束条件] = {"列名1":数据1,"列名2":数据2,"列名3":数据3...}
```
更新方式 3：用Condition约束对象更新表中数据
```python
tb[约束对象] = {"列名1":数据1,"列名2":数据2,"列名3":数据3...}
```

### 5. 删除表中数据
删除方式 1：用 * 符号删除表中全部数据（不推荐，推荐使用清空函数）
```python
del tb["*"]
```
删除方式 2：用SQL约束语句删除表中数据
```python
del tb[约束条件]
```
删除方式 3：用Condition约束对象删除表中数据
```python
del tb[约束对象]
```
以上仅仅是对dbso库常用操作的介绍，更多的操作请查看文章中库**结构表**
> dbso库查询对象均支持内置的 len() 函数统计当前查询对象下的子查询对象数或数据行数
***

## 异常处理
在操作数据库时，可能会遇到各种异常，dbso提供了rollback函数

```python
try:
    ...
except Exception as e:
	...
    conn.rollback()
finally:
	...
    conn.disconnect()
```
以上代码为异常处理示例
***

## 总结
&emsp;&emsp;本文介绍了如何用dbso库对MySQL数据库进行连接和管理等操作，介绍了dbso库的基本使用方法，通过dbso库我们可以轻松地在Python中使用MySQL库，无论是查询还是操作，dbso都为其提供了强大的面向对象方式功能支持。\
&emsp;&emsp;由于本库处于初期版本阶段，可能存在一定Bug和缺陷，如果希望参与到改进该项目中，可以将反馈和建议发送至作者邮箱。
***
文章作者：Nine\
作者邮箱：ninecodespace@gmail.com\
[Python官方文档：https://docs.python.org/3/library/index.html](https://docs.python.org/3/library/index.html)
