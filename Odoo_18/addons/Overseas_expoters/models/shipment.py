from odoo import models, fields, api

class ImporrtExportShipment(models.Model):
    _name = 'imporrt.export.shipment'
    _description = 'Shipment Tracking'


    name = fields.char(string='Shipment Reference', required=True)
    partner_id = fields.Many2one('imporrt.export.partner',string='Customer/Supplier',required=True)
    product_id = fields.Many2one('imporrt.export.product',string='Product',required=True)
    shipment_type = fields.selection([('import','Import'),('export','Export')],string='Shipment Type',required=True)
    shipment_status = fields.selection([('draft','Darft'),('onboard','Onboard'),('arrived','Arrived')],string='Shipment Status',required=True)
    shipment_date = fields.date = fields.date(string='Shipment Date')   