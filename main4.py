"""
Flask 应用程序：用户登录 + 按年份搜索电影标题

- 使用 Peewee ORM 连接 MySQL 数据库
- 显示登录页面，验证用户名密码
- 提供年份输入框，返回符合条件的电影名称列表
"""

from flask import Flask, render_template, request, redirect, url_for
from peewee import MySQLDatabase, Model, CharField, IntegerField

# ======= 数据库配置 =======
DB_CONFIG = {
    'database': 'spider',
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',  # 请替换为你的真实密码
    'charset': 'utf8mb4'
}

db = MySQLDatabase(**DB_CONFIG)


# pylint: disable=too-few-public-methods
class DoubanMovie(Model):
    """豆瓣电影模型：用于查询电影标题与年份"""
    title = CharField()
    year = IntegerField()

    class Meta:
        database = db
        table_name = 'douban_movie'


app = Flask(__name__)


@app.route('/')
def home():
    """主页视图"""
    return render_template('home.html')


@app.route('/signin', methods=['GET'])
def signin_form():
    """登录表单页面"""
    return render_template('form.html', message=None, username='')


@app.route('/signin', methods=['POST'])
def signin():
    """处理登录请求"""
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'password':
        return redirect(url_for('search'))
    return render_template('form.html', message='用户名或密码错误', username=username)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """按年份搜索电影标题"""
    if request.method == 'POST':
        year_input = request.form.get('year', '').strip()
        if not year_input.isdigit():
            return render_template('search.html', error='请输入合法的年份', results=[])

        year = int(year_input)
        query_result = DoubanMovie.select().where(DoubanMovie.year == year)
        movies = list(query_result)  # 显式转为可迭代对象
        titles = [movie.title for movie in movies]
        return render_template('search.html', year=year, results=titles, error=None)

    return render_template('search.html', results=[], error=None)


if __name__ == '__main__':
    db.connect()
    app.run(debug=True)
