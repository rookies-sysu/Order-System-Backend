# Database of TinyHippo

> Departured after dockerized

## The format of config

```json
{
    "localhost":{
        "host":"localhost",
        "port":3306,
        "user":"root",
        "password":"xxx",
        "database":"xxx",
        "charset":"utf8"
        }
}
```


## Usage

### Import data
```shell
python data_importer.py
```


### The Operator of Each Table

```python
from dbOperators import *
```

