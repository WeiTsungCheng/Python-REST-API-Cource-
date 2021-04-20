from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # 反向來說 StoreModel 也可以知道是哪一個model 和它建立關係
    # 因為可以有多個ItemModel 物件 都持有StoreItem (多對一)， 所以這理的 items 指的是多個 ItemModel 物件

    # 重要但是常常被忽略:
    # 每當我們create 一個 StoreModel 就需要產生相對應的 ItemModel去 match 其store.id
    # 這將會造成大量的運行成本
    # 所以我們加上 lazy ='dynamic'， 要SQLALCHEMY 不要產生每一個相對應的 ItemModel object

    # 重要:
    # 當我們加上 lazy ='dynamic' 時，items 就不再是 items 的 list ，而是 query builder, 具有能力去查看 items table
    # 所以需要加上 .all() 去取得每一個item
    # 這也就是說，直到call def json 之前，都不會調查 table ， 這也表示create StoreModel 所做的事變簡單了
    # 但是當 使用 def json 時， 就需要查看 所有items

    # 所以這是一個取捨，是要在創建StoreModel快一點，或是call def JSON這方法時快一點(如果不使用lazy 則在創建時就會acess 每一個item，會慢一點，但之後再訪問很快)
    # 以目前這個專案來說，我們create StoreModel (即store)的時機 ，是在要取得資料的時機，所以採用目前的方式
    items = db.relationship('ItemModel', lazy ='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
