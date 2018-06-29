# 数据库信息
DB_HOST="db"
DB_PORT=3306
DB_DATABASE="TINYHIPPO"
DB_USER="root"
DB_PASSWORD="tiny-hippo"
DB_CHARSET="utf8"

# 数据库连接池信息
# mincached : 启动时开启的闲置连接数量
DB_MIN_CACHED=3

# maxcached : 连接池中允许的闲置的最多连接数量
DB_MAX_CACHED=3

# maxshared : 共享连接数允许的最大数量。如果达到了最大数量，被请求为共享的连接将会被共享使用
DB_MAX_SHARED=10

# maxconnecyions : 创建连接池的最大数量
DB_MAX_CONNECYIONS=20

# blocking : 设置在连接池达到最大数量时的行为
DB_BLOCKING=True

# maxusage : 单个连接的最大允许复用次数。当达到最大数时,连接会自动重新连接(关闭和重新打开)
DB_MAX_USAGE=0

# setsession : 一个可选的SQL命令列表用于准备每个会话
DB_SET_SESSION=None