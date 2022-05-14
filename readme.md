---
Title: Dcard爬蟲機器人
Date: 2020/05/14 22:45

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
建置好環境後，放置在路徑底下，並創建`main.py`

    |-- setting.json
    |-- DcardCrawler.py
    |-- main.py

### 簡單實例
假如現在要下載穿塔版熱門前一百大文章的圖片
```python=
#==============================main.py=====================================
# 載入套件
import DcardCrawler

# 初始化程式
data = DcardCrawler(get_path="GET_FORUMS_POSTS",
                          forums="dressup", popular=True, limit=100)
# 將取得的資料轉換成dataframe
data.data_cleaning()
# 執行下載圖片
data.run_download_img()

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