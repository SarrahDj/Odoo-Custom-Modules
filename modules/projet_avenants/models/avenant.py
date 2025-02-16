from odoo import models, fields, api

class Avenant(models.Model):
    _name = 'avenant.model'
    _description = 'Avenant'

    avenant_id = fields.Char(string="Avenant", required=True, copy=False, readonly=True, index=True,
                             default=lambda self: ('New'))

    order_id = fields.Many2one('sale.order', string="Sale Order", required=True)
    client_id = fields.Many2one(related='order_id.partner_id', string='Client', readonly=True)
    address = fields.Char(related='order_id.partner_id.contact_address', string="Adresse", readonly=True)
    date = fields.Datetime(string="Date", default=fields.Datetime.now, readonly=True)
    avenant_line_ids = fields.One2many('avenant.line', 'avenant_id', string="Avenant Lines")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], string="State", default='draft')

    total_price = fields.Monetary(string="Total", compute="_compute_total_price", currency_field='currency_id', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)

    @api.depends('avenant_line_ids.subtotal')
    def _compute_total_price(self):
        for avenant in self:
            total = sum(line.subtotal for line in avenant.avenant_line_ids)
            avenant.total_price = total

    @api.model
    def create(self, vals):
        if vals.get('avenant_id', ('New')) == ('New'):
            vals['avenant_id'] = self.env['ir.sequence'].next_by_code('avenant.model') or ('New')
        return super(Avenant, self).create(vals)

class AvenantLine(models.Model):
    _name = 'avenant.line'
    _description = 'Avenant Line'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', ondelete='cascade')
    avenant_id = fields.Many2one('avenant.model', string="Avenant Reference")
    product_id = fields.Many2one('product.product', string="Article")
    description = fields.Char(related="product_id.lst_price",string="Description")
    quantity = fields.Float(related="product_id.lst_price",string="Quantité")
    price_unit = fields.Float(related="product_id.lst_price" ,string="Prix Unitaire")
    tax_id = fields.Many2many('account.tax', string="Taxes")

    # Add the currency_id field
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id)

    subtotal = fields.Monetary(string="Sous-total", compute="_compute_subtotal", currency_field='currency_id')

    @api.depends('quantity', 'price_unit', 'tax_id')
    def _compute_subtotal(self):
        for line in self:
            taxes = line.tax_id.compute_all(line.price_unit, quantity=line.quantity, currency=line.currency_id)
            line.subtotal = taxes['total_included']

