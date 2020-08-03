#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import web


class PageModule(web.UIModule):

    def render(self, page, page_total, base_url, openid='', user_name='', dt='', tp='', pay_type='', max_display=20):
        return self.render_string('ui-mod/page-module.tpl',
            page=page,
            page_total=page_total,
            base_url=base_url.format(openid, user_name, dt=dt, tp=tp, pay_type=pay_type),
            max_display=max_display)


class JmpModule(web.UIModule):

    def render(self, data, t='sp'):
        return self.render_string('ui-mod/jmp-module.tpl', data=data, t=t)
