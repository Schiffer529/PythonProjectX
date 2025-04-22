import os
import re
from bs4 import BeautifulSoup

# 改为你的本地 HTML 文件保存路径
dest_dir = r"C:\Users\26755\Desktop\Python3.7\douban_movies.txt"

# 遍历每个 HTML 文件
for html_file in os.listdir(dest_dir):
    if not html_file.endswith('.html'):
        continue  # 忽略非 HTML 文件
    print(f"\n📄 正在解析文件: {html_file}")
    file_path = os.path.join(dest_dir, html_file)

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()
        soup = BeautifulSoup(html, 'lxml')

        # 找到电影列表
        movie_list = soup.find('ol', class_='grid_view').find_all('li')

        for movie in movie_list:
            # 电影标题
            title = movie.find('span', class_='title').get_text(strip=True)

            # 评分
            rating = movie.find('span', class_='rating_num').get_text(strip=True)

            # 评论人数
            comment_text = movie.find_all('span')[-1].get_text()
            comment_match = re.search(r"(\d+)", comment_text)
            comment_num = comment_match.group(1) if comment_match else "0"

            # 图片链接
            img_link = movie.find('img')['src']

            # 详情页链接
            detail_link = movie.find('a')['href']

            # 信息提取：导演、主演
            p_tags = movie.find('div', class_='bd').find_all('p')
            info_line_1 = p_tags[0].get_text(strip=True)
            info_line_2 = p_tags[1].get_text(strip=True)

            # 提取导演和主演
            director = ""
            actor = ""
            match_director = re.search(r"导演: ([^\\/]+)", info_line_1)
            if match_director:
                director = match_director.group(1).strip()

            match_actor = re.search(r"主演: (.+)", info_line_1)
            if match_actor:
                actor = match_actor.group(1).strip()

            # 提取上映时间、出品地、剧情类别
            parts = [x.strip() for x in info_line_2.split("/")]
            release_year = parts[0] if len(parts) > 0 else ""
            region = parts[1] if len(parts) > 1 else ""
            genre = parts[2] if len(parts) > 2 else ""

            # 输出信息
            print(f"""
🎬 电影名：{title}
⭐ 评分：{rating}
🗣️ 评论人数：{comment_num}
🎥 导演：{director}
👤 主演：{actor}
📅 上映时间：{release_year}
🌍 出品地：{region}
📚 剧情类别：{genre}
🔗 电影链接：{detail_link}
🖼️ 封面链接：{img_link}
""")
