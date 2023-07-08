# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
	_inherit = "res.users"

	registro_ids = fields.One2many('registro.monitoreo', 'create_uid', string=u'Iluminación')

class RegistroMonitoreo(models.Model):
	_name = 'registro.monitoreo'

	name = fields.Char("Codigo", index=True, default=lambda self: _('New'))
	ruc = fields.Char(string="RUC")
	cliente = fields.Char(string="Razon Social")
	sede = fields.Char(string=u'Sede')
	fecha_monitoreo = fields.Date("Fecha Inicio de Monitoreo")
	fecha_monitoreo_fin = fields.Date("Fecha Fin de Monitoreo")
	puntos = fields.Integer("Puntos Máximos por Agente")
	sequence = fields.Char(compute='_compute_sequence', string="Codigo")

	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('registro.monitoreo') or _('New')
		res = super(RegistroMonitoreo, self).create(vals)
		return res

	@api.depends("create_uid")
	def _compute_sequence(self):
		for i, record in enumerate(self.sorted('id', reverse=False), 1):
			record.sequence = i
			if i < 10:
				record.sequence = "RM-000{}".format(i)
			elif i>= 10 and i < 100:
				record.sequence = "RM-00{}".format(i)
			elif i>= 100 and i < 1000:
				record.sequence = "RM-0{}".format(i)
			elif i>= 1000 and i < 10000:
				record.sequence = "RM-{}".format(i)



class AgenteGeneral(models.Model):
	_name = 'agente.general'

	registro_id = fields.Many2one('registro.monitoreo', string=u'Registro')
	area = fields.Char(string=u'Área')
	puesto_trabajo = fields.Char(string=u'Puesto de Trabajo')
	empleado = fields.Char(string=u'Empleado')
	ubicacion = fields.Char(string=u'Ubicación del Punto')
	actividades = fields.Char(string='Actividades')
	fuentes_peligro = fields.Char(string=u'Fuentes de Peligro')
	controles = fields.Char(string=u'Controles Existentes')
	active = fields.Boolean(string=u'Activo', default=True)
	capacitacion = fields.Boolean("Capacitaciones", default=False)
	imagen = fields.Binary(string=u'Imagen')


class RiesgoDisergonomico(models.Model):
	_name = 'riesgo.disergonomico'
	_inherits = {'agente.general': 'agente_general_id'}

	agente_general_id = fields.Many2one('agente.general', required=True, ondelete='restrict', auto_join=True,
										string='Agente General')
	postura_1 = fields.Boolean(string='Las manos por encima de la cabeza')
	postura_2 = fields.Boolean(string='Las codos por encima del hombro')
	postura_3 = fields.Boolean(string='Espalda inclinada hacia adelante más de 30 grados')
	postura_4 = fields.Boolean(string='Espalda en extensión más de 30 grados')
	postura_5 = fields.Boolean(string='Cuello doblado / girado más de 30 grados')
	postura_6 = fields.Boolean(string='Estando sentado, espalda inclinada hacia adelante más de 30 grados')
	postura_7 = fields.Boolean(string='Estando sentado, espalda girada o lateralizada más de 30 grados')
	postura_8 = fields.Boolean(string='De cuclillas')
	postura_9 = fields.Boolean(string='De rodillas')
	postura_10 = fields.Boolean(string='Más de 2 horas en total por día')
	levantamiento_1 = fields.Boolean(string='40 KG. Una vez/ día')
	levantamiento_2 = fields.Boolean(string='25 KG. Más de doce veces / hora')
	levantamiento_3 = fields.Boolean(string='5 KG. Más de doce veces / minuto')
	levantamiento_4 = fields.Boolean(string='Menos de 3 Kg. Más de cuatro veces / min')
	levantamiento_5 = fields.Boolean(string='Durante más de 2 horas por día')
	esfuerzo_1 = fields.Boolean(string='Si se manipula y sujeta en pinza un objeto de más de 1kg')
	esfuerzo_2 = fields.Boolean(
		string='Si las muñecas están flexionadas en extensión, giradas o lateralizadas haciendo un agarre con fuerza')
	esfuerzo_3 = fields.Boolean(string='Si se ejecuta la acción de atornillar de forma intensa')
	esfuerzo_4 = fields.Boolean(string='Durante más de 2 horas por día')
	movimiento_1 = fields.Boolean(
		string='El trabajador repite el mismo movimiento muscular más de 4 veces/min. durante más de 2 horas por día')
	impacto_1 = fields.Boolean(
		string='Usando manos o rodillas como un martillo más de 10 veces por hora, más de 2 horas por día')
	vibracion_1 = fields.Boolean(string='Nivel moderado: más de 30 min/día')
	vibracion_2 = fields.Boolean(string='Nivel alto: 2horas/día')

class MonitoreosTransien(models.TransientModel):
	_name = 'monitoreo.transient'


	def limites_permisos(self,plan_id):
		permiso_line = self.env["registro.monitoreo"].search([('create_uid', '=',  self.env.user.id)])
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		if len(permiso_line) < plan.limite_registro:
			return True
		else:
			return False

	def limites_puntos_iluminacion(self,plan_id,registro_id):
		permiso_line = self.env["registro.monitoreo"].search([('create_uid', '=',  self.env.user.id),('id', '=',  registro_id)])
		_logger.info(permiso_line)
		_logger.info(permiso_line.iluminacion_ids)
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		if len(permiso_line.iluminacion_ids) < plan.limite_puntos:
			return True
		else:
			return False

	def limites_puntos_dosimetria(self,plan_id,registro_id):
		permiso_line = self.env["registro.monitoreo"].search([('create_uid', '=',  self.env.user.id),('id', '=',  registro_id)])
		_logger.info(permiso_line)
		_logger.info(permiso_line.dosimetria_ids)
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		if len(permiso_line.dosimetria_ids) < plan.limite_puntos:
			return True
		else:
			return False
