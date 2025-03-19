from odoo import api, fields, models
from datetime import date

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([('male','Male'),('female','Female')], string='Gender')
    tag_ids = fields.Many2many('hospital.patient.tag', string='Tags')
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.date_of_birth:
                birth_date = rec.date_of_birth
                rec.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                rec.age = 0

    def unlink(self):
        for rec in self:
            appointments = self.env['hospital.appointment'].search([('patient_id', '=', rec.id)])
            if appointments:
                raise models.ValidationError('Cannot delete patient with existing appointments')
        return super().unlink()