from odoo import api, fields, models
from datetime import date

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    date_of_birth = fields.Date(string = "Date of Birth")
    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender')
    tag_ids = fields.Many2many('hospital.patient.tag','patient_tag_rel','patient_id',string='Tags')

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

    # def create(self, vals):
    #     record = super(Patient, self).create(vals)
    #     self._send_webhook('create', record)
    #     return record

    # def write(self, vals):
    #     result = super(Patient, self).write(vals)
    #     self._send_webhook('write', self)
    #     return result

    def unlink(self):
        for rec in self:
            domain = [('patient_id','=',rec.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
                raise models.ValidationError('Cannot delete patient, patient having appointments')
        return super().unlink()

    # def _send_webhook(self, event, record):
    #     webhooks = self.env['wings_hospital.webhook'].search([('event', '=', event)])
    #     for webhook in webhooks:
    #         data = {
    #             'id': record.id,
    #             'name': record.name,
    #             'age': record.age
    #         }
    #         headers = {'Content-Type': 'application/json'}
    #         try:
    #             requests.post(webhook.url, data=json.dumps(data), headers=headers)
    #         except Exception as e:
    #             _logger.error(f"Failed to send webhook: {str(e)}")    


# this is also usble for showign an error same as above
    #  def _chek_patient_appoint (self):
    #     for rec in self:
    #         domain = [('patient_id','=',rec.id)]
    #         appointments = self.env['hospital.appointment'].search(domain)
    #         if appointments:
    #             raise ValidationError('Cannot delete patient, patient having appointments')