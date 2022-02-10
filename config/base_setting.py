SERVER_PORT = 9988
DEBUG = False
SQLALCHEMY_ECHO = True

AUTH_COOKIE_NAME = "mooc_food"

## 过滤不需要权限校验的url
IGNORE_URLS = [
    "^/user/login"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static",
    "^/favicon.ico"
]

PAGE_SIZE = 10
PAGE_DISPLAY = 20