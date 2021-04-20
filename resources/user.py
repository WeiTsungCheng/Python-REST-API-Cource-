# 讓User class 可以使用 sqlite 的語法 和 database 相互作用
# 透過 SQLAlchemy 與database溝通， 不需要透過 sqlite3
# import sqlite3
from models.user import UserModel
# 因為需要讓使用者可以註冊，所以我們在這裡也引入from flask_restful import Resource
# 需要拿到用戶註冊的帳密 所以需要 import reqparse
from flask_restful import Resource, reqparse

# 獨立的class 用來註冊新的User
class UserRegister(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank"
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username is already exsist"}, 400

        # user = UserModel(data['username'], data['password'])
        # 從上面來看 data 用過 從parser 來，所以必定有 username 和 password 這兩個種參數
        # 因為data 這個dicitonary 對應的資料與Model相同，所以可以直接unpacking
        user = UserModel(**data)
        user.save_to_db()


        return {"message" : "User create successfully"}, 201
