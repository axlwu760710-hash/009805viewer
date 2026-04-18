import yfinance as yf
import pandas as pd
import datetime
import os

# 1. 定位 index.html 的路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(current_dir, "index.html")

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
    # 抓取數據
    tickers = list(COMPONENTS.keys()) + ["TWD=X"]
    data = yf.download(tickers, period="2d", interval="1d", progress=False)['Close']
    
    if data.empty or len(data) < 2:
        return

    latest, prev = data.iloc[-1], data.iloc[-2]
    rows_html = ""
    total_impact = 0
    
    for t, weight in COMPONENTS.items():
        if t in latest and t in prev:
            change = (latest[t] - prev[t]) / prev[t]
            impact = change * weight
            total_impact += impact
            color = "#22c55e" if change >= 0 else "#ef4444"
            rows_html += f'<tr><td><b style="color:#38bdf8;">{t}</b></td><td style="color:{color}">{change:+.2%}</td><td>{weight:.2%}</td><td style="color:{color}">{impact:+.4%}</td></tr>'
    
    usd_change = (latest["TWD=X"] - prev["TWD=X"]) / prev["TWD=X"]
    final_total = total_impact + usd_change
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- 終極修正：直接「生成」整份 HTML，不依賴舊檔案內容，不使用 replace ---
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>009805 戰情室</title></head>
    <body style="background-color: #0f172a; color: white; font-family: sans-serif; padding: 20px;">
        <h2>⚡ 009805 成分股即時估算</h2>
        <p>最後更新：{now_str}</p>
        <div style="display:flex; gap:20px; font-size:20px; margin-bottom:20px;">
            <div>美股影響: <b style="color:#38bdf8;">{total_impact:+.2%}</b></div>
            <div>匯率影響: <b style="color:#38bdf8;">{usd_change:+.2%}</b></div>
            <div>預估總計: <b style="color:#22c55e;">{final_total:+.2%}</b></div>
        </div>
        <table border="1" style="width:100%; border-collapse:collapse; background-color:#1e293b;">
            <thead><tr style="background:#334155;"><th>代號</th><th>漲跌</th><th>權重</th><th>貢獻</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </body>
    </html>
    """

    # 直接強制蓋寫 index.html，不管裡面本來有什麼
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    
    print(f"✅ 數據已強制重寫：{now_str}")

if __name__ == "__main__":
    run()
