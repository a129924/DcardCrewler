---
Title: Dcard爬蟲機器人
Date: 2022/05/17 15:00

---

---

# Dcard爬蟲機器人(下載圖片)

## 目的

* 讓能夠初學python的使用者，利用簡單的參數輸入，達到目的
* 且能快速的下載使用者所需的圖片在指定的路徑上

---
## 目標

### 這是什麼?
* 一個利用DCARD官方API下載圖片
* 也能利用本套件，取得使用者所需要的資料

- [x] 選定看板
- [x] 根據條件篩選
- [x] 下載圖片

### 使用情境
當你時間不多，但又想要看板上的圖片，就可以使用本套件，幫你節省滑看板時間，又能看到想要的文章圖片

---

## 執行環境
目前運行電腦版本為windows11
python環境為3.7.7，也使用了以下套件：
1. requests
2. json
3. os
4. urllib.request
5. fake_useragent
6. pandas
7. time

另外有幾個套件要下載，指令如下

```shell=
$ pip install requests
$ pip install urllib3
$ pip install fake-useragent
$ pip install pandas
```

---

## 如何使用

### 文件說明
在使用之前，我先說明主程式簡易的參數解說，同樣一份說明我也註記在主程式之中。
```python=
#==========================DcardCrawler.py===================================
"""
***取得文章預設是30筆 limit最大為100筆
GET_ALL_POST # 取得所有的文章
GET_FORUMS_POSTS # 取得該板所有文章
GET_THE_POST # 取得該文章
GET_POST_LINK # 取得該文章連結
GET_POST_CONTENT" # 取得該文章所有留言

METHOD
"popular "# 熱門=true #由舊到新=false
"limit" # 限制回傳的資料 最多100筆 熱門回應只取前3筆
"after", # 取得下一頁資訊 利用該文章回傳最多樓層 例如after=1 會取得1之後 不包含1
"""
```
這是依據[DCARD API說明文件](https://blog.jiatool.com/posts/dcard_api_v2/)所制定的格式，其中`METHOD`限制API回傳的值

### 開始使用
建置好環境後，放置在路徑底下，並創建`main.py`，或者是參考附加的`main.py`

    |-- setting.json
    |-- DcardCrawler.py
    |-- main.py

### 簡單實例
假如現在要下載**穿塔版**熱門前一百大文章的圖片
```python=
#==============================main.py=====================================

# 載入套件
from DcardCrawler import DcardCrawler

# 初始化程式
data1 = DcardCrawler(get_path="GET_FORUMS_POSTS",
                    forums="dressup", popular=True, 
                    limit=100)
#從API取得的資料轉換成json
data1.getDardApi()
# 將json轉換成dataframe 並篩選出要的欄位
data1.data_cleaning()
# 執行下載圖片 路徑必須加r ex: r".\data" 或者是 r'D:\data'
# 預設為 ".\data"
data1.run_download_img()
```

執行完成後，檔案結構如下


    |-- setting.json
    |-- DcardCrawler.py
    |-- main.py
    |-- data
        |-- dressup
            |-- article1
                |-- XXX1.jpg
                |-- XXX2.jpg
                .........
            |-- article2
                |--YYY1.jpg
                |--YYY2.jpg
                ........
            ........
        
<!-- ## 必要的背景
需要能夠了解python的for指令、IO操作、讀懂API文件、pandas基礎操作 -->

---

## 文件資料來源
[DCARD API官方文件](https://blog.jiatool.com/posts/dcard_api_v2/)

---
###### tags: `python` `爬蟲` `Dcard API` 
