from odoo import models, fields, api

class ImporrtExportProduct(models.Model):
    # models.Model is the base class for all Odoo models that need to be stored in the database.
    _name = 'imporrt.export.product' # Database table name
    _discription = 'Export product' # Description of the model

    name = fields.char(string='Name', required=True)
    product_type = fields.selection([('import','Import'),('export','Export')], string='Product Type', required=True)
    quantity = fields.integer(string='Quantity', required=True)
    description = fields.text(string='Description')