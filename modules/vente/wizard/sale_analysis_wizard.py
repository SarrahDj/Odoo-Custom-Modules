from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleAnalysisWizard(models.TransientModel):
    _name = 'sale.analysis.wizard'
    _description = 'Wizard d\'Analyse des Ventes'

    start_date = fields.Date(string="Date de Début")
    end_date = fields.Date(string="Date de Fin")
    filter_by_customer = fields.Boolean(string="Filtrer par Client")
    customer_id = fields.Many2one('res.partner', string="Client")

    def action_analyze(self):
        # Collect data based on the wizard input
        domain = [('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date)]
        if self.filter_by_customer:
            domain.append(('partner_id', '=', self.customer_id.id))

        orders = self.env['sale.order'].search(domain)
        if not orders:
            raise UserError('No orders found for the given criteria.')

        # Prepare data for the report
        order_data = []
        for order in orders:
            order_data.append({
                'date_order': order.date_order.strftime('%Y-%m-%d') if order.date_order else '',  # Format date as a string
                'amount_total': order.amount_total,
                'partner_id': order.partner_id.name
            })

        # Generate and return the PDF report
        return self.env.ref('vente.report_sale_order_analysis').report_action([], data={
            'start_date': self.start_date.strftime('%Y-%m-%d') if self.start_date else '',
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else '',
            'filter_by_customer': self.filter_by_customer,
            'customer_name': self.customer_id.name ,
            'orders': order_data  # Pass formatted data
        })
