- 自动生产model代码
pip install flask-sqlacodegen
flask-sqlacodegen "mysql://root:zhousir_0301@127.0.0.1/food_db" --tables user --outfile "common/models/user.py" --flask