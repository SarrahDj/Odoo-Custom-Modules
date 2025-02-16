from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    avenant_line_ids = fields.One2many('avenant.line', 'sale_order_id', string='Avenant Lines')
    def action_create_avenant(self):
        """Create a new Avenant record from the Sale Order."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Avenant',
            'res_model': 'avenant.model',
            'view_mode': 'form',
            'view_type': 'form',
            'context': {
                'default_order_id': self.id,
                'default_client_id': self.partner_id.id,
            },
            'target': 'current',
              }
    combined_order_line_ids = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='order_id',
        string="Combined Order Lines",
        compute='_compute_combined_order_lines',
    )

    @api.depends('order_line', 'avenant_line_ids')
    def _compute_combined_order_lines(self):
        for order in self:
            # Combine order lines from sale.order.line and avenant.line
            avenant_lines = self.env['avenant.line'].search([('sale_order_id', '=', order.id)])
            order.combined_order_line_ids = order.order_line + avenant_lines
