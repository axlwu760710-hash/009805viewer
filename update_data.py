import yfinance as yf
import pandas as pd
import datetime
import os

# 1. 定位檔案
current_dir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(current_dir, "index.html")

# 【在這裡修改你的起始正確權重】
# 只要改這一次，之後程式會根據漲跌自動計算權重偏移
BASE_COMPONENTS = {
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
    tickers = list(BASE_COMPONENTS.keys()) + ["TWD=X"]
    data = yf.download(tickers, period="2d", interval="1d", progress=False)['Close']
    
    if data.empty or len(data) < 2: return
    latest, prev = data.iloc[-1], data.iloc[-2]
    
    # --- 關鍵：計算動態權重偏移 ---
    temp_weights = {}
    total_val = 0
    for t, base_w in BASE_COMPONENTS.items():
        # 模擬：原始權重 * (今日價格 / 昨日價格) = 今日實際權重占比
        current_val = base_w * (latest[t] / prev[t])
        temp_weights[t] = current_val
        total_val += current_val

    rows_html = ""
    total_impact = 0
    
    for t in BASE_COMPONENTS.keys():
        # 重新標準化，確保總和是 100%
        real_time_weight = temp_weights[t] / total_val
        change = (latest[t] - prev[t]) / prev[t]
        impact = change * real_time_weight
        total_impact += impact
        
        color = "#22c55e" if change >= 0 else "#ef4444"
        rows_html += f'<tr><td><b style="color:#38bdf8;">{t}</b></td><td style="color:{color}">{change:+.2%}</td><td>{real_time_weight:.2%}</td><td style="color:{color}; font-weight:bold;">{impact:+.4%}</td></tr>'
    
    usd_change = (latest["TWD=X"] - prev["TWD=X"]) / prev["TWD=X"]
    final_total = total_impact + usd_change
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>009805 戰情室</title></head>
    <body style="background-color: #0f172a; color: white; font-family: sans-serif; padding: 20px;">
        <h2 style="color:#38bdf8;">⚡ 009805 動態權重監控</h2>
        <p style="color:#94a3b8;">最後更新：{now_str} (每早自動同步)</p>
        <div style="display:flex; gap:20px; font-size:20px; margin-bottom:20px; background:#1e293b; padding:15px; border-radius:10px;">
            <div>美股影響: <b style="color:#38bdf8;">{total_impact:+.2%}</b></div>
            <div>匯率(台幣): <b style="color:#fcd34d;">{usd_change:+.2%}</b></div>
            <div style="border-left:2px solid #334155; padding-left:20px;">預估總計: <b style="color:#22c55e;">{final_total:+.2%}</b></div>
        </div>
        <table border="1" style="width:100%; border-collapse:collapse; background-color:#1e293b; border:none;">
            <thead><tr style="background:#334155; color:#94a3b8;"><th>代號</th><th>今日漲跌</th><th>即時權重</th><th>貢獻度</th></tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
    </body>
    </html>
    """
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"✅ 動態數據更新完成：{now_str}")

if __name__ == "__main__": run()
