from odoo import http,fields
from odoo.http import request
from werkzeug.exceptions import Forbidden, NotFound
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import Website
import datetime
import base64
from datetime import datetime,  timedelta, date
import logging
import pytz
import xlsxwriter
_logger = logging.getLogger(__name__)

class AuditoriaInterna(http.Controller):

    # @http.route('/auditoria_interna', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
    # def index(self):
    #     today = date.today()
    #     fecha_actual = today.strftime("%Y-%m-%d")
    #     verificaciones = request.env["lista.verificacion"].sudo().search([('create_uid',  '=', request.env.user.id)])
    #     return request.render('auditoria_interna.auditoria_interna', {"fecha_actual":fecha_actual,"verificaciones":verificaciones})


    # @http.route('/auditoria_interna/<model("lista.verificacion"):verificacion>', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
    # def auditoria_interna(self,verificacion):
    #     today = date.today()
    #     fecha_actual = today.strftime("%Y-%m-%d")
    #     return request.render('auditoria_interna.formulario', {"fecha_actual":fecha_actual,"verificacion":verificacion})
    @http.route('/auditoria_interna', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
    def lista_auditoria(self):
        today = date.today()
        fecha_actual = today.strftime("%Y-%m-%d")
        auditoria_interna = request.env["auditoria.interna"].sudo().search([('create_uid',  '=', request.env.user.id)])
        return request.render('auditoria_interna.lista_auditoria', {"fecha_actual":fecha_actual,"auditoria_interna":auditoria_interna})


    @http.route('/auditoria_interna/<model("auditoria.interna"):auditoria_interna>', type='http', methods=['GET', 'POST'], auth="user", website=True, csrf=False)
    def form_auditoria(self,auditoria_interna):
        fechas = []
        for registro in auditoria_interna.registro_ids:
            fecha_dia = registro.fecha.strftime("%Y-%m-%d")
            fecha_hora = registro.fecha.strftime("%H:%M:%S")
            fecha_inicio = fecha_dia+'T'+fecha_hora
            fechas.append(fecha_inicio)

        today = datetime.now(pytz.timezone('America/Lima'))
        today_dia = today.strftime("%Y-%m-%d")
        today_hora = today.strftime("%H:%M:%S")
        today_inicio = today_dia+'T'+today_hora

        attachments = request.env['ir.attachment'].sudo().search(
            [('res_model', '=', 'auditoria.interna'),
             ('res_id', '=', auditoria_interna.id)], order='id')


        return request.render('auditoria_interna.formulario_auditoria', {"fecha_actual":today_inicio,"auditoria_interna":auditoria_interna,'attachments': attachments,'fechas': fechas})

    @http.route(['/guardar_documento'], type='http', methods=['POST'], auth="public", website=True, csrf=False)
    def guardardocumento(self, **kw):

        _logger.info("entroaguardardocumento")
        auditoria = request.env['auditoria.interna'].sudo().search([('id',  '=', 1)])
        _logger.info(auditoria)
        _logger.info(kw['attachment'])
        _logger.info(type(kw['attachment']))
        _logger.info(base64.b64encode(kw['attachment'].encode('ascii')))
        auditoria.sudo().write({
            'attachment': (base64.b64encode(kw['attachment'].encode('ascii'))).decode('ascii')
        })

    @http.route('/auditoria_interna/success', type='http', methods=['GET', 'POST'], auth="public", website=True, csrf=False)
    def auditoria_success(self):
        return request.render('auditoria_interna.success')
