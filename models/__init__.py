# 重要備註:
# 如果對於一些比較舊的python 版本， 沒有在folder 裡面添加 __init__.py
# 則foder 裡面的檔案無法被讀取
# python 3.5 以後已經修正了這個問題

# 重要觀念 -> model is our internal representation of an entity
# 對於內部而言(例如security.py)，則是與model(例如 class User) 相互作用
# 這樣一來不會污染到resourses 對外的作用
