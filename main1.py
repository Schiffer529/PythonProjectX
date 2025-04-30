import os
from bs4 import BeautifulSoup

# 设置 HTML 文件夹路径和输出 TXT 文件路径
source_dir = "C:/Users/26755/Desktop/Python3.7/"
output_file = os.path.join(source_dir, "douban_extracted.txt")

# 打开输出文件用于写入
with open(output_file, "w", encoding="utf-8") as out:
    for file_name in os.listdir(source_dir):
        if not file_name.endswith(".html"):
            continue  # 跳过非 HTML 文件

        file_path = os.path.join(source_dir, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "lxml")
        movie_items = soup.select("ol.grid_view li")  # ⭐️ 获取电影项

        for movie in movie_items:
            try:
                # 获取标题
                title_tag = movie.find("span", class_="title")
                if not title_tag:
                    print(f"[跳过] 未找到标题：{file_name}")
                    continue
                title = title_tag.get_text(strip=True)

                # 评分
                rating_tag = movie.find("span", class_="rating_num")
                rating = rating_tag.get_text(strip=True) if rating_tag else ""

                # 评论人数
                star_div = movie.find("div", class_="star")
                comment_text = star_div.find_all("span")[-1].get_text(strip=True) if star_div else ""
                comment_num = ''.join(filter(str.isdigit, comment_text))

                # 导演与主演
                p_tag = movie.find("div", class_="bd").find("p")
                info_text = p_tag.get_text(strip=True) if p_tag else ""
                director, actor = "", ""
                if "导演" in info_text:
                    parts = info_text.split("主演:")
                    director = parts[0].replace("导演:", "").strip()
                    if len(parts) > 1:
                        actor = parts[1].strip()

                # 年份 / 国家 / 类型
                lines = p_tag.get_text().split("\n") if p_tag else []
                last_line = lines[-1].strip() if len(lines) > 1 else ""
                detail_parts = last_line.split("/")
                year = detail_parts[0].strip() if len(detail_parts) > 0 else ""
                country = detail_parts[1].strip() if len(detail_parts) > 1 else ""
                genre = detail_parts[2].strip() if len(detail_parts) > 2 else ""

                # 图片链接
                img_tag = movie.find("img")
                pic_link = img_tag.get("src") if img_tag else ""

                # 写入到 TXT 文件
                out.write(f"{title}\t{rating}\t{comment_num}\t{director}\t{actor}\t{year}\t{country}\t{genre}\t{pic_link}\n")
                print(f"[成功] 写入：{title}")

            except Exception as e:
                print(f"[跳过] 某部电影解析失败：{e}")
