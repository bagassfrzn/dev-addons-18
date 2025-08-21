from odoo import http
from odoo.http import request
import json
from odoo.http import Response
from odoo.tools.config import config
import logging



class ITClubAPI(http.Controller):

    HEADER_NAME = 'ITCLUB-API-KEY'
    CONF_PARAM_KEY = 'itclub_api_key'

    def _check_api_key(self):
        provided_key = request.httprequest.headers.get(self.HEADER_NAME)
        actual_key = config.get(self.CONF_PARAM_KEY)
        return provided_key == actual_key

   
    # @http.route('/api/test-connection', type='http', auth='public', methods=['GET'], csrf=False)
    # def test_connection(self, **kwargs):
    #     return "Bagas mau reign"

    @http.route('/api/create-member', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def create_member(self, **kwargs):
        values = kwargs.get('values') or kwargs.get('params', {}).get('values')

        if not self._check_api_key():
            return Response(
                json.dumps({'status': 'error', 'message': 'Unauthorized'}),
                status=401,
                content_type='application/json'
            )

        if not values:
            return {'status': 'error', 'message': 'Field \"values\" tidak ditemukan'}

        if not values.get('name'):
            return {'status': 'error', 'message': 'Field \"name\" tidak boleh kosong'}

        try:
            partner = request.env['res.partner'].sudo().create({
                'name': values.get('name'),
                'mobile': values.get('mobile'),
                'email': values.get('email'),
                'street': values.get('street'),
                'grade': values.get('grade'),
                'major': values.get('major'),
                'extracurricular_ids': [(6, 0, values.get('extracurricular_ids', []))],
                'company_type': 'person',
                'extracurricular_contact_type': 'student',
                'extracurricular_contact_position': 'member',
            })

            return {
                'status': 'success',
                'partner_id': partner.id
            }

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

            
    # @http.route('/api/create-coach', type='json', auth='public', methods=['POST'], csrf=False)
    # def create_coach(self, **kwargs):
    #     self.values = kwargs

    #     if not self.values._check_api_key():
    #         return Response(
    #             json.dumps({'status': 'error', 'message': 'Unauthorized'}),
    #             status=401,
    #             content_type='application/json'
    #         )
        
    #     try:
    #         partner = request.env['res.partner'].sudo().create({
    #             'name': data.get('name'),
    #             'mobile': data.get('mobile'),
    #             'email': data.get('email'),
    #             'street': data.get('street'),
    #             'grade': data.get('grade'),
    #             'major': data.get('major'),
    #             'extracurricular_ids': [(6, 0, data.get('extracurricular_ids', []))],
    #             'company_type': 'person',
    #             'extracurricular_contact_type': 'coach',
    #         })

    #         return {'status': 'success', 'id': partner.id}
    #     except Exception as e:
    #         return Response(
    #             json.dumps({'status': 'error', 'message': str(e)}),
    #             status=500,
    #             content_type='application/json'
    #         )
