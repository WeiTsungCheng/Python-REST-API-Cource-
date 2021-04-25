# -*- coding: UTF-8 —
import os

from flask import Flask
# reqparse 這方法可以讓我們限定，request 的參數一定要包含哪些
# resource  呈現我們API 可以作的事情 (return, create... )，例如這理的resource 是 Item 所以可以呈現 新增item 取item...
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
# 因為 user.py 移動到resources 資料夾(package)中，所以路徑需要修正
from resources.user import UserRegister
from resources.item import Item, ItemList

from resources.store import Store, StoreList
from db import db

# 觀念補充:
# 如果有其他的檔案將此檔app.py import 進去，將會將此檔整個跑過一次，確定每一個class和function 可以運作，
# 底下這段app 的生成沒有問題，但是最底下app.run(port=5000, debug=True) 將會出現問題
# 因為如果我們只是想import app.py， 我們並不想執行app.run(port=5000, debug=True)
# 所以加上 if __name__ == '__main__': ，當我們在terminal 執行 app.py 時， app.py 會自動被設成main ，所以if 後面的app.run會被執行
# 反之，如果其他的檔案import app.py ，則if 後面不會被執行

app = Flask(__name__)

# 告訴 app.py data base 在哪裡
# 因此 SQLALCHEMY 將會去讀 同資料層級下的data.db
# 補充 'sqlite:///data.db' 不見得需要是SQLite 換成MySQL 和 PostgreSQL 也可以work
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

# 必要:
# SQLALCHEMY_TRACK_MODIFICATIONS ，如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
# 因為 Flask 的擴充SQLAlchemy，會track 所有的改變，到 SQLAlchemy session ，這將消浩掉一些資源
# 但是 SQLAlchemy 本身，它的Library 就有modification tracker
# 總結，關閉 flask SQLAlchemy modification tracker， 但是不關閉 SQLAlchemy modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

db.init_app(app)

# @ 表示 decorator 函數
# 底下這段表示，在接收第一個 request 執行之前(任何一個)，必須先執行def create_tables()，產生data.db
# 無論 data.db 是否存在，每次重新run app.py後的第一個request執行前，這 def create_tables()就會被執行一次

# 超級重要:
# SQLAlchemy 為我們建立 TABLE， 但它只能建立，它看得到的！
# 所以必須要透過import，舉例來說，這裡app.py 需要 from resources.store import Store, StoreList
# 然後 從resources.store (即 store.py) 中再得到另一個 import  from models.store import storeModel
# 從storeModel 中，SQLAlchemy 才能知道要建立的 TABLE 有哪些 Column
# 所以如果 app.py 中沒有import Store ，這串連結ˊ將無法成立

# Flask 的 decorator, 當第一個 request 發生前執行
@app.before_first_request
def create_tables():
    print('HI~DB')
    db.create_all()

jwt = JWT(app, authenticate, identity)  # 新增加 /auth 這個endpoint

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
# 先把UserRegister import 進來 然後把它加到api resource裡面
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    # # 這裡特別注意，要import 在這裡，因為如果 import 在最上面
    # # 當之後我們的Item 物件也需要import db 時，將造成無限import問題
    app.run(port=5000, debug=True)

