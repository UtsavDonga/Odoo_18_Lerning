from import odoo models, fields, api

class ImporrtExportPartner(models.Model):
    _name = 'imporrt.export.partner'
    _description = 'Supplier Customer'
    
    name = fields.char(string='Name', required=True)
    partner_type = fields.selection([('supplier','Supplier'),('customer','Customer')],string='Type', required=True)
    email = fields.char(string='Email')
    phone = fields.char(string='phone Number')
    address = fields.text(string='Address')
