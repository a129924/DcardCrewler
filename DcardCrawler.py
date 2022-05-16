import requests
import json
import os
import urllib.request
from fake_useragent import UserAgent
import pandas as pd
import time ,re

class DcardCrawler:
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
    def __init__(self, get_path: str = "GET_ALL_POSTS", forums: str = None, post_id: int = None, **method):  # str
        with open("setting.json") as f:
            common_formats = json.load(f)
            
        try:
            if get_path == "GET_ALL_POSTS":
                self.url = f"{common_formats[get_path]}"
            elif forums and post_id:
                raise IndexError("引數過多")
            elif (get_path == "GET_FORUMS_POSTS" and forums) or (get_path != "GET_FORUMS_POSTS" and post_id):
                self.url = f"{common_formats[get_path]}{self._mix_url_params(method)}"
                
                if "{post_id}" in common_formats[get_path]:
                    self.url = f"{common_formats[get_path].replace('{post_id}', post_id)}{self._mix_url_params(method)}"
                elif "{forums}" in common_formats[get_path]:
                    self.url = f"{common_formats[get_path].replace('{forums}', forums)}{self._mix_url_params(method)}"
                
                self.forums, self.post_id, self.method = forums, post_id, method
            else:
                raise IndexError("參數不足")
        except IndexError as error:
            print(f"引發異常: {repr(error)}")
            
    # 把引入的參數 變成網址路徑
    def _mix_url_params(self, methods:dict) -> str: # str #V
        parameter = "&".join(map(str, [f"{key}={str(value).lower()}" for key, value in methods.items() if key in ["popular", "limit", "after"]]))
        return f"?{parameter}" if len(parameter) > 0 else ""
    
    # 把API回傳的 轉成json格式
    def getDardApi(self) -> json:  # json #V
        # dressup
        ua = UserAgent()
        response = requests.get(self.url, headers={'user-agent': ua.random})

        try:
            if "error" in json.loads(response.text):
                raise ValueError("無此看板或文章編號")
            else:
                self.data = json.loads(response.text)
        except ValueError as error:
            print(f"引發異常: {repr(error)}")

        return self.data
    
    # 篩選出需要的欄位
    def _json_to_dataframe(self)->pd.DataFrame: return pd.DataFrame(self.data, columns=[
        "id", 'title', "forumAlias", "commentCount", "likeCount", "gender", "school", "media"])  # V
    # 把沒有media及作者去除
    def data_cleaning(self) -> pd.DataFrame: # V
        df = self._json_to_dataframe()
        # data_cleaning_json: dict[str:str,str:list(str)] = {}
        self._df_mask = df[(df["media"].str.len() != 0) & (df["school"] != "客服小天使")]
        
        return self._df_mask
    
    # 判斷路徑是否合法

    def _isLegalPath(self, filepath:str) -> bool:
        """
        True:path為正確的檔案路徑
        False:path為錯誤的檔案路徑
        """
        HomeDrive, HomePath = os.path.splitdrive(filepath)

        if not HomeDrive:
            filepath = os.path.join(os.getcwd(), HomePath[2:])

        re_path = r'^(?P<path>(?:[a-zA-Z]:)?\\(?:[^\\\?\/\*\|<>:"]+\\)+)' \
            r'(?P<filename>(?P<name>[^\\\?\/\*\|<>:"]+?)|\.' \
            r'(?P<ext>[^.\\\?\/\*\|<>:"]+))$'

        path_flag = re.search(re_path, filepath)

        return path_flag is not None
    
    # 判斷路徑是否存在 存在回傳True
    def _file_is_exists(self, filepath: str) -> bool: return os.path.isfile(filepath) # V
    
    # 判斷檔案是否存在 存在回傳True
    def _folder_is_exists(self, folder_name: str) -> bool: return os.path.isdir(folder_name) # V
    
    # 把結果download成json檔存在路徑
    def json_to_file(self, filepath: str = "data", filename: str = "dcard"):  # V
        assert self._isLegalPath(filename), f"檔案路徑錯誤: {filename}"
        
        data = self.data
        #判斷資料夾是否存在
        if not self._folder_is_exists(filepath):
            os.makedirs(filepath)
        filename = f"{filename}.json"
        #寫進本地端
        with open(os.path.join(filepath, filename), 'w+', encoding='utf-8') as json_file:
            json_file.write(json.dumps(data, ensure_ascii=False))
            
    # 設定路徑 檔案名稱
    def _set_download_filepath(self, title: str, img_url: str, download_location: str) -> tuple: # V #tuple[str,str,str]
        folder_name = f"{download_location}\{self.forums}\{title}"
        file_name = img_url.split('/')[-1]
        filepath = os.path.join(folder_name, file_name)
        
        return folder_name, file_name, filepath
    
    # 下載圖片
    def _download_img(self, title: str, img_url: str, download_location: str): # V
        folder_name, file_name, filepath = self._set_download_filepath(title, img_url, download_location)

        try:
            if self._file_is_exists(filepath) is False:
                if self._folder_is_exists(folder_name) is False:
                    os.makedirs(folder_name)
                
                print(f'{img_url} 下載中...')
                urllib.request.urlretrieve(img_url, filepath)
                print(f'{file_name} 成功下載')
                
        except OSError as error:
            print(f"filepath: {filepath}")
            print(f"error: {error}")
            error_dict = {}
            
    # 執行download_img
    def run_download_img(self, download_location: str = r'.\data') -> None:  # V
        # dowload_location帶入參數 必須帶r'downloadlocation'
        # download_location若是不帶HomeDrive 則會存在執行檔所在的download_location中
        assert self._isLegalPath(download_location), f"檔案路徑錯誤:'{download_location}'"
        count = 0
        start_time = time.time()
        
        for i in self._df_mask.index:
            title = eval(repr(self._df_mask["title"][i].replace(">", "").replace("<", "").replace("*", "")).replace('\\', '').replace(".", "·").replace("/",""))

            for url in self._df_mask["media"][i]:
                img_url = url["url"]
                filepath = self._set_download_filepath(title, img_url, download_location)[2] # folder_name, file_name, filepath
                
                if "imgur" in img_url and (self._file_is_exists(filepath) is False):
                    time.sleep(1)
                    
                    self._download_img(title, url["url"], download_location)
                    count += 1

        end_time = time.time()
        print(f"總計下載{count}個檔案,共計花費{end_time - start_time:.2f}秒")