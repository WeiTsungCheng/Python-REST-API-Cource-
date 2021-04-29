# Python-REST-API-Cource-

Udemy 課程 https://www.udemy.com/course/rest-api-flask-and-python
課程線上文件: https://arac.tecladocode.com/

有上傳 heroku 進行操作

1. Section 6 ok
2. Section 8 使用 heroku postgres sql 出現 heroku 出現 H13錯誤 503.

解決方法 uwsgi -> gunicorn 
requirements 添加 SQLAlchemy, gunicorn 

但會出現 Internal Server Error 500
原因出在 SQLAlchemy==1.4.7 , SQLAlchemy 1.4.x has removed support for the postgres://

解法
import os
import re

uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

參考
https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres


3. Seciton 11

使用 @jwt_required 將會出錯 
因為 Flask-JWT-Extended 在 4.0.0 版 將  @jwt_required  改為 @jwt_required(), 還有其他的改變不一一列舉 詳情參考以下文件
參考
https://flask-jwt-extended.readthedocs.io/en/stable/v4_upgrade_guide/
