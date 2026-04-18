import streamlit as st
import streamlit.components.v1 as components
import os

# 設定網頁標題與圖示
st.set_page_config(page_title="009805 監控站", layout="wide")

# 1. 定位 index.html 的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(current_dir, "index.html")

# 2. 檢查檔案是否存在並讀取
if os.path.exists(index_path):
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # 3. 將 GitHub Actions 算好的 HTML 直接渲染到 Streamlit 中
    # padding=0 確保網頁全滿，不會有奇怪的邊框
    components.html(html_content, height=2000, scrolling=True)
else:
    st.error("找不到 index.html 資料檔，請確認 GitHub Actions 是否已執行成功。")
    st.info("目前的目錄檔案清單：" + str(os.listdir(current_dir)))
