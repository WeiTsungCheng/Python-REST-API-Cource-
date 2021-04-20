# 透過 SQLAlchemy 與database溝通， 不需要透過 sqlite3
# import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    # 新增必要參數store_id
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item need a store id"
    )

    @jwt_required()
    def get(self, name):

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        #
        # if row:
        #     return  {'item': {'name': row[0], 'price': row[1]}}
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return  {'message': 'Item not found'}, 404

        # 因為 def get 需要JWT token, def post . 無法直接 self.get 去確認這個name item 是否以存在
        # 所以 新增底下的@classmethod 來解決這個問題
        # 並且讓 def get 和 def post 共用這個方法

    def post(self, name):

        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exisit".format(name)}, 400

        data = Item.parser.parse_args()

        #補上 stores_id 這個參數
        # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)
        # 重要觀念:
        # 這理將可能的insert失敗，做error handling
        # 例如 connection.commit() 發生錯誤
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item"}, 500 # Internal Server Error

        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message' : 'Item Delete' }

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        # update_item = ItemModel(name, data['price'])


        if item is None:
            # item = ItemModel(name, data['price'], data['store_id'])
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        # 當沒有這個名子的item,則就加入到data base
        # 當存在這個名子的item,因為帶有特定的id 作為primary_key，所以添加到data base 時，不會新增一個，而是更新原來那個
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required()
    def get(self):
        # return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {'items': [x.json() for x in ItemModel.query.all()]}

        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # items = []
        #
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
        #
        # # 這裡不需要 commit 因為並沒有儲存任何東西
        # # connection.commit()
        # connection.close()
        #
        # return {'items': items}

# 補充小知識:
# function 之間通常會留一行空行，而class 之間會留兩行
