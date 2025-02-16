from odoo import fields, models


class Locataire(models.Model):
    _name = 'agence.locataire'
    _description = 'Locataire d agence'

    code_locataire = fields.Char()
    partner_id = fields.Many2one(
        'res.partner',
        delegate=True,
        ondelete='cascade',
        required=True)