# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from logging import getLogger

log = getLogger(__name__)


class DimTime(models.Model):
    _name = 'dw_sale.dim_time'
    _description = 'Time dimension'
    _rec_name = 'sale'

    nk_sale = fields.Many2one('sale.order.line', 'Ordem de compra (Obj)')
    sale = fields.Char('Ordem de compra')
    data_criacao = fields.Date('Data de criação')
    data_atualizacao = fields.Date('Data de atualização')
    data_compra = fields.Date('Data de compra')
    data_confirmacao = fields.Date('Confirmação da compra')

    @api.model
    def create(self, vals):
        self._preencher_vals(vals)
        return super(DimTime, self).create(vals)

    @api.multi
    def write(self, vals):
        self._preencher_vals(vals)
        return super(DimTime, self).write(vals)

    def _preencher_vals(self, vals):
        if vals.get('nk_sale', False):
            nk_sale = self.env['sale.order.line'].browse(vals['nk_sale'])
            vals['sale'] = '%s - %s' % (nk_sale.order_id.name, nk_sale.name.split('\n')[0] or nk_sale.product_id.name)
            if nk_sale.order_id.date_order:
                vals['data_compra'] = fields.Datetime.from_string(nk_sale.order_id.date_order).strftime(DEFAULT_SERVER_DATE_FORMAT)
            if nk_sale.order_id.confirmation_date:
                vals['data_confirmacao'] = fields.Datetime.from_string(nk_sale.order_id.confirmation_date).strftime(DEFAULT_SERVER_DATE_FORMAT)
            vals['data_criacao'] = fields.Datetime.from_string(nk_sale.create_date).strftime(DEFAULT_SERVER_DATE_FORMAT)
            vals['data_atualizacao'] = fields.Datetime.from_string(nk_sale.write_date).strftime(DEFAULT_SERVER_DATE_FORMAT)

    @api.returns('self')
    def criar_por_sale(self, sale_order_line):
        """
        Cria um novo registro do modelo atual a partir de um 'sale.order.line'.

        :param sale_order_line: ID ou objeto do modelo 'sale.order.line'
        :return: Novo registro do modelo atual.
        """
        if isinstance(sale_order_line, int):
            return self.create({'nk_sale': sale_order_line})
        return self.create({'nk_sale': sale_order_line.id})

    @api.onchange('nk_sale')
    def nk_sale_change(self):
        if self.nk_sale:
            self.sale = '%s - %s' % (
            self.nk_sale.order_id.name, self.nk_sale.name.split('\n')[0] or self.nk_sale.product_id.name)
            self.data_criacao = fields.Datetime.from_string(self.nk_sale.create_date).strftime(
                DEFAULT_SERVER_DATE_FORMAT)
            self.data_atualizacao = fields.Datetime.from_string(self.nk_sale.write_date).strftime(
                DEFAULT_SERVER_DATE_FORMAT)


class DimProduct(models.Model):
    _name = 'dw_sale.dim_product'
    _description = 'Product dimension'
    _TIPOS_PRODUTOS = [('consu', 'Consumível'), ('service', 'Serviço')]

    nk_product = fields.Many2one('product.template', 'Produto')
    name = fields.Char('Nome do produto')
    #type = fields.Selection(_TIPOS_PRODUTOS, 'Tipo de produto')
    list_price = fields.Float('Valor de venda')
    product_uom_id = fields.Many2one('product.uom', 'Unidade de Medida') #________obs
    product_uom = fields.Char('Unidade de Medida')
    categ_id = fields.Many2one('product.category', 'Categoria do Produto')
    categ = fields.Char('Categoria do Produto')
    volume = fields.Float('Volume')
    weight = fields.Float('Peso')
    sale_ok = fields.Boolean('Pode ser vendido')
    purchease_ok = fields.Boolean('Pode ser comprado')
    active = fields.Boolean('Ativo', help='Oculta registro sem excluí-lo')

    @api.model
    def create(self, vals):
        self._preencher_vals(vals)
        return super(DimProduct, self).create(vals)

    @api.multi
    def write(self, vals):
        self._preencher_vals(vals)
        return super(DimProduct, self).write(vals)

    def _preencher_vals(self, vals):
        if vals.get('nk_product', False):
            nk_product = self.env['product.template'].browse(vals['nk_product'])
            vals['name'] = nk_product.name
            #vals['type'] = nk_product.type
            vals['list_price'] = nk_product.list_price
            vals['product_uom_id'] = nk_product.uom_id.id
            vals['product_uom'] = nk_product.uom_id.name
            vals['categ_id'] = nk_product.categ_id.id
            vals['categ'] = nk_product.categ_id.name
            vals['volume'] = nk_product.volume
            vals['weight'] = nk_product.weight
            vals['active'] = nk_product.active

    @api.returns('self')
    def criar_por_sale(self, sale_order_line):
        """
        Cria um novo registro do modelo atual a partir de um 'sale.order.line'.

        :param sale_order_line: ID ou objeto do modelo 'sale.order.line'
        :return: Novo registro do modelo atual.
        """
        if isinstance(sale_order_line, int):
            sale_order_line = self.env['sale.order.line'].browse(sale_order_line)
        return self.create({'nk_product': sale_order_line.product_id.id})


class DimClient(models.Model):
    _name = 'dw_sale.dim_client'
    _description = 'Criar uma breve descrição'

    nk_client = fields.Many2one('res.partner', 'Cliente')
    name = fields.Char('Nome do cliente')
    street = fields.Char('Rua')
    city = fields.Char('Cidade')
    state_id = fields.Many2one("res.country.state", string='Estado')
    country_id = fields.Many2one('res.country', string='País')
    state = fields.Char('Nome do Estado')
    country = fields.Char('Nome do País')

    @api.model
    def create(self, vals):
        self._preencher_vals(vals)
        return super(DimClient, self).create(vals)

    @api.multi
    def write(self, vals):
        self._preencher_vals(vals)
        return super(DimClient, self).write(vals)

    def _preencher_vals(self, vals):
        if vals.get('nk_client', False):
            nk_client = self.env['res.partner'].browse(vals['nk_client'])
            vals['name'] = nk_client.name
            vals['street'] = nk_client.street
            vals['city'] = nk_client.city
            vals['state_id'] = nk_client.state_id.id
            vals['state'] = nk_client.state_id.name
            vals['country_id'] = nk_client.country_id.id
            vals['country'] = nk_client.country_id.name

    @api.returns('self')
    def criar_por_sale(self, sale_order_line):
        """
        Cria um novo registro do modelo atual a partir de um 'sale.order.line'.

        :param sale_order_line: ID ou objeto do modelo 'sale.order.line'
        :return: Novo registro do modelo atual.
        """
        if isinstance(sale_order_line, int):
            sale_order_line = self.env['sale.order.line'].browse(sale_order_line)
        return self.create({'nk_client': sale_order_line.order_id.partner_id.id})

    @api.onchange('nk_client')
    def nk_client_change(self):
        if self.nk_client:
            self.name = self.nk_client.name
            self.street = self.nk_client.street
            self.city = self.nk_client.city
            self.state_id = self.nk_client.state_id
            self.state = self.nk_client.state_id.name
            self.country_id = self.nk_client.country_id
            self.country = self.nk_client.country_id.name


class DimSaleTeam(models.Model):
    _name = 'dw_sale.dim_sale_team'
    _description = 'Team dimension'

    nk_sale_team = fields.Many2one('crm.team', 'Canal de vendas')
    salesman_id = fields.Many2one('res.users', 'Vendedor')
    company_id = fields.Many2one('res.company', 'Empresa')

    sale_team = fields.Char('Canal de vendas')
    salesman = fields.Char('Vendedor')
    company = fields.Char('Empresa')
    active = fields.Boolean('Ativo')

    @api.returns('self')
    def criar_por_sale(self, sale_order_line):
        """
        Cria um novo registro do modelo atual a partir de um 'sale.order.line'.

        :param sale_order_line: ID ou objeto do modelo 'sale.order.line'
        :return: Novo registro do modelo atual.
        """
        if isinstance(sale_order_line, int):
            sale_order_line = self.env['sale.order.line'].browse(sale_order_line)
        return self.create({
            'nk_sale_team': sale_order_line.order_id.team_id.id,
            'salesman_id': sale_order_line.salesman_id.id,
            'company_id': sale_order_line.company_id.id,

            'sale_team': sale_order_line.order_id.team_id.name,
            'salesman': sale_order_line.salesman_id.name,
            'company': sale_order_line.company_id.name,
            'active': sale_order_line.order_id.team_id.active
        })


class FactSaleOrder(models.Model):
    _name = 'dw_sale.fact_sale_order'
    _description = 'Fact table sale orders'
    _STATUS_FATURA = [('upselling', 'Oportunidade de venda'),
                      ('invoiced', 'Totalmente faturado'),
                      ('to invoice', 'Faturar'),
                      ('no', 'Nada a faturar')]
    _STATUS = [('draft', 'Cotação'),
               ('sent', 'Cotação enviada'),
               ('sale', 'Pedido de venda'),
               ('done', 'Concluída'),
               ('cancel', 'Cancelada')]

    sk_time = fields.Many2one('dw_sale.dim_time', 'DimTime', required=True, ondelete='restrict')
    sk_product = fields.Many2one('dw_sale.dim_product', 'DimProduct', required=True, ondelete='restrict')
    sk_client = fields.Many2one('dw_sale.dim_client', 'DimClient', required=True, ondelete='restrict')
    sk_sale_team = fields.Many2one('dw_sale.dim_sale_team', 'DimSaleTeam', required=True, ondelete='restrict')

    invoice_status = fields.Selection(_STATUS_FATURA, 'Estatus de fatura', required=True)
    price_unit = fields.Float('Preço unitario', required=True)
    price_tax = fields.Float('Taxas', required=True)
    price_total = fields.Float('Preço total', required=True)
    price_subtotal = fields.Float('Preço subtotal', required=True)
    price_reduce = fields.Float('Preço unitario reduzido', required=True)
    price_reduce_taxinc = fields.Float('Preço unitario reduzido taxado', required=True)
    price_reduce_taxexcl = fields.Float('Preço unitario reduzido não taxado', required=True)
    product_uom_qty = fields.Float('Qtd Encomendada', readonly=True) #________________________obs
    discount = fields.Float('Porcentagem do disconto', required=True)
    qty_delivered = fields.Float('Quantidade entregue', required=True)
    qty_to_invoice = fields.Float('Quantidade para faturar', required=True)
    state = fields.Selection(_STATUS, 'Status do pedido', required=True)
    amt_to_invoice = fields.Integer('Montante à faturar', required=True)
    amt_invoiced = fields.Integer('Montante Faturado', required=True)

    @api.returns('self')
    def criar_por_sale(self, sale_order_line):
        """
        Cria um novo registro do modelo atual a partir de um 'sale.order.line'.

        :param sale_order_line: ID ou objeto do modelo 'sale.order.line'
        :return: Novo registro do modelo atual.
        """
        if isinstance(sale_order_line, int):
            sale_order_line = self.env['sale.order.line'].browse(sale_order_line)
        return self.create({
            'sk_time': self.env['dw_sale.dim_time'].criar_por_sale(sale_order_line).id,
            'sk_product': self.env['dw_sale.dim_product'].criar_por_sale(sale_order_line).id,
            'sk_client': self.env['dw_sale.dim_client'].criar_por_sale(sale_order_line).id,
            'sk_sale_team': self.env['dw_sale.dim_sale_team'].criar_por_sale(sale_order_line).id,

            'invoice_status': sale_order_line.invoice_status,
            'price_unit': sale_order_line.price_unit,
            'price_tax': sale_order_line.price_tax,
            'price_total': sale_order_line.price_total,
            'price_subtotal': sale_order_line.price_subtotal,
            'price_reduce': sale_order_line.price_reduce,
            'price_reduce_taxinc': sale_order_line.price_reduce_taxinc,
            'price_reduce_taxexcl': sale_order_line.price_reduce_taxexcl,
            'discount': sale_order_line.discount,
            'product_uom_qty': sale_order_line.product_uom_qty,
            'qty_delivered': sale_order_line.qty_delivered,
            'qty_to_invoice': sale_order_line.qty_to_invoice,
            'state': sale_order_line.state,
            'amt_to_invoice': sale_order_line.amt_to_invoice,
            'amt_invoiced': sale_order_line.amt_invoiced
        })

    @api.model
    def schedule_fact_load(self):
        log.info('Atualizando Fatos...')
        for sale in self.env['sale.order.line'].search([]):
            self.criar_por_sale(sale)
        log.info('Atualização concluída com %d novos fatos.' % self.env['sale.order.line'].search_count([]))
        return True

