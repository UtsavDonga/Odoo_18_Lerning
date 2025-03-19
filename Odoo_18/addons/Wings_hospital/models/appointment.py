from odoo import models, fields, api

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Book a Slot for Appointment"
    _inherit = 'mail.thread'
    _rec_name = 'patient_id'

    reference = fields.Char(string='Reference', default='new')
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, ondelete="restrict")
    appointment_date = fields.Date(string='Appointment Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    date_of_birth = fields.Date(string="DOB", related='patient_id.date_of_birth', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'new':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)

    def copy(self, default=None):
        default = dict(default or {})
        default['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or '/'
        return super(HospitalAppointment, self).copy(default)
