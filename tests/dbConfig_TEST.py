# The information of database
DB_HOST="127.0.0.1"
DB_PORT=3306
DB_DATABASE="TINYHIPPOTEST"
DB_USER="root"
DB_PASSWORD="tiny-hippo"
DB_CHARSET="utf8"

# The information of database connection pool

# mincached : The number of idle connections opened at startup
DB_MIN_CACHED=3

# maxcached : The maximum number of idle connections allowed in the connection pool
DB_MAX_CACHED=3

# maxshared : The maximum number of shared connections allowed. If the maximum number is reached, the connection requested to be shared will be shared.
DB_MAX_SHARED=10

# maxconnecyions : The maximum number of connection pools created.
DB_MAX_CONNECYIONS=20

# blocking : Set the behavior when the connection pool reaches its maximum number.
DB_BLOCKING=True

# maxusage : The maximum number of allowed multiplexing for a single connection. When the maximum number is reached, the connection will automatically reconnect (close and reopen)
DB_MAX_USAGE=0

# setsession : An optional list of SQL commands is used to prepare each session.
DB_SET_SESSION=None