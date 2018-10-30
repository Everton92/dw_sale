# -*- coding: utf-8 -*-
from odoo import http

# class /home/everton/odoo/addons/moduleBi(http.Controller):
#     @http.route('//home/everton/odoo/addons/dw_sale//home/everton/odoo/addons/dw_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//home/everton/odoo/addons/dw_sale//home/everton/odoo/addons/dw_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/home/everton/odoo/addons/dw_sale.listing', {
#             'root': '//home/everton/odoo/addons/dw_sale//home/everton/odoo/addons/dw_sale',
#             'objects': http.request.env['/home/everton/odoo/addons/dw_sale./home/everton/odoo/addons/dw_sale'].search([]),
#         })

#     @http.route('//home/everton/odoo/addons/dw_sale//home/everton/odoo/addons/dw_sale/objects/<model("/home/everton/odoo/addons/dw_sale./home/everton/odoo/addons/dw_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/home/everton/odoo/addons/dw_sale.object', {
#             'object': obj
#         })