from odoo import models, fields, api
from odoo.exceptions import UserError

class SurfaceAnalysisWizard(models.TransientModel):
    _name = 'surface.analysis.wizard'

    date_start = fields.Date(string="Start Date", required=True)
    date_end = fields.Date(string="End Date", required=True)

    def action_get_analysis(self):
        query = """
            SELECT pt.name, SUM(sol.product_uom_qty * pp.width * pp.height) AS total_surface, 
                   SUM(sol.product_uom_qty * pp.product_weight) AS total_weight, 
                   SUM(sol.price_subtotal) AS total_price
            FROM sale_order_line sol
            JOIN product_product pp ON sol.product_id = pp.id
            JOIN product_template pt ON pp.product_tmpl_id = pt.id
            JOIN sale_order so ON sol.order_id = so.id
            WHERE so.state = 'sale' 
            AND so.date_order >= %s AND so.date_order <= %s
            GROUP BY pt.name
        """
        self.env.cr.execute(query, (self.date_start, self.date_end))
        results = self.env.cr.fetchall()

        if not results:
            raise UserError("No results found for the selected date range.")

        formatted_results = []
        for row in results:
            formatted_results.append({
                'product': row[0],
                'total_surface': row[1],
                'total_weight': row[2],
                'total_price': row[3],
            })

        # Pass the results to the report context
        return self.env.ref('vente.surface_analysis_pdf_report').report_action(self, data={
            'results': formatted_results,'date_start': self.date_start, 'date_end': self.date_end})