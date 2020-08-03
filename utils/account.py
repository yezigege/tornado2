import hashlib


def hash(text):
    text = hashlib.md5(text.encode()).hexdigest()  # 给密码加密，用hashlib来算法加密，utf8不加的话就是默认utf8

    return text


USER_DATA = {
    'name': 'admin',
    'password': hash('123456')
}


def authenticate(username, password):  # 用户密码匹配判断函数
    if username and password:
        hash_pwd = hash(password)
        if username == USER_DATA['name'] and hash_pwd == USER_DATA['password']:  # 是否与保存的一致
            return True

    return False
