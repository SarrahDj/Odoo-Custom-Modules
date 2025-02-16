from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_address = fields.Char(string="Adresse du Client", compute='_compute_customer_address')
    total_weight = fields.Float(string="Total Poids", compute='_compute_total_weight')

    @api.depends('partner_id')
    def _compute_customer_address(self):
        for order in self:
            order.customer_address = order.partner_id.contact_address

    @api.depends('order_line.weight', 'order_line.product_uom_qty')
    def _compute_total_weight(self):
        for order in self:
            total_weight = sum(line.weight * line.product_uom_qty for line in order.order_line)
            order.total_weight = total_weight

    def action_confirm(self):
        # Call the original confirmation method
        res = super(SaleOrder, self).action_confirm()

        # Loop through orders to generate pickings and redirect
        for order in self:
            if order.state == 'sale':
                # Create the delivery order (stock picking)
                picking = order._create_delivery_picking()

                # Confirm and assign the picking (if automatic assignments are enabled)
                picking.action_confirm()
                picking.action_assign()

                # Redirect the user to the created delivery order (picking)
                return {
                    'type': 'ir.actions.act_window',
                    'name': 'Delivery Order',
                    'res_model': 'stock.picking',
                    'view_mode': 'form',
                    'res_id': picking.id,
                    'target': 'current',
                }

        return res


    def _create_delivery_picking(self):
        Picking = self.env['stock.picking']
        Stockmove = self.env['stock.move']

        picking_type = self.env.ref('stock.picking_type_out')
        picking_vals = {
            'origin': self.name,
            'partner_id': self.partner_id.id,
            'picking_type_id': picking_type.id,
            'location_id': picking_type.default_location_src_id.id,
            'location_dest_id': self.partner_id.property_stock_customer.id,
            'sale_id': self.id,
        }
        picking = Picking.create(picking_vals)

        for line in self.order_line:
            if line.product_id.type != 'service':
                move= Stockmove.create({
                    'name': line.name,
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom': line.product_uom.id,
                    'picking_id': picking.id,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking.location_dest_id.id,
                    'sale_line_id': line.id,
                })

                # Populate picking with product dimensions (assuming these fields exist in the product model)
                move.stock_weight = line.product_id.weight
                move.thick = line.product_id.thickness
                move.high = line.product_id.height
                move.wide = line.product_id.width

        return picking

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    weight = fields.Float(string="Poids", readonly=True)
    thick = fields.Float(string="Epaisseur" , readonly=True)
    high = fields.Float(string="Longueur" , readonly=True)
    wide = fields.Float(string="Largeur" , readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
           self.weight = self.product_id.product_weight
           self.thick = self.product_id.thickness
           self.high = self.product_id.height
           self.wide = self.product_id.width

class ProductDimensions(models.Model):
    _inherit = 'product.product'

    product_weight = fields.Float(string="Poids", default=0.0)
    thickness = fields.Float(string="Epaisseur", default=0.0)
    height = fields.Float(string="Longueur", default=0.0)
    width = fields.Float(string="Largeur", default=0.0)


class StockMove(models.Model):
    _inherit = 'stock.move'

    stock_weight = fields.Float(related='product_id.product_weight', string="Poids", readonly=True)
    thickness = fields.Float(related='product_id.thickness', string="Epaisseur", readonly=True)
    height = fields.Float(related='product_id.height', string="Longueur", readonly=True)
    width = fields.Float(related='product_id.width', string="Largeur", readonly=True)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_weight = fields.Float(string='Total Weight', compute='_compute_total_weight', store=True)
    general_surface = fields.Float(string='General Surface', compute='_compute_general_surface', store=True)

    @api.depends('move_ids_without_package')
    def _compute_total_weight(self):
        for picking in self:
            total_weight = 0.0
            for move in picking.move_ids_without_package:
                total_weight += move.product_id.product_weight * move.product_uom_qty
            picking.total_weight = total_weight

    @api.depends('move_ids_without_package')
    def _compute_general_surface(self):
        for picking in self:
            total_surface = 0.0
            for move in picking.move_ids_without_package:
                product = move.product_id
                surface = product.width * product.height
                total_surface += surface * move.product_uom_qty
            picking.general_surface = total_surface