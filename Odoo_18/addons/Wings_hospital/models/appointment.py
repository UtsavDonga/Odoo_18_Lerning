from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
    _name = "hospital.appointment" #Defines the model's technical name.
    _description = "Book a Slot for Appointment" #Provides a description of the model.
    _inherit = 'mail.thread' #Adds tracking functionality (for logging status changes).
    _rec_name = 'patient_id' #Defines the field shown as the record name in views.

    reference = fields.Char(string='Reference', default='new') #A unique appointment reference (generated later in the create method).
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True) # Links each appointment to one doctor.
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True, ondelete="restrict") #Links each appointment to one patient.
    appointment_date = fields.Date(string='Appointment Date')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')

    date_of_birth = fields.Date(string="DOB", related='patient_id.date_of_birth', store=True)

    #Drop Down menu for Slot
    time_slot = fields.Selection([
        ('10-11','10:00 AM - 11:00 AM'),
        ('11-12','11:00 AM - 12:00 PM'),
        ('12-1','12:00 PM - 1:00 PM'),
        ('2-3','2:00 PM - 3:00 PM'),
        ('3-4','3:00 PM - 4:00 PM'),
        ('4-5','4:00 PM - 5:00 PM'),
        ('5-6','5:00 PM - 6:00 PM'),
        ('6-7','6:00 PM - 7:00 PM')
    ], string="Time Slot", required=True)

    #Computed Field for Available Slots
    available_time_slots = fields.Char(
        string="Available Slots", compute="_compute_available_slots"
    )
    #Stores available slots, Computed dynamically using _compute_available_slots.

    #Ensures that a doctor cannot have multiple appointments in the same time slot on the same date. this chake that Duplicate data is not enterd at database level
    _sql_constraints = [
        ('unique_appointment', 'unique(doctor_id, appointment_date, time_slot)',
         "This time slot is already booked for the selected doctor, please choose another slot.")
    ]

    #Generates a unique reference number for each appointment.
    #Uses ir.sequence for sequential numbering.
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('reference') or vals['reference'] == 'new':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(vals_list)

    #Ensures copied appointments get a new reference.
    def copy(self, default=None):
        default = dict(default or {})
        default['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or '/'
        return super(HospitalAppointment, self).copy(default)

    #Send mail using Email Template
    def send_appointment_email(self):
        template = self.env.ref('Wings_hospital.mail_template_appointment_created', raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)
        else:
            raise ValueError("Email template 'mail_template_appointment_created' not found!")


    #Dynamically calculates available slots by checking existing bookings.
    #Uses mapped('time_slot') to extract booked slots.
    @api.depends('doctor_id', 'appointment_date')
    def _compute_available_slots(self):
        all_slots = ['10-11', '11-12', '12-1', '2-3', '3-4', '4-5', '5-6', '6-7']
        for record in self:
            if record.doctor_id and record.appointment_date:
                booked_slots = self.env['hospital.appointment'].search([
                    ('doctor_id', '=', record.doctor_id.id),
                    ('appointment_date', '=', record.appointment_date),
                    ('state', '!=', 'cancelled'),
                    ('id', '!=', record.id)
                ]).mapped('time_slot')

                available_slots = [slot for slot in all_slots if slot not in booked_slots]
                record.available_time_slots = ', '.join(available_slots) if available_slots else "No slots available"
            else:
                record.available_time_slots = ', '.join(all_slots)


    #Ensures that an appointment cannot be created if the time slot is already taken.
    @api.constrains('doctor_id', 'appointment_date', 'time_slot')
    def _check_time_slot_availability(self):
        for record in self:
            existing_appointment = self.env['hospital.appointment'].search([
                ('doctor_id', '=', record.doctor_id.id),
                ('appointment_date', '=', record.appointment_date),
                ('time_slot', '=', record.time_slot),
                ('id', '!=', record.id),
            ])
            if existing_appointment.exists():
                raise ValidationError(f"The time slot {record.time_slot} is already booked for this doctor on {record.appointment_date}. Please select a different slot.")

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
