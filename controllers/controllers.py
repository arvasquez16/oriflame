# -*- coding: utf-8 -*-
from odoo import http

# class Oriflame(http.Controller):
#     @http.route('/oriflame/oriflame/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/oriflame/oriflame/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('oriflame.listing', {
#             'root': '/oriflame/oriflame',
#             'objects': http.request.env['oriflame.oriflame'].search([]),
#         })

#     @http.route('/oriflame/oriflame/objects/<model("oriflame.oriflame"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('oriflame.object', {
#             'object': obj
#         })