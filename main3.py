import pymysql
pymysql.install_as_MySQLdb()  # 让 pymysql 像 mysqlclient 一样用

from peewee import *

# 连接数据库
db = MySQLDatabase(
    database="spider",
    host="localhost",
    port=3306,
    user="root",
    password="123456",  # 这里填写你的MySQL密码
    charset='utf8mb4'
)

# 定义表结构
class DoubanMovie(Model):
    title = CharField(max_length=100)
    rating = FloatField()
    comment_num = IntegerField()
    director = TextField()
    actor = CharField(max_length=100)
    year = IntegerField()
    country = CharField(max_length=50)
    genre = CharField(max_length=100, null=True)  # genre 字段
    pic_link = TextField(null=True)  # pic_link 字段

    class Meta:
        database = db
        table_name = 'douban_movie'

# 创建表
db.connect()
db.create_tables([DoubanMovie])

# 读取 txt 文件并插入数据
def save_movies_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # 假设格式是 tab 分隔：标题\t评分\t评论数\t导演\t演员\t年份\t国家\t类型\t图片链接
            parts = line.strip().split("\t")
            if len(parts) < 7:
                continue  # 跳过不完整的数据
            DoubanMovie.create(
                title=parts[0],
                rating=float(parts[1]),
                comment_num=int(parts[2]),
                director=parts[3],
                actor=parts[4],
                year=int(parts[5]),
                country=parts[6],
                genre=parts[7] if len(parts) > 7 else None,  # 处理 genre 字段
                pic_link=parts[8] if len(parts) > 8 else None  # 处理 pic_link 字段
            )

# 替换成你的实际文件路径
save_movies_from_txt("C:/Users/26755/Desktop/Python3.7/douban_movies.txt")
print("写入完成！")
