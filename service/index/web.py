from service.base import BaseHandler


class IndexHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        self.write("<h1>Hello world!</h1>")
