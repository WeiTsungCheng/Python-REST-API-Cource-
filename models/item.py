
# 透過 SQLAlchemy 與database溝通， 不需要透過 sqlite3
# import sqlite3

from db import db

#  在class 中加入 db 這個參數， 表是用這個class 擴充db
class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # 到小數第二位
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # db.Integer 就是store.py id的型別， stores.id 表示 在stores TABLE 中的 id Column
    # 這裡是用ForeignKey 因為指的是另外一個 相關聯TABLE上的id
    # 這個Model 無法 delete 這個store ， 因為用的是 oreignKey 引用，某種程度上來說增添了安全性
    # 在這裡添加 store_id ，是為了做到，我們所屬於哪個store，這樣才能找到是哪一個store

    # 其實用 SQL 做join 可以達到類似效果，但是不需要這麼做，因為 SQLAlchemy 將會為我們做)
    # 我們需要做的僅是如下，因為在這裡我們已經有store_id ，所以可以在database中找到相對應的store.id 的store
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):

        # 這裡的query 是 db.Model已經定義好的
        # 使用 db.Model 中的query， 我們可以省去寫 sqlite3 的語法  "SELECT * FROM items WHERE name=name LIMIT 1"

        # 重點:
        # SQLAlchemy的好處是，會直接拿到 ItemModel 的物件，而不是dictionary

        # 以下寫法都可以
        # return ItemModel.query.filter_by(name=name).filter_by(id=1)
        # return ItemModel.query.filter_by(name=name,id=1)
        # return ItemModel.query.filter_by(name=name).first()

        return cls.query.filter_by(name=name).first()
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     # return cls(row[0], row[1])
        #     return cls(*row)

    def save_to_db(self):

        # 重點:
        # SQLAlchemy 可以把 object 直接轉換成row 到database

        # session 指得是，即將被寫入database 的物件集合

        # 思考
        # 若我們根據id(唯一不會重複的值)  將db 中的某一筆 item 取出，然後加入session, 此時 SQLAlchemy 將會 update ， 而非 insert
        # 因此 我們不需要分別 insert 和 update 兩個方法， 統一為 def save_to_db 這個方法

        db.session.add(self)
        db.session.commit()

        # 為item 新增加一個delete 的方法
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
