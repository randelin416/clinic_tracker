import tkinter as tk
import requests
from bs4 import BeautifulSoup

def on_select(event):
    selected_clinic = event.widget.get()
    print("您選擇了門診：", selected_clinic)

def fetch_clinic_names():
    # 目標網站的 URL
    url = "https://www.kmuh.org.tw/Web/WebRegistration/OPDSeq/ProcessMain?lang=tw"

    # 發起 HTTP 請求獲取網頁內容
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        })

    # 檢查請求是否成功
    if response.status_code == 200:
        print("網頁請求成功！")
        
        # 使用 BeautifulSoup 解析 HTML 內容
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 假設所有門診進度的區域包含在 id 為 "ListBlock" 的 div 中
        clinicNames = soup.find("div.SeqDeptTitle > span")
        
        # 檢查是否找到了相應的 div
        if clinicNames:
            for d in clinicNames:
                print(d.text)
            # # 提取所有門診進度信息
            # clinic_schedules = list_block_div.find_all("div", {"class": "SeqDeptItem"})
            
            # # 提取門診名稱
            # clinic_names = [clinic.find("div", {"class": "SeqDeptTitle"}).text.strip() for clinic in clinic_schedules]
            # return clinic_names
        else:
            print("未找到包含所有門診名稱的相應 div 元素。")
    else:
        print("網頁請求失敗，錯誤碼：", response.status_code)

# 建立主視窗
root = tk.Tk()
root.title("門診追蹤")

# 創建下拉菜單
clinic_names = fetch_clinic_names()
if clinic_names:
    selected_clinic_var = tk.StringVar(root)
    selected_clinic_var.set(clinic_names[0])  # 預設選項
    clinic_menu = tk.OptionMenu(root, selected_clinic_var, *clinic_names, command=on_select)
    clinic_menu.pack()
else:
    tk.Label(root, text="無法獲取門診資料").pack()

# 建立 Tkinter 標籤和輸入框
tk.Label(root, text="請輸入您的電話號碼：").pack()
phone_number_entry = tk.Entry(root)
phone_number_entry.pack()

# 創建一個按鈕，當用戶點擊時觸發設定通知的方法
def set_notification():
    phone_number = phone_number_entry.get()
    print("您設定的通知電話號碼是：", phone_number)

tk.Button(root, text="設定通知", command=set_notification).pack()

# 啟動主迴圈
root.mainloop()
