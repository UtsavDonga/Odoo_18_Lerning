from odoo import models, fields, api
from odoo.exceptions import UserError

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Book a Slot for Appointment"
    _inherit = 'mail.thread'
    _rec_name = 'patient_id'

    reference = fields.Char(string='Reference', default='new')
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True)
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

    def send_appointment_email(self):
        print("\n\n\n\n\n\n\n\n\n utsav")
        template = self.env.ref('Wings_hospital.mail_template_appointment_created', raise_if_not_found=False)
        if template:  # Ensure it's a record, not an int  
            print("\n\n\n\n\n\n\n\n\n template",template)
            template.send_mail(self.id, force_send=True)
        else:
            raise ValueError("Email template 'mail_template_appointment_created' not found!")


  # @api.model
    # def create(self, vals):
    #     record = super(HospitalAppointment, self).create(vals)
    #     if not record.doctor_id.email:
    #         raise UserError("Doctor does not have an email address configured.")
    #     record.send_doctor_email()
    #     return record

    # def write(self, vals):
    #     if 'state' in vals:
    #         for rec in self:
    #             old_state = rec.state
    #             new_state = vals['state']
    #             if old_state != new_state:
    #                 rec.send_patient_email(old_state, new_state)
    #     return super(HospitalAppointment, self).write(vals)

    # def send_doctor_email(self):
    #     """Send an email to the doctor when a new appointment is created."""
    #     if not self.doctor_id.email:
    #         return

    #     mail_obj = self.env['mail.mail']
    #     email_values = {
    #         'subject': f'New Appointment: {self.patient_id.name}',
    #         'email_to': self.doctor_id.email,
    #         'body_html': f""" 
    #             <p>Dear Dr. {self.doctor_id.name},</p>
    #             <p>You have a new appointment scheduled:</p>
    #             <ul>
    #                 <li><strong>Patient:</strong> {self.patient_id.name}</li>
    #                 <li><strong>Date:</strong> {self.appointment_date}</li>
    #             </ul>
    #             <p>Thank You.</p>""",
    #     }

    #     mail = mail_obj.create(email_values)
    #     mail.send()
    #     return mail

    # def send_patient_email(self, old_state, new_state):
    #     """Send an email to the patient when the appointment status is updated."""
    #     if not self.patient_id.email:
    #         return

    #     mail_obj = self.env['mail.mail']
    #     email_values = {
    #         'subject': f'Appointment Status Update:{self.patient_id.name}',
    #         'email_to': self.patient_id.email,
    #         'body_html': f""" 
    #             <p>Dear {self.patient_id.name},</p>
    #             <p>Your appointment status has been updated.</p>
    #             <ul>
    #                 <li><strong>Doctor:</strong> {self.doctor_id.name}</li>
    #                 <li><strong>Date:</strong> {self.appointment_date}</li>
    #                 <li><strong>Old Status:</strong> {old_state.capitalize()}</li>
    #                 <li><strong>New Status:</strong> {new_state.capitalize()}</li>
    #             </ul>
    #             <p>Thank You.</p>""",
    #     }
    # mail = mail_obj.create(email_values)
    # mail.send()
    # return mail
