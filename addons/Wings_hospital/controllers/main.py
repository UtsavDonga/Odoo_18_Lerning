from odoo import http
from odoo.http import request
import json

class WebhookController(http.Controller):

    @http.route('/webhook/receive', type='json', auth='public', methods=['POST'], csrf=False)
    def receive_webhook(self, **post):
        try:
            data = json.loads(request.httprequest.data)
            request.env['wings_hospital.patient'].sudo().create({
                'name': data.get('name'),
                'age': data.get('age')
            })
            return {'status': 'success', 'message': 'Webhook received'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
