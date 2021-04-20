# 這個User class用來找 user 的資料，務必和註冊的 class 不要寫在一起
# 注意! class User 不屬於Resources

import sqlite3
from db import db

# 注意！
# 整個UserModel 可以被視為一個API (p.s. 不是rest API)，一個具有兩個end point 的API
# 用來被整個程序去呼叫 ， 去處理關於user 的事項(包含資料存入或取出，從data base)
# 舉例來說 security.py 不會在乎UserModel 中 def find_by_username 是怎麼被實作的，甚至是被什麼語言所實做的，只要回傳的值是它要的

class UserModel(db.Model):
    # 給table u 一個名稱
    __tablename__ = 'users'

    # 告訴 SQLAlchemy 這個 model 將有三個 columns (如下)

    # 注意！
    # model中id這個參數，是自動產生(primary_key=True), 當我們每insert一個new row 到database
    # SQL engine (這裡用的是Lite, 也可以是Postgres, MySQL) 將會自動給我們id ，我們不需要自己產生
    # 因此當我們create 一個物件，透過 SQLALCHEMY， id 也就會自動生成
    # 所以， 我們千萬不要在 def init 中再多新增一個參數，叫id
    # 當然如果我們想要自己控制id 我們也可以選擇在def init 中，自己定一個
    id = db.Column(db.Integer, primary_key=True)
    # 限定最多 80 個 characters
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    # 這裡設定db 的欄位必須和 def __init__ 裡面的參數相對應，否則無法存到db

    def __init__(self, username, password):
        self.username = username
        self.password = password

        # 不會報錯，但是如法存到db
        # self.something = "hi"

    # 新添加一個存入database 的方法
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):

        # cls.query 會回傳一個query builder (= SELECT * FROM users)
        # query builder 僅是一個 object ，可以build queries

        # 第一個 username 指的是這個model 的 username ， 第二個username 則是此方法帶入的 username (雖然顯示的顏色不同)
        # cls.query.filter_by(username=username).first() 拿到的是UserModel object
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        # 這裡前一個id 是Model 的id， 第二個_id 是這個方法傳入的_id
        return  cls.query.filter_by(id=_id).first()


