import requests
from bs4 import BeautifulSoup

# 目標網站的 URL
url = "https://www.kmuh.org.tw/Web/WebRegistration/OPDSeq/ProcessMain?lang=tw"

# 發起 HTTP 請求獲取網頁內容
response = requests.get(url)

# 檢查請求是否成功
if response.status_code == 200:
    print("網頁請求成功！")
    
    # 使用 BeautifulSoup 解析 HTML 內容
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 假設所有門診進度的區域包含在 id 為 "ListBlock" 的 div 中
    list_block_div = soup.find("div", {"id": "ListBlock"})
    
    # 檢查是否找到了相應的 div
    if list_block_div:
        # 提取所有門診進度信息
        clinic_schedules = list_block_div.find_all("div", {"class": "SeqDeptItem"})
        
        # 檢查是否找到了門診進度信息
        if clinic_schedules:
            print("門診進度信息：")
            for i, clinic_schedule in enumerate(clinic_schedules, 1):
                # 提取門診名稱
                clinic_name = clinic_schedule.find("div", {"class": "SeqDeptTitle"}).text.strip()
                # 提取門診號碼
                clinic_number = clinic_schedule.find("span", {"class": "Title CurrentSeq"}).text.strip()
                print(f"{i}. {clinic_name} 的門診號碼為：{clinic_number}")
            
            # 讓使用者選擇門診
            selected_index = input("請輸入您想要查詢的門診編號：")
            
            # 檢查使用者輸入是否有效
            if selected_index.isdigit() and 1 <= int(selected_index) <= len(clinic_schedules):
                selected_clinic = clinic_schedules[int(selected_index) - 1]
                clinic_name = selected_clinic.find("div", {"class": "SeqDeptTitle"}).text.strip()
                clinic_number = selected_clinic.find("span", {"class": "Title CurrentSeq"}).text.strip()
                print(f"您選擇了查詢 {clinic_name} 門診的資訊。門診號碼為：{clinic_number}")
                
                # 在這裡可以繼續編寫程式碼，根據使用者的選擇，發送相應的通知。
            else:
                print("無效的門診編號。")
        else:
            print("未找到門診進度信息。")
    else:
        print("未找到包含所有門診進度的相應 div 元素。")
else:
    print("網頁請求失敗，錯誤碼：", response.status_code)
