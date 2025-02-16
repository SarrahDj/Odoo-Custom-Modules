from odoo import  fields,models
from  odoo.exceptions import  Warning

class Salle (models.Model):
    _inherit = 'agence.salle'

    def check_typesalle(self):
        for salle in self:
            if not salle.nbplaces:
                raise Warning(' Ajouter le nombre de places pour  %s' % salle.name)
            if salle.nbplaces <= 20:
                raise Warning(' C est une salle de réunion !  ')
            elif  salle.nbplaces >10 and  salle.nbplaces < 100 :
                raise Warning(' C est une salle de formation ! ')
            else:
                raise Warning(' C est une salle de Conférence !  ')
        return True

    # On ajoute le champ surface
    surface=fields.Integer(' Surface ' )
    # On modifie le champ description, en le rendant html
    description = fields.Html('desciption détaillé')