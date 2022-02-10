import random


class UrlManage(object):

    def __init__(self):
        pass

    @staticmethod
    def buildUrl(url):
        return url

    @staticmethod
    def buildStaticUrl(url):
        ver = random.randint(1000, 9999)
        path = "/static" + url + "?ver=%s" % ver
        return UrlManage.buildUrl(path)
