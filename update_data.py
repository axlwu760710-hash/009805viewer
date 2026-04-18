import yfinance as yf
import pandas as pd
import datetime
import os

# 1. 鎖定檔案路徑 (確保程式能看到同資料夾的 index.html)
current_dir = os.path.dirname(os.path.abspath(__file__))
index_path = os.path.join(current_dir, "index.html")

# 2. 你的 50 檔權重數據 (此處省略部分清單，請維持你原本的完整 50 檔)
COMPONENTS = {
    "GEV": 0.1265, "VRT": 0.0975, "ETN": 0.0912, "PWR": 0.0635, "HUBB": 0.0610,
    # ... 請保留你原本完整的 50 檔清單 ...
}

def run():
    # 3. 抓取數據 (美股 50 檔 + 匯率)
    tickers = list(COMPONENTS.keys()) + ["TWD=X"]
    data = yf.download(tickers, period="2d", interval="1d", progress=False)['Close']
    
    if data.empty or len(data) < 2:
        print("數據同步中或今日未開盤")
        return

    latest, prev = data.iloc[-1], data.iloc[-2]
    rows = ""
    total_impact = 0
    
    for t, weight in COMPONENTS.items():
        if t in latest and t in prev:
            change = (latest[t] - prev[t]) / prev[t]
            impact = change * weight
            total_impact += impact
            color = "#22c55e" if change >= 0 else "#ef4444"
            rows += f'<tr><td><span class="ticker">{t}</span></td><td style="color:{color}">{change:+.2%}</td><td><span class="weight-tag">{weight:.2%}</span></td><td style="color:{color}; font-weight:bold;">{impact:+.4%}</td></tr>'
    
    usd_change = (latest["TWD=X"] - prev["TWD=X"]) / prev["TWD=X"]
    final_total = total_impact + usd_change
    
    # 4. 寫入 HTML (關鍵：如果檔案不在會報錯)
    if not os.path.exists(index_path):
        print(f"錯誤：在 {current_dir} 找不到 index.html")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # 替換標籤內容
    html = html.replace("", f"{total_impact:+.2%}")
    html = html.replace("", f"{usd_change:+.2%}")
    html = html.replace("", f"{final_total:+.2%}")
    html = html.replace("", rows)
    html = html.replace("", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ 數據同步成功！")

if __name__ == "__main__":
    run()
