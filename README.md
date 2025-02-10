# **Strava GPX Uploader**
🚴‍♀️ **批量上传 Komoot/其他来源的 GPX 轨迹到 Strava，支持断点续传 & 自动限速**


## **📌 1. 安装**
### **🔹 安装 Python 依赖**
```bash
pip install requests python-dotenv
```

### **🔹 克隆代码**
```bash
git clone https://github.com/ice5555/StravaUploader.git
cd StravaUploader
```

---

## **📌 2. 运行上传**
```bash
python uploader.py
```
**✅ 第一次运行时：**
- **如果 `.env` 配置文件不存在**，会提示输入 `CLIENT_ID`, `CLIENT_SECRET`, `REFRESH_TOKEN`，并自动生成 `.env`。
- **如果 `.env` 存在但为空**，也会提示输入。

---

## **📌 3. GPX 数据文件**
**GPX 文件默认放在 `data/` 文件夹下**，脚本会**自动读取和上传**。

- **示例文件格式**
  ```
  2024-02-01_Morning_Ride-12345678.gpx
  2023-12-25_Christmas_Ride-98765432.gpx
  ```
---

## **📌 4. API 速率限制**
Strava API 限制：
- **15 分钟内最多 200 次上传**
- **每天最多 2000 次上传**
- **脚本会自动等待，防止超过速率**

---

## **📌 5. 目录结构**
```
StravaUploader/
│── data/                 # 存放 GPX 文件
│── .gitignore            
│── .env                  # 存储 API 密钥（自动生成）
│── README.md             # 说明文档
│── requirements.txt      # 依赖安装
│── importer.py           # 主要 Python 代码
│── uploaded_files.txt    # 记录已上传文件
```

---

## **📌 6. FAQ**

### **Q: 为什么我的 GPX 没有按照时间顺序上传？**
**确保 GPX 文件名包含 `YYYY-MM-DD`**，这样才能正确排序。

### **Q: 上传失败，提示 `Authorization Error`？**
**请检查 `CLIENT_ID`, `CLIENT_SECRET`, `REFRESH_TOKEN` 是否正确。**

