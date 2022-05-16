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
