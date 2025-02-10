import os
import requests
import time
from datetime import datetime
from dotenv import load_dotenv

# 获取 Strava API 认证信息
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

# 文件夹路径
GPX_FOLDER = "./data"  
UPLOADED_LOG = "uploaded_files.txt"

def setup_env():
    global CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN

    print("\n🔹 检测到 .env 文件丢失或为空，开始交互式配置 🔹")
    CLIENT_ID = input("请输入 Strava CLIENT_ID: ").strip()
    CLIENT_SECRET = input("请输入 Strava CLIENT_SECRET: ").strip()
    REFRESH_TOKEN = input("请输入 Strava REFRESH_TOKEN: ").strip()

    # 保存到 .env
    with open(".env", "w") as f:
        f.write(f"CLIENT_ID={CLIENT_ID}\n")
        f.write(f"CLIENT_SECRET={CLIENT_SECRET}\n")
        f.write(f"REFRESH_TOKEN={REFRESH_TOKEN}\n")

    print("\n✅ API 配置完成！已生成 .env 文件。\n")

if not CLIENT_ID or not CLIENT_SECRET or not REFRESH_TOKEN:
    setup_env()

def get_access_token():
    response = requests.post("https://www.strava.com/oauth/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    })
    return response.json().get("access_token", None)

def get_uploaded_files():
    if not os.path.exists(UPLOADED_LOG):
        return set()
    with open(UPLOADED_LOG, "r") as f:
        return set(f.read().splitlines())

def save_uploaded_file(file_name):
    with open(UPLOADED_LOG, "a") as f:
        f.write(file_name + "\n")

def get_gpx_files_sorted():
    gpx_files = [f for f in os.listdir(GPX_FOLDER) if f.endswith(".gpx")]
    
    def extract_date(file_name):
        try:
            date_str = file_name.split("_")[0]  
            return datetime.strptime(date_str, "%Y-%m-%d")
        except:
            return datetime.min  

    return sorted(gpx_files, key=extract_date, reverse=True)

def upload_gpx_to_strava():
    access_token = get_access_token()
    if not access_token:
        print("❌ 获取 Access Token 失败！")
        return

    headers = {"Authorization": f"Bearer {access_token}"}
    uploaded_files = get_uploaded_files()
    uploaded_count = 0

    for file_name in get_gpx_files_sorted():
        if file_name not in uploaded_files:
            file_path = os.path.join(GPX_FOLDER, file_name)
            print(f"📤 上传 {file_name} 到 Strava...")

            with open(file_path, "rb") as gpx_file:
                response = requests.post(
                    "https://www.strava.com/api/v3/uploads",
                    headers=headers,
                    files={"file": gpx_file},
                    data={"data_type": "gpx"}
                )

            if response.status_code == 201:
                upload_id = response.json().get("id", "未知")
                print(f"✅ 上传成功！Upload ID: {upload_id}")
                save_uploaded_file(file_name)
            else:
                print(f"❌ 上传失败！错误信息: {response.json()}")

            uploaded_count += 1
            if uploaded_count % 180 == 0:
                print("⏳ 等待 15 分钟，避免 API 限制...")
                time.sleep(900)
            else:
                time.sleep(5)

upload_gpx_to_strava()
