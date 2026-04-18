import yfinance as yf
import pandas as pd
import datetime
import os

# 1. 定位路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(current_dir, "index.html")

# 2. 成分股權重 (請根據最新權重微調)
COMPONENTS = {
    "GEV": 0.1265, "VRT": 0.0975, "ETN": 0.0912, "PWR": 0.0635, "HUBB": 0.0610,
    "NEE": 0.0418, "SO": 0.0355, "DUK": 0.0332, "NXT": 0.0275, "D": 0.0235,
    "AEP": 0.0232, "BE": 0.0222, "FSLR": 0.0205, "ED": 0.0182, "SWX": 0.0179,
    "AGX": 0.0175, "EXC": 0.0162, "MTZ": 0.0156, "PEG": 0.0135, "CEG": 0.0125,
    "EIX": 0.0124, "WEC": 0.0124, "TTEK": 0.0123, "POWL": 0.0121, "ES": 0.0116,
    "ACM": 0.0114, "ETR": 0.0112, "XEL": 0.0104, "ENS": 0.0101, "FE": 0.0098,
    "PPL": 0.0094, "GNRC": 0.0090, "VST": 0.0076, "DTE": 0.0068, "AEE": 0.0067,
    "EVRG": 0.0063, "VICR": 0.0058, "PNW": 0.0054, "CMS": 0.0053, "OGE": 0.0045,
    "PCG": 0.0044, "CNP": 0.0042, "NRG": 0.0042, "LNT": 0.0042, "ENPH": 0.0038,
    "AES": 0.0034, "ITRI": 0.0031, "AMSC": 0.0024, "MEI": 0.0007, "MVST": 0.0003
}

def run():
    # 3. 抓取數據
    tickers = list(COMPONENTS.keys()) + ["TWD=X"]
    data = yf.download(tickers, period="2d", interval="1d", progress=False)['Close']
    
    if data.empty or len(data) < 2:
        print("數據同步中或非開盤日...")
        return

    latest, prev = data.iloc[-1], data.iloc[-2]
    rows_list = []
    total_impact = 0
    
    # 4. 計算權重貢獻
    for t, weight in COMPONENTS.items():
        if t in latest and t in prev:
            change = (latest[t] - prev[t]) / prev[t]
            impact = change * weight
            total_impact += impact
            color = "#22c55e" if change >= 0 else "#ef4444"
            rows_list.append(f'<tr><td><span class="ticker">{t}</span></td><td style="color:{color}">{change:+.2%}</td><td>{weight:.2%}</td><td style="color:{color}; font-weight:bold;">{impact:+.4%}</td></tr>')
    
    usd_change = (latest["TWD=X"] - prev["TWD=X"]) / prev["TWD=X"]
    final_total = total_impact + usd_change
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 5. 讀取與安全置換
    if not os.path.exists(index_path):
        print(f"錯誤：找不到 {index_path}")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # --- 關鍵修正：檢查標籤是否存在，絕對不使用空字串 ---
    mapping = {
        "": f"{total_impact:+.2%}",
        "": f"{usd_change:+.2%}",
        "": f"{final_total:+.2%}",
        "": "".join(rows_list),
        "": update_time
    }

    for tag, val in mapping.items():
        if tag in html:
            html = html.replace(tag, val)
        else:
            print(f"警告：標籤 {tag} 在 index.html 中消失了，請手動還原 index.html 模板")

    # 6. 寫回
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ 009805 數據更新成功")

if __name__ == "__main__":
    run()
