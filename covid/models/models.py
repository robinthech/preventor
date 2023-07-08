# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import logging
_logger = logging.getLogger(__name__)


class CovidAnexo4(models.Model):
    _name= "covid.4"

    name = fields.Char("Nombre")
    fecha = fields.Date('Fecha de Evaluación')
	empresa = fields.Char('Empresa Evaluada')
    ruc = fields.Char('RUC')
    sequence = fields.Char("Codigo",compute="_compute_sequence",store=True)

    @api.depends("create_uid")
	def _compute_sequence(self):
		for i, record in enumerate(self.sorted('id', reverse=False), 1):
			record.sequence = i
			if i < 10:
				record.sequence = "A4-000{}".format(i)
			elif i>= 10 and i < 100:
				record.sequence = "A4-00{}".format(i)
			elif i>= 100 and i < 1000:
				record.sequence = "A4-0{}".format(i)
			elif i>= 1000 and i < 10000:
				record.sequence = "A4-{}".format(i)


class CovidAnexo4Lista(models.Model):
    _name= "covid.4.lista"

    name = fields.Char("Elemento")
    cumplimiento = fields.Boolean("Cumple (Si/No)")
    detalles = fields.Text("Detalles / Pendientes / Por Mejorar")
