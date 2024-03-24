# -*- coding: UTF-8 -*-
tinyint = "TINYINT"  # 1 Bytes 小整数值
smallint = "SMALLINT"  # 2 Bytes 大整数值
mediumint = "MEDIUMINT"  # 3 Bytes 大整数值
int = "INT"
integer = "INTEGER"  # 4 Bytes 大整数值
bigint = "BIGINT"  # 8 Bytes 极大整数值
float = "FLOAT"  # 4 Bytes 单精度浮点数值
double = "DOUBLE"  # 8 Bytes 双精度浮点数值
decimal = "DECIMAL"  # 对DECIMAL(M,D)如果M>D为M+2否则为D+2 小数值

date = "DATE"  # 3 YYYY-MM-DD	日期值
time = "TIME"  # 3 HH:MM:SS 时间值或持续时间
year = "YEAR"  # 1 YYYY 年份值
datetime = "DATETIME"  # 8 YYYY-MM-DD hh:mm:ss 混合日期和时间值
timestamp = "TIMESTAMP"  # 4 YYYY-MM-DD hh:mm:ss 混合日期和时间值，时间戳

char = "CHAR"  # 0-255 bytes 定长字符串
varchar = "VARCHAR"  # 0-65535 bytes 变长字符串
tinyblob = "TINYBLOB"  # 0-255 bytes 不超过 255 个字符的二进制字符串
tinytext = "TINYTEXT"  # 0-255 bytes 短文本字符串
blob = "BLOB"  # 0-65 535 bytes	二进制形式的长文本数据
text = "TEXT"  # 0-65 535 bytes	长文本数据
mediumblob = "MEDIUMBLOB"  # 0-16 777 215 bytes	二进制形式的中等长度文本数据
mediumtext = "MEDIUMTEXT"  # 0-16 777 215 bytes	中等长度文本数据
longblob = "LONGBLOB"  # 0-4 294 967 295 bytes 二进制形式的极大文本数据
longtext = "LONGTEXT"  # 0-4 294 967 295 bytes 极大文本数据
enum = "ENUM"  # 枚举类型
