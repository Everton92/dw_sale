# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api


class DwReport(models.Model):
    _name = 'dw_sale.report'
    _description = 'Sales Data Warehouse Statistics'

    _auto = False
    _rec_name = 'data_confirmacao'
    _order = 'data_confirmacao desc'
    _STATUS = [('draft', 'Cotação'),
               ('sent', 'Cotação enviada'),
               ('sale', 'Pedido de venda'),
               ('done', 'Concluída'),
               ('cancel', 'Cancelada')]

    name = fields.Char('Referência do Pedido', readonly=True)
    unidade_medida_id = fields.Many2one('product.uom', 'Unidade de Medida', readonly=True)
    total_registros = fields.Integer('Total de registros', readonly=True)
    data_compra = fields.Date('Data de compra', readonly=True)
    data_confirmacao = fields.Date('Data de compra', readonly=True)
    qtd_pedida = fields.Float('Quantidade pedida', readonly=True)
    qtd_entregue = fields.Float('Quantidade entregue', readonly=True)
    qtd_a_faturar = fields.Float('Quantidade a faturar', readonly=True)
    montante_faturado = fields.Float('Montante faturado', readonly=True)
    montante_a_faturar = fields.Float('Montante a faturar', readonly=True)
    total_n_tributado = fields.Float('Total não tributado', readonly=True)
    total_registros = fields.Integer('Nº de Linhas', readonly=True)
    state = fields.Selection(_STATUS, string='Status', readonly=True)
    cliente_id = fields.Many2one('res.partner', 'Cliente', readonly=True)
    produto_id = fields.Many2one('product.template', 'Produto', readonly=True)
    vendedor_id = fields.Many2one('res.users', 'Vendedor', readonly=True)
    categoria_id = fields.Many2one('product.category', 'Categoria do Produto', readonly=True)
    time_venda_id = fields.Many2one('crm.team', 'Sales Channel', readonly=True, oldname='section_id')
    empresa_id = fields.Many2one('res.company', 'Empresa', readonly=True)
    peso = fields.Float('Peso total', readonly=True)
    volume = fields.Float('Volume', readonly=True)

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            'CREATE or REPLACE VIEW %s as ('
            '  SELECT min(dfato.id)                             id,'    
            '         dprod."name"                                "name",'
            '         dprod.product_uom_id                      unidade_medida_id,'
            '         dsale.data_compra                         data_compra,' 
            '         dsale.data_confirmacao                    data_confirmacao,'
            '         SUM(dfato.product_uom_qty)                qtd_pedida,'
            '         SUM(dfato.qty_delivered)                  qtd_entregue,'
            '         SUM(dfato.qty_to_invoice)                 qtd_a_faturar,'
            '         SUM(dfato.amt_invoiced)                   montante_faturado,'
            '         SUM(dfato.amt_to_invoice)                 montante_a_faturar,'
            '         SUM(dfato.price_subtotal)                 total_n_tributado,'
            '         count(*)                                  total_registros,'
            '         dfato.state                               state,'
            '         dcli.nk_client                            cliente_id,'
            '         dprod.nk_product                          produto_id,'
            '         dteam.salesman_id                         vendedor_id,'
            '         dprod.categ_id                            categoria_id,'
            '         dteam.nk_sale_team                        time_venda_id,'
            '         dteam.company_id                          empresa_id,'
            '         SUM(dprod.weight * dfato.product_uom_qty) peso,'
            '         SUM(dprod.volume * dfato.product_uom_qty) volume'
            '    FROM dw_sale_fact_sale_order     dfato'
            '         JOIN dw_sale_dim_time       dsale ON (dfato.sk_time      = dsale.id)'
            '           LEFT JOIN sale_order_line sale  ON (dsale.nk_sale      = sale.id)'
            '         JOIN dw_sale_dim_product    dprod ON (dfato.sk_product   = dprod.id)'
            '         JOIN dw_sale_dim_client     dcli  ON (dfato.sk_client    = dcli.id)'
            '         JOIN dw_sale_dim_sale_team  dteam ON (dfato.sk_sale_team = dteam.id)'
            '  GROUP BY dprod.nk_product,'
            '           sale.order_id,'
            '           dprod.product_uom_id,'
            '           dprod."name",'
            '           dprod.categ_id,'
            '           dsale.sale,'
            '           dsale.data_compra,'
            '           dsale.data_confirmacao,'
            '           dcli.nk_client,'
            '           dteam.salesman_id,'
            '           dfato.state,'
            '           dteam.company_id,'
            '           dteam.nk_sale_team'
            ');' % self._table
        )
