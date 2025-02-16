from odoo import models, fields, api

class RistourneModel(models.Model):
    _inherit = 'product.template'

    discount = fields.Float(string="ristourne")

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    acc_discount = fields.Float(string='Ristourne')
    montant_ristourne = fields.Float(string='Montant Ristourne', compute='_compute_montant_ristourne', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.acc_discount = self.product_id.discount

    @api.depends('product_id', 'acc_discount')
    def _compute_montant_ristourne(self):
        for line in self:
            if line.product_id and line.product_id.list_price:
                line.montant_ristourne = (line.product_id.list_price * line.acc_discount) / 100
                line.montant_ristourne = line.montant_ristourne * line.quantity
            else:
                line.montant_ristourne = 0.0


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_ristourne = fields.Float(string='Total Ristourne', compute='_compute_total_ristourne', store=True)

    @api.depends('invoice_line_ids.montant_ristourne')
    def _compute_total_ristourne(self):
        for move in self:
            move.total_ristourne = sum(line.montant_ristourne for line in move.invoice_line_ids)


class ProductTemplate(models.Model):
    _inherit = 'product.template'


    list_price = fields.Float(string='Realisation Price')
    standard_price = fields.Float(string='Real Cost')
    invoice_policy= fields.Selection(selection=[
        ('order', 'ordered quantities'),
        ('delivery', 'Done quantities')
    ])
    previsionnel_cost = fields.Float(string='Previsionnel cost')

class ProductProd(models.Model):
    _inherit = 'product.product'

    discount = fields.Float(string="ristourne")


    list_price = fields.Float(string='Realisation Price')
    standard_price = fields.Float(string='Real Cost')
    invoice_policy= fields.Selection(selection=[
        ('order', 'ordered quantities'),
        ('delivery', 'Done quantities')
    ])
    previsionnel_cost = fields.Float(string='Rrevisionnel cost')


