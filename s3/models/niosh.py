# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _
import math


class RegistroMonitoreo(models.Model):
	_inherit = "registro.monitoreo"

	niosh_ids = fields.One2many('niosh.niosh', 'registro_id', string=u'NIOSH')
	puntos_niosh = fields.Integer(compute="_compute_puntos_niosh", string=u"NIOSH")

	@api.depends("reba_ids")
	def _compute_puntos_niosh(self):
		for record in self:
			record.puntos_niosh = len(record.niosh_ids)

class Niosh(models.Model):
    _name = 'niosh.niosh'
    _inherits = {'riesgo.disergonomico': 'riesgo_disergonomico_id'}

    name = fields.Char(string="Código", index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('niosh.niosh') or _('New')
        res = super(Niosh, self).create(vals)
        return res

    riesgo_disergonomico_id = fields.Many2one('riesgo.disergonomico', required=True, ondelete='restrict', auto_join=True, tring='Riesgo Disergonomico')
    masa = fields.Float(string='Masa de Objeto a Levantar (m ≤ mref) Especifica')
    distancia = fields.Float("Distancia Horizontal (h)")
    posicion_inicial = fields.Float(string='Posición Vertical Inicial (v)')
    posicion_final = fields.Float(string='Posición Vertical Final (v)')
    frecuencia = fields.Float(string='Frecuencia de Levantamiento (F) / minuto')
    calidad = fields.Selection(selection=[("Bueno", "Bueno"), ("Regular", "Regular"), ("Malo", "Malo")],default="Regular",
                               string='Calidad de Agarre (c)')
    angulo = fields.Float(string='Angulo de Asimetría')
    duracion = fields.Float(string='Duración del Trabajo (Horas)')
    lc = fields.Float(string='LC',default=25)

    # campos calculados
    hm = fields.Float(compute="_compute_niosh", string="HM", store=True)
    vm = fields.Float(compute="_compute_niosh", string="VM", store=True)
    dm = fields.Float(compute="_compute_niosh", string="DM", store=True)
    am = fields.Float(compute="_compute_niosh", string="AM", store=True)
    fm = fields.Float(compute="_compute_niosh", string="FM", store=True)
    cm = fields.Float(compute="_compute_niosh", string="CM", store=True)
    rwl = fields.Float(compute="_compute_niosh", string="RWL", store=True)
    il = fields.Float(compute="_compute_niosh", string="IL", store=True)
    nivel_riesgo = fields.Char(compute="_compute_niosh", string="Nivel de Riesgo", store=True)
    desplazamineto = fields.Float(compute="_compute_niosh", string="Desplazamiento vertical (D)", store=True)
    cumple = fields.Char(compute="_compute_niosh", string="¿Cumple?", store=True)

    @api.depends("distancia", "posicion_inicial", "posicion_final", "angulo", "frecuencia", "duracion", "lc",
                 "nivel_riesgo")
    def _compute_niosh(self):
        for record in self:
            if record.distancia <= 25:
                record.hm = 1
            elif record.distancia > 63:
                record.hm = 0
            elif record.distancia != 0:
                record.hm = 25/record.distancia

            record.vm = (1 - 0.003 * math.fabs(record.posicion_inicial - 75))
            record.desplazamineto = math.fabs(record.posicion_inicial - record.posicion_final)
            if record.desplazamineto < 25:
                record.dm = 1
            elif record.desplazamineto > 175:
                record.dm = 0
            elif record.desplazamineto != 0:
                record.dm = 0.82 + (4.5/record.desplazamineto)

            if record.angulo > 135:
                record.am = 0
            else:
                record.am = 1 - (0.0032 * record.angulo)

            if record.frecuencia <= 0.2:
                numero = 0.2

            elif record.frecuencia <= 0.5:
                numero = 0.5

            elif record.frecuencia <= 15:
                numero = math.ceil(record.frecuencia)

            else:
                numero = 0

            if record.duracion <= 1:
                indice_1 = 0
            elif record.duracion <= 2:
                indice_1 = 1
            else:
                indice_1 = 2

            if record.posicion_inicial < 75:
                indice_2 = 0
            else:
                indice_2 = 1

            indice = 2 * indice_1 + indice_2 + 2

            if numero == 0:
                record.fm = 0

            elif numero == 15:
                if indice == 3:
                    record.fm = 0.28
                else:
                    record.fm = 0

            elif numero == 14:
                if indice == 3:
                    record.fm = 0.31
                else:
                    record.fm = 0

            elif numero == 13:
                if indice == 3:
                    record.fm = 0.34
                else:
                    record.fm = 0

            elif numero == 12:
                if indice == 2 or indice == 3:
                    record.fm = 0.37
                elif indice == 5:
                    record.fm = 0.21
                else:
                    record.fm = 0

            elif numero == 11:
                if indice == 2 or indice == 3:
                    record.fm = 0.41
                elif indice == 5:
                    record.fm = 0.23
                else:
                    record.fm = 0

            elif numero == 10:
                if indice == 2 or indice == 3:
                    record.fm = 0.45
                elif indice == 4 or indice == 5:
                    record.fm = 0.26
                elif indice == 7:
                    record.fm = 0.13
                else:
                    record.fm = 0

            elif numero == 9:
                if indice == 2 or indice == 3:
                    record.fm = 0.52
                elif indice == 4 or indice == 5:
                    record.fm = 0.3
                elif indice == 7:
                    record.fm = 0.15
                else:
                    record.fm = 0

            elif numero == 8:
                if indice == 2 or indice == 3:
                    record.fm = 0.6
                elif indice == 4 or indice == 5:
                    record.fm = 0.35
                else:
                    record.fm = 0.18

            elif numero == 7:
                if indice == 2 or indice == 3:
                    record.fm = 0.7
                elif indice == 4 or indice == 5:
                    record.fm = 0.42
                else:
                    record.fm = 0.22

            elif numero == 6:
                if indice == 2 or indice == 3:
                    record.fm = 0.75
                elif indice == 4 or indice == 5:
                    record.fm = 0.5
                else:
                    record.fm = 0.27

            elif numero == 5:
                if indice == 2 or indice == 3:
                    record.fm = 0.8
                elif indice == 4 or indice == 5:
                    record.fm = 0.6
                else:
                    record.fm = 0.35

            elif numero == 4:
                if indice == 2 or indice == 3:
                    record.fm = 0.84
                elif indice == 4 or indice == 5:
                    record.fm = 0.72
                else:
                    record.fm = 0.45

            elif numero == 3:
                if indice == 2 or indice == 3:
                    record.fm = 0.88
                elif indice == 4 or indice == 5:
                    record.fm = 0.79
                else:
                    record.fm = 0.55

            elif numero == 2:
                if indice == 2 or indice == 3:
                    record.fm = 0.91
                elif indice == 4 or indice == 5:
                    record.fm = 0.84
                else:
                    record.fm = 0.65

            elif numero == 1:
                if indice == 2 or indice == 3:
                    record.fm = 0.94
                elif indice == 4 or indice == 5:
                    record.fm = 0.88
                else:
                    record.fm = 0.75

            elif numero == 0.5:
                if indice == 2 or indice == 3:
                    record.fm = 0.97
                elif indice == 4 or indice == 5:
                    record.fm = 0.92
                else:
                    record.fm = 0.81

            elif numero == 0.2:
                if indice == 2 or indice == 3:
                    record.fm = 0.1
                elif indice == 4 or indice == 5:
                    record.fm = 0.95
                else:
                    record.fm = 0.85

            if record.hm < 75:
                if record.calidad == "Bueno":
                    record.cm = 1
                elif record.calidad == "Regular":
                    record.cm = 0.95
                elif record.calidad == "Malo":
                    record.cm = 0.9

            elif record.hm >= 75:
                if record.calidad == "Bueno":
                    record.cm = 1
                elif record.calidad == "Regular":
                    record.cm = 1
                elif record.calidad == "Malo":
                    record.cm = 0.9

            record.rwl = record.lc * record.hm * record.vm * record.dm * record.am * record.fm * record.cm
            if record.rwl != 0:
                record.il = record.masa / record.rwl

            if record.il <= 1:
                record.nivel_riesgo = "BAJO"
                record.cumple = "SÍ CUMPLE"
            elif record.il < 3 and record.il > 1:
                record.nivel_riesgo = "MEDIO"
                record.cumple = "SÍ CUMPLE"
            elif record.il >= 3:
                record.nivel_riesgo = "ALTO"
                record.cumple = "NO CUMPLE"
