from tornado.web import authenticated

from service.base import BaseHandler


class IndexHandler(BaseHandler):
    @authenticated
    async def get(self, *args, **kwargs):
        self.render('index.html')
        self.write("<h1>Hello world!</h1>")
