from service.base import BaseHandler
from utils.account import authenticate


class LoginHandler(BaseHandler):
    async def get(self, *args, **kwargs):
        if self.current_user:  # 若用户已登录
            self.redirect('/')  # 那么直接跳转到主页
        else:
            nextname = self.get_argument('next', '')  # 将原来的路由赋值给nextname
            self.render('login.html', nextname=nextname)  # 否则去登录界面

    async def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        passed = authenticate(username, password)

        if passed:
            self.session.set('user_info', username)  # 将前面设置的cookie设置为username，保存用户登录信息
            next_url = self.get_argument('next', '')  # 获取之前页面的路由

            if next_url:
                self.redirect(next_url)  # 跳转主页路由
            else:
                self.redirect('/')
        else:
            self.write({'msg': 'login fail'})  # 不通过，有问题
