from odoo import models, fields, api
import requests
import json

class Webhook(models.Model):
    _name = 'wings_hospital.webhook'
    _description = 'Webhook Configuration'

    name = fields.Char(string="Webhook Name", required=True)
    url = fields.Char(string="Target URL", required=True)
    event = fields.Selection([
        ('create', 'On Create'),
        ('write', 'On Update'),
        ('unlink', 'On Delete')
    ], string="Trigger Event", required=True)