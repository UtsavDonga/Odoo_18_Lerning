from odoo import models, fields

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor Record'

    name = fields.Char(string='Name', required=True)
    specialization = fields.Char(string='Specialization')
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')


    
 