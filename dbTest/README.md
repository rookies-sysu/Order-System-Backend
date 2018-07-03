# Test for Database

Testing after database has been created.



## 1 Select & Update

### 1.1 Select

假设 tN 为数据表名，rN 为餐厅账户名，ID 为餐厅ID，PH 为餐厅电话, R 为搜索的及结果属性:

- **等价类划分:**

  tN1 = {tN: 数据库中不存在该数据表名}

  tN2 = {tN: 数据库中已存在该数据表名}

  rN1 = {rN: 数据库中不存在该 'restaurantName'}

  rN2 = {rN: 数据库中已存在该 'restaurantName'}

  R1 = {R: 这些属性值全部属于该数据表}

  R2 = {R: 这些属性值不是全部属于该数据表}

- **输入:**

  (tN, rN, R) or (tN, rN, R, PH)

- **输出:**

  { status, result }

|       测试用例        | tableName   | restaurantName | phone       | result                     | 预期输出                                                  |
| :-------------------: | :---------- | :------------- | :---------- | -------------------------- | :-------------------------------------------------------- |
|   WR1(tN1, rN2, R1)   | Restaurants | rName1         | -           | ["restaurantID"]           | { False, [] }                                             |
|   WR2(tN2, rN2, R2)   | Restaurant  | rName1         | -           | ["restaurantIDs"]          | { False, [] }                                             |
|   WR3(tN2, rN2, R1)   | Restaurant  | rName1         | -           | ["restaurantID"]           | {True, [{'restaurantID': 1}]}                             |
| WR4(tN2, rN2, R1, PH) | Restaurant  | rName1         | 10293847567 | ["restaurantID", " email"] | {True, [{'restaurantID': 1, 'email': 'rName1@mail.com'}]} |
|   WR5(tN2, rN1, R1)   | Restaurant  | rName3         | -           | ["restaurantID"]           | {True, []}                                                |
| WR6(tN2, rN1, R1, PH) | Restaurant  | rName3         | 10293847567 | ["restaurantID"]           | {True, []}                                                |

### 1.2 Update

假设 SI 为餐厅登录状态，tN 为数据表名，rN 为餐厅账户名，ID 为餐厅ID，N 为更新的键值对:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  tN1 = {tN: 数据库中不存在该数据表名}

  tN2 = {tN: 数据库中已存在该数据表名}

  N1 = {N: 更新的键值对数量为1}

  N2 = {N: 更新的键值对数量不为1}

  N2 = {N: 更新的键值对数量为1,但是更新的值为与表中其他值冲突}

- **输入:**

  (tN, rN, R) or (tN, rN, R, PH)

- **输出:**

  status = { SUCCESS, FAILED }

|     测试用例      | tableName   | new                                             | 预期输出 |
| :---------------: | :---------- | ----------------------------------------------- | :------- |
| WR1(SI1, tN2, N1) | Restaurant  | password = '1234567'                            | FAILED   |
| WR2(SI2, tN1, N1) | Restaurants | password = '1234567'                            | FAILED   |
| WR3(SI2, tN2, N2) | Restaurant  | password = '1234567', restaurantName = 'rName2' | FAILED   |
| WR4(SI2, tN2, N1) | Restaurant  | password = '1234567'                            | SUCCESS  |
| WR5(SI2, tN2, N3) | Restaurant  | restaurantName = 'rName2'                       | FAILED   |

### 

## 2 Table 'Restaurant'

### 2.1 Insert

假设 rN 为餐厅账户名，P 为餐厅账户密码，PH 为餐厅电话，E 为餐厅邮箱:

- **等价类划分:**

  rN1 = {rN: 数据库中不存在该 'restaurantName'}

  rN2 = {rN: 数据库中已存在该 'restaurantName'}

  P1 = {P: 6 $\le$ len('password') $\le$ 20}

  P2 = {P: 6 > len('password') or  len('password') > 20}

  PH1 = {PH: 数据库中不存在该 'phone'}

  PH2 = {PH: 数据库中已存在该 'phone'}

  E1 = {PH: 数据库中不存在该 'email'}

  E2 = {PH: 数据库中已存在该 'email'}

- **输入:**

  (rN, P, PH, E)

- **输出:**

  status = { SUCCESS, FAILED }

|       测试用例        | restaurantName | password | phone       | email           | 预期输出 |
| :-------------------: | :------------- | :------- | :---------- | :-------------- | :------- |
| WR1(rN1, P1, PH1, E1) | rName1         | 123456   | 10293847567 | rName1@mail.com | SUCCESS  |
| WR2(rN2, P1, PH1, E1) | rName1         | 123456   | 10293847568 | rName2@mail.com | FAILED   |
| WR3(rN1, P2, PH1, E1) | rName2         | 12345    | 10293847568 | rName2@mail.com | FAILED   |
| WR4(rN1, P2, PH1, E1) | rName2         | 21个1    | 10293847568 | rName2@mail.com | FAILED   |
| WR5(rN1, P1, PH2, E1) | rName2         | 123456   | 10293847567 | rName2@mail.com | FAILED   |
| WR6(rN1, P1, PH1, E2) | rName2         | 123456   | 10293847568 | rName1@mail.com | FAILED   |

### 2.2 Delete

假设 SI 为餐厅登录状态，rN 为餐厅账户名，ID 为餐厅ID:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  rN1 = {rN: 数据库中不存在该 'restaurantName'}

  rN2 = {rN: 数据库中已存在该 'restaurantName'}

  rN3 = {rN: 其他用户的 'restaurantName'}

  ID1 = {ID: 数据库中不存在该 'restaurantID'}

  ID2 = {ID: 数据库中已存在该 'restaurantID'}

  ID3 = {ID: 其他用户的 'restaurantID'}

- **输入:**

  (SI, rN) or (SI, ID)

- **输出:**

  status = { SUCCESS, FAILED }

|   测试用例    | restaurantName | restaurantID | 预期输出 |
| :-----------: | :------------- | :----------- | -------- |
| WR1(SI1, rN2) | rName1         | -            | FAILED   |
| WR2(SI1, ID2) | -              | 1            | FAILED   |
| WR3(SI2, rN1) | rName3         | -            | FAILED   |
| WR4(SI2, rN3) | rName2         | -            | FAILED   |
| WR5(SI2, ID1) | -              | 3            | FAILED   |
| WR6(SI2, rN2) | rName1         | -            | SUCCESS  |
| WR6(SI2, ID2) | -              | 2            | SUCCESS  |



## 3 Table 'DishType'

### 3.1 Insert

假设 SI 为餐厅登录状态，dtN 为菜类名:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  dtN1 = {dtN: 该商家的数据库中不存在该菜类名}

  dtN2 = {dtN: 该商家的数据库中已存在该菜类名}

- **输入:**

  (SI, dtN)

- **输出:**

  status = { SUCCESS, FAILED }

|    测试用例    | dishTypeName | 预期输出 |
| :------------: | :----------- | :------- |
| WR1(SI1, dtN1) | dtype1       | FAILED   |
| WR2(SI2, dtN2) | dtype1       | SUCCESS  |
| WR3(SI2, dtN1) | dtype1       | FAILED   |

### 3.2 Delete

假设 SI 为餐厅登录状态，dtN 为菜类名，dtID 为菜类ID:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  dtN1 = {dtN: 该商家的数据库中不存在该菜类名}

  dtN2 = {dtN: 该商家的数据库中已存在该菜类名}

  dtID1 = {dtID: 该商家的数据库中不存在该菜类ID}

  dtID2 = {dtID 该商家的数据库中已存在该菜类ID}

- **输入:**

  (SI, dtID) or (SI, dtN) 

- **输出:**

  status = { SUCCESS, FAILED }

|    测试用例     | dishTypeName | dishTypeID | 预期输出 |
| :-------------: | :----------- | ---------- | :------- |
| WR1(SI1, dtID2) | -            | 1          | FAILED   |
| WR2(SI2, dtID1) | -            | 3          | FAILED   |
| WR3(SI2, dtID1) | -            | 5          | FAILED   |
| WR4(SI2, dtN1)  | dtype3       | -          | FAILED   |
| WR5(SI2, dtN1)  | dtype5       | -          | FAILED   |
| WR6(SI2, dtID2) | -            | 1          | SUCCESS  |
| WR7(SI2, dtN2)  | dtype2       | -          | SUCCESS  |



## 4 Table 'RestaurantTable'

### 4.1 Insert

假设 SI 为餐厅登录状态，tN 为桌号:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  tN1 = {tN: 该商家的数据库中不存在该桌号}

  tN2 = {tN: 该商家的数据库中已存在该桌号}

- **输入:**

  (SI, tN)

- **输出:**

  status = { SUCCESS, FAILED }

|   测试用例    | tableNumber | 预期输出 |
| :-----------: | :---------- | :------- |
| WR1(SI1, tN1) | 1           | FAILED   |
| WR2(SI2, tN1) | 1           | SUCCESS  |
| WR3(SI2, tN2) | 1           | FAILED   |

### 4.2 Delete

假设 SI 为餐厅登录状态，tN 为桌号，tID 为桌ID:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  tN1 = {tN: 该商家的数据库中不存在该桌号}

  tN2 = {tN: 该商家的数据库中已存在该桌号}

  tID1 = {tID: 该商家的数据库中不存在该桌ID}

  tID2 = {tID: 该商家的数据库中已存在该桌ID}

- **输入:**

  (SI, tID) or (SI, tN) 

- **输出:**

  status = { SUCCESS, FAILED }

|    测试用例    | tableNumber | tableID | 预期输出 |
| :------------: | :---------- | ------- | :------- |
| WR1(SI1, tID2) | -           | 1       | FAILED   |
| WR2(SI2, tID1) | -           | 3       | FAILED   |
| WR3(SI2, tID1) | -           | 5       | FAILED   |
| WR4(SI2, tN1)  | 3           | -       | FAILED   |
| WR5(SI2, tN1)  | 5           | -       | FAILED   |
| WR6(SI2, tID2) | -           | 1       | SUCCESS  |
| WR7(SI2, tN2)  | 2           | -       | SUCCESS  |

## 5 Table 'QRlink'

### 5.1 Insert

假设 SI 为餐厅登录状态，URL 为二维码URL, tN 为桌号:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  URL1 = {URL: 该商家的数据库中不存在该二维码URL}

  URL2 = {URL: 该商家的数据库中已存在该二维码URL}

  tN1 = {tN: 该商家的数据库中不存在该桌号}

  tN2 = {tN: 该商家的数据库中已存在该桌号}

- **输入:**

  (SI, URL, tN)

- **输出:**

  status = { SUCCESS, FAILED }

|      测试用例       | linkImageURL       | tableNumber | 预期输出 |
| :-----------------: | ------------------ | :---------- | :------- |
| WR1(SI1, URL1, tN1) | http://qrlink1.com | 1           | FAILED   |
| WR2(SI2, URL1, tN1) | http://qrlink1.com | 1           | SUCCESS  |
| WR3(SI2, URL2, tN1) | http://qrlink1.com | 2           | FAILED   |
| WR4(SI2, URL1, tN2) | http://qrlink2.com | 1           | FAILED   |

### 5.2 Delete

假设 SI 为餐厅登录状态，URL 为二维码URL，LID 为二维码ID:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  URL1 = {URL: 该商家的数据库中不存在该二维码URL}

  URL2 = {URL: 该商家的数据库中已存在该二维码URL}

  LID1 = {LID: 该商家的数据库中不存在该二维码ID}

  LID2 = {LID: 该商家的数据库中已存在该二维码ID}

- **输入:**

  (SI, URL) or (SI, LID) 

- **输出:**

  status = { SUCCESS, FAILED }

|    测试用例    | linkImageURL       | linkID | 预期输出 |
| :------------: | :----------------- | ------ | :------- |
| WR1(SI1, LID2) | -                  | 1      | FAILED   |
| WR2(SI2, LID1) | -                  | 3      | FAILED   |
| WR3(SI2, LID1) | -                  | 5      | FAILED   |
| WR4(SI2, URL1) | http://qrlink3.com | -      | FAILED   |
| WR5(SI2, URL1) | http://qrlink5.com | -      | FAILED   |
| WR6(SI2, LID2) | -                  | 1      | SUCCESS  |
| WR7(SI2, URL2) | http://qrlink2.com | -      | SUCCESS  |



## 6 Table 'Dish'

### 6.1 Insert

假设 SI 为餐厅登录状态，dN 为菜名，dtID 为菜类ID:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  dN1 = {dN: 该商家的数据库中不存在该菜名}

  dN2 = {dN: 该商家的数据库中已存在该菜名}

  dtID1 = {dtID: 数据库中不存在该菜类ID}

  dtID2 = {dtID: 数据库中已存在该菜类ID}

- **输入:**

  (SI, dN, dtID)

- **输出:**

  status = { SUCCESS, FAILED }

|       测试用例       | dishName | dishTypeID | 预期输出 |
| :------------------: | -------- | :--------- | :------- |
| WR1(SI1, dN1, dtID2) | dish1    | 5          | FAILED   |
| WR2(SI2, dN1, dtID2) | dish1    | 5          | SUCCESS  |
| WR3(SI2, dN2, dtID2) | dish1    | 5          | FAILED   |
| WR4(SI2, dN1, dtID1) | dish2    | 7          | FAILED   |
| WR5(SI2, dN1, dtID1) | dish2    | 3          | FAILED   |

### 6.2 Delete

假设 SI 为餐厅登录状态，dID 为菜ID:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  dID1 = {dID: 该商家的数据库中不存在该菜ID}

  dID2 = {dID: 该商家的数据库中已存在该菜ID}

- **输入:**

  (SI, dID) 

- **输出:**

  status = { SUCCESS, FAILED }

|    测试用例    | dishID | 预期输出 |
| :------------: | ------ | :------- |
| WR1(SI1, dID2) | 1      | FAILED   |
| WR2(SI2, dID1) | 7      | FAILED   |
| WR3(SI2, dID1) | 9      | FAILED   |
| WR6(SI2, dID2) | 1      | SUCCESS  |



## 7 Table 'DishComment'

### 7.1 Insert

假设 dID 为菜ID:

- **等价类划分:**

  dID1 = {dID: 数据库中不存在该菜ID}

  dID2 = {dID: 数据库中已存在该菜ID}

- **输入:**

  (dID) 

- **输出:**

  status = { SUCCESS, FAILED }

| 测试用例  | dishID | 预期输出 |
| :-------: | ------ | :------- |
| WR1(dID2) | 11     | FAILED   |
| WR2(dID1) | 9      | SUCCESS  |

### 7.2 Delete

假设 dcID 为菜评论ID，dID 为菜ID:

- **等价类划分:**

  dcID1 = {dcID: 数据库中不存在该菜评论ID}

  dcID2 = {dcID: 数据库中已存在该菜评论ID}

  dID1 = {dID: 数据库中不存在该菜ID}

  dID2 = {dID: 数据库中已存在该菜ID}

- **输入:**

  (dcID) or (dID)

- **输出:**

  status = { SUCCESS, FAILED }

|  测试用例  | dishCommentID | dishID | 预期输出 |
| :--------: | ------------- | ------ | :------- |
| WR1(dcID1) | 4             | -      | FAILED   |
| WR2(dcID2) | 3             | -      | SUCCESS  |
| WR3(dID1)  | -             | 10     | FAILED   |
| WR4(dID2)  | -             | 9      | SUCCESS  |



## 8 Table 'OrderList'

### 8.1 Insert

假设 SI 为餐厅登录状，tID 为桌ID:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  tID1 = {tID: 数据库中不存在该桌ID}

  tID2 = {tID: 数据库中已存在该桌ID}

- **输入:**

  (SI, tID)

- **输出:**

  status = { SUCCESS, FAILED }

|    测试用例    | tableID | 预期输出 |
| :------------: | ------- | :------- |
| WR1(SI1, tID2) | 5       | FAILED   |
| WR2(SI2, tID2) | 5       | SUCCESS  |
| WR3(SI2, tID1) | 7       | FAILED   |

### 8.2 Delete

假设 SI 为餐厅登录状态，oID 为订单ID，tID 为桌ID:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  oID1 = {oID: 数据库中不存在该订单ID}

  oID2 = {oID: 数据库中已存在该订单ID}

  tID1 = {tID: 数据库中不存在该桌ID}

  tID2 = {tID: 数据库中已存在该桌ID}

- **输入:**

  (SI, oID) or (SI, tID)

- **输出:**

  status = { SUCCESS, FAILED }

|    测试用例    | orderID | tableID | 预期输出 |
| :------------: | ------- | ------- | :------- |
| WR1(SI1, oID2) | 1       | -       | FAILED   |
| WR2(SI2, oID1) | 10      | -       | FAILED   |
| WR3(SI2, tID1) | -       | 7       | FAILED   |
| WR4(SI2, oID2) | 1       | -       | SUCCESS  |
| WR5(SI2, tID2) | -       | 5       | SUCCESS  |



## 9 Table 'Recommendation'

### 9.1 Insert

假设 SI 为餐厅登录状态:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

- **输入:**

  (SI)

- **输出:**

  status = { SUCCESS, FAILED }

| 测试用例 | 预期输出 |
| :------: | :------- |
| WR1(SI1) | FAILED   |
| WR2(SI2) | SUCCESS  |

### 9.2 Delete

假设 SI 为餐厅登录状态，rcID 为推荐ID:

- **等价类划分:**

  SI1 = {SI: 未登录}

  SI2 = {SI: 已登录}

  rcID1 = {rcID: 该商家的数据库中不存在该推荐ID}

  rcID2 = {rcID: 该商家的数据库中已存在该推荐ID}

- **输入:**

  (SI, rcID)

- **输出:**

  status = { SUCCESS, FAILED }

|    测试用例     | recommendationID | 预期输出 |
| :-------------: | ---------------- | :------- |
| WR1(SI1, rcID2) | 1                | FAILED   |
| WR2(SI1, rcID1) | 5                | FAILED   |
| WR3(SI1, rcID1) | 3                | FAILED   |
| WR4(SI1, rcID2) | 1                | SUCCESS  |



## 10 Table 'RecommendationDetails'

### 10.1 Insert

假设 rcID 为推荐ID，dID 为菜ID，R为推荐ID与菜ID的关系:

- **等价类划分:**

  rcID1 = {rcID: 数据库中不存在该rcID}

  rcID2 = {rcID: 数据库中已存在该rcID}

  dID1 = {dID: 数据库中不存在该dID}

  dID2 = {dID: 数据库中已存在该dID}

  R1 = {R: 推荐ID与菜ID不属于同一个餐厅}

  R2 = {R: 推荐ID与菜ID属于同一个餐厅}

- **输入:**

  (rcID, dID, R)

- **输出:**

  status = { SUCCESS, FAILED }

|       测试用例       | recommendationID | dishID | 预期输出 |
| :------------------: | ---------------- | ------ | :------- |
| WR1(rcID1, dID2, R1) | 5                | 9      | FAILED   |
| WR2(rcID2, dID1, R1) | 2                | 11     | FAILED   |
| WR3(rcID2, dID2, R1) | 3                | 9      | FAILED   |
| WR4(rcID2, dID2, R2) | 2                | 9      | SUCCESS  |

### 10.2 Delete

假设 rcID 为推荐ID，dID 为菜ID:

- **等价类划分:**

  rcID1 = {rcID: 数据库中不存在该rcID}

  rcID2 = {rcID: 数据库中已存在该rcID}

  dID1 = {dID: 数据库中不存在该dID}

  dID2 = {dID: 数据库中已存在该dID}

- **输入:**

  (rcID) or (dID)

- **输出:**

  status = { SUCCESS, FAILED }

|  测试用例  | recommendationID | dishID | 预期输出 |
| :--------: | ---------------- | ------ | :------- |
| WR1(rcID1) | 7                | -      | FAILED   |
| WR2(dID1)  | -                | 11     | FAILED   |
| WR3(dID2)  | -                | 9      | SUCCESS  |
| WR4(rcID2) | 2                | -      | SUCCESS  |

### 