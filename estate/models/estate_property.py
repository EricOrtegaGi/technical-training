from odoo import fields, models
from odoo import api
from odoo.exceptions import UserError
class EstateProperty(models.Model):
    _name = 'estate.property'
    name = fields.Char('Propietat Immobiliària', required=True )
    _description = fields.Text('Descripció')
    postcode = fields.Char('Codi Postal')
    date_availability = fields.Date('Data Disponibilitat', copy=False)
    selling_price = fields.Float('Preu de Venda')
    bedrooms = fields.Integer('Habitacions')
    active = fields.Boolean(default=True)
    state = fields.Selection([('New','En Tractament'),('OfferAccepted', 'Oferta Acceptada'),('Sold', 'Venuda'),('Canceled', 'Cancel·lada')],default='New',copy=False,required = True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Ofertes')
    avgPrice = fields.Float('Preu per m2', compute='_calcularPreuPerMetre',stored=True)
    area = fields.Float('Àrea')
    expected_selling_price = fields.Float('Preu de venda esperat')
    buyer_id = fields.Many2one('res.partner', string='Comprador')
    salesperson_id = fields.Many2one('res.users', string='Comercial', default=lambda self: self.env.user.id)
    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
    Type_id = fields.Many2one('estate.property.type', string='Tipo')
    certificat_energetic = fields.Selection([('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F'),('G','G')], string='Certificat Energetic')
    any_construccio = fields.Integer('Any de construcció')
    banys = fields.Integer('Banys') 
    parking = fields.Boolean('Parking')
    @api.depends('expected_selling_price','area')
    
    def _calcularPreuPerMetre(self):
        for record in self:
            if record.area > 0 :
                record.avgPrice = record.expected_selling_price/record.area
            else:
                record.avgPrice = None
                    
    def cancellarPropietat(self):
        if self.state == 'Sold':
            raise UserError('No es pot cancel·lar una propietat venuda')
        else:
            self.state = 'Canceled'
        return True
    
    def _update_buyer(self):
        self.ensure_one()
        highest_offer = self.env['estate.property.offer'].search([('property_id','=',self.id)], order='price desc', limit=1)
        if highest_offer:
            self.buyer_id = highest_offer.partner_id.id
            
            
        
    
     

            