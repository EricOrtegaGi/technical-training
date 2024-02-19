from odoo import fields, models
from odoo import api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Model per estate.property.offer"
    price = fields.Float('Preu')
    status = fields.Selection([('Accepted', 'Acceptada'), ('Refused','Rebutjada'), ('Process','En Proces')],copy=False, default='Process',required=True)
    partner_id = fields.Many2one('res.partner',string='Comprador',required=True, copy = False)
    property_id = fields.Many2one('estate.property',string='Propietat',required=True)

    @api.model 
    def create(self, values):
        record = super(EstatePropertyOffer, self).create(values)
        record.property_id._update_buyer()
        return record

    def write(self, vals):
        res = super(EstatePropertyOffer, self).write(vals)
        for record in self:
            record.property_id._update_buyer()
        return res
