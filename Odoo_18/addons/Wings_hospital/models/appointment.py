from odoo import api, fields, models

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Book a Slot for Appointment"
    _inherit = 'mail.thread'
    _rec_names_search = ['reference','patient_id']
    _rec_name = 'patient_id'

    reference = fields.Char(string='reference', default='new')
    patient_id = fields.Many2one('hospital.patient', string='patient',required=False,ondelete="restrict")
    appointment_date = fields.Date(string='Date')

    date_of_birth = fields.Date(string = "DOB", related='patient_id.date_of_birth', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'new':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)

    def _compute_display_name(self):
        for rec in self:
            print('values is',f"{rec.reference} - {rec.patient_id.name}")
            rec.display_name = f"{rec.reference} - {rec.patient_id.name}"
            
    def copy(self, default=None):
        default = dict(default or {})  #""" Generate a new unique reference for duplicated records """
        default['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or '/' # Featch next number from the sequence 
        return super(HospitalAppointment, self).copy(default)#Calls the original Odoo copy function but replaces the old reference with the new one
         #ensures that the copied record is created with a unique reference.

      

