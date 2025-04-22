import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Accept-Encoding": "br, gzip, deflate",  # 支持 Brotli 解码
}

for page in range(10):
    start = page * 25
    url = f"https://movie.douban.com/top250?start={start}"
    print(f"📥 正在抓取第 {page + 1} 页：{url}")

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # 尝试 Brotli 解码
        try:
            import brotli

            content = brotli.decompress(response.content).decode("utf-8")
        except:
            content = response.text

        # 保存为 HTML 文件（路径为桌面 Python3.7 文件夹）
        file_path = rf"C:\Users\26755\Desktop\Python3.7\douban_top250_page{page + 1}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f" 第 {page + 1} 页保存成功：{file_path}\n")
    else:
        print(f" 第 {page + 1} 页抓取失败，状态码：{response.status_code}\n")

    time.sleep(1)  # 避免请求过快被封
