from odoo import fields, models
from odoo.exceptions import Warning

class Salle(models.Model):
    _name = 'agence.salle'
    _description = 'Salle'

    def check_typesalle(self):
        for salle in self:
            if not salle.nbplaces:
                raise Warning(' Ajouter le nombre de places pour  %s' % salle.name)
            if salle.nbplaces < 100:
                raise Warning(' C est une salle de formation ou de réunion ')
            else:
                raise Warning(' C est une salle de Conférence !  ')
        return True


    name = fields.Char('Désignation', required=True)
    isactif = fields.Boolean('Active ?')
    nbplaces = fields.Integer('Nbr de place' )
    prix_location = fields.Float('Prix Location / Heure :')
    description= fields.Text('Description')

class Bureau(models.Model):
    _name = 'agence.bureau'
    _description = 'Bureau'
    name = fields.Char('Désignation', required=True)
    isactif = fields.Boolean('Actif?')
    surface = fields.Integer('Surface en M2 ' )
    prix_location = fields.Float('Prix Location / Mois ')
    description= fields.Text('Description')