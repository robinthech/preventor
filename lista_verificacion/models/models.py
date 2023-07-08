# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID, _
import math  # noqa
import base64  # noqa
import io  # noqa
from xlwt import easyxf, Workbook  # noqa
from xlwt import Formula  # noqa
from PIL import Image  # noqa
import xlsxwriter
from datetime import datetime, timedelta, date
from odoo.exceptions import ValidationError
import odoo.addons.decimal_precision as dp
import os
import pytz

class Sgsst(models.Model):
	_name = 'lista.verificacion'

	name = fields.Char("N° Lista", index=True,default=lambda self: _('Borrador'))
	evaluado = fields.Char('Evaluado por')
	fecha = fields.Date('Fecha de Evaluación')
	empresa = fields.Char('Empresa Evaluada')
	datos = fields.Char('Datos Adicionales')
	txt_excel_cal = fields.Char()
	txt_binary_excel_cal = fields.Binary(string=u'Lista Verificacion')
	count_si = fields.Integer("Contador si")
	count_no = fields.Integer("Contador no")
	count_total = fields.Integer("Contador Total")
	puntaje = fields.Char('Puntaje Obtenido',default='0.00%')
	otros_ids = fields.One2many("lista.otros", "otros_id", "Otros lineamientos")
	# contador = fields.Integer(compute="_compute_contador_otros", string="contador")
	# indicador_ids = fields.One2many("principio.indicador", 'verifica_id', string="Indicadores", copy=True)

	# @api.depends("otros_ids")
	# def _compute_contador_otros(self):
	#     for record in self:
	#         record.contador = len(record.otros_ids)





	principios_char_1 = fields.Char(default='D.S 005-2012-TR,art. 24.',string='principios 1')
	principios_bol_1 = fields.Char('principios 1')
	principios_text_1 = fields.Text('principios 1')
	principios_char_2 = fields.Char(default='D.S 005-2012-TR,art. 24.',string='principios 2')
	principios_bol_2 = fields.Char('principios 2')
	principios_text_2 = fields.Text('principios 2')
	principios_char_3 = fields.Char('principios 3',default='Ley 29783, art. 18.')
	principios_bol_3 = fields.Char('principios 3')
	principios_text_3 = fields.Text('principios 3')
	principios_char_4 = fields.Char('principios 4',default='Ley 29783, art. 18,inciso D.')
	principios_bol_4 = fields.Char('principios 4')
	principios_text_4 = fields.Text('principios 4')
	principios_char_5 = fields.Char('principios 5',default='Ley 29783, art. 18,inciso E.')
	principios_bol_5 = fields.Char('principios 5')
	principios_text_5 = fields.Text('principios 5')
	principios_char_6 = fields.Char('principios 6',default='Ley 29783, art.18, inciso F.')
	principios_bol_6 = fields.Char('principios 6')
	principios_text_6 = fields.Text('principios 6')
	principios_char_7 = fields.Char('principios 7',default='Ley 29783, art.18, inciso G.')
	principios_bol_7 = fields.Char('principios 7')
	principios_text_7 = fields.Text('principios 7')
	principios_char_8 = fields.Char('principios 8',default='Ley 29783, art.18, inciso H.')
	principios_bol_8 = fields.Char('principios 8')
	principios_text_8 = fields.Text('principios 8')
	principios_char_9 = fields.Char('principios 9',default='Ley 29783, art.18, inciso I.')
	principios_bol_9 = fields.Char('principios 9')
	principios_text_9 = fields.Text('principios 9')
	principios_char_10 = fields.Char('principios 10',default='Ley 29783, art.18, inciso J.')
	principios_bol_10 = fields.Char('principios 10')
	principios_text_10 = fields.Text('principios 10')

	politica_char_1 = fields.Char('politica 1',default='Ley 29783, art.22, inciso A.')
	politica_bol_1 = fields.Char('politica 1')
	politica_text_1 = fields.Text('politica 1')
	politica_char_2 = fields.Char('politica 2',default='Ley 29783, art.22, inciso B.')
	politica_bol_2 = fields.Char('politica 2')
	politica_text_2 = fields.Text('politica 2')
	politica_char_3 = fields.Char('politica 3',default='Ley 29783, art.22, inciso C.')
	politica_bol_3 = fields.Char('politica 3')
	politica_text_3 = fields.Text('politica 3')
	politica_char_4 = fields.Char('politica 4',default='Ley 29783, art.23, incisos A, B y C.')
	politica_bol_4 = fields.Char('politica 4')
	politica_text_4 = fields.Text('politica 4')

	direccion_char_1 = fields.Char('direccion 1',default='D.S 005-2012-TR, art.78 inciso B. Ley 29783, art. 18, inciso J.')
	direccion_bol_1 = fields.Char('direccion 1')
	direccion_text_1 = fields.Text('direccion 1')
	direccion_char_2 = fields.Char('direccion 2',default='Ley 29783, art.25.')
	direccion_bol_2 = fields.Char('direccion 2')
	direccion_text_2 = fields.Text('direccion 2')

	liderazgo_char_1 = fields.Char('liderazgo 1',default='Ley 29783, art.26.')
	liderazgo_bol_1 = fields.Char('liderazgo 1')
	liderazgo_text_1 = fields.Text('liderazgo 1')
	liderazgo_char_2 = fields.Char('liderazgo 2',default='D.S 005-2012-TR, art. 26, inciso J.')
	liderazgo_bol_2 = fields.Char('liderazgo 2')
	liderazgo_text_2 = fields.Text('liderazgo 2')

	organizacion_char_1 = fields.Char('organizacion 1',default='Ley 29783, art.27.')
	organizacion_bol_1 = fields.Char('organizacion 1')
	organizacion_text_1 = fields.Text('organizacion 1')
	organizacion_char_2 = fields.Char('organizacion 2',default='D.S 005-2012-TR, art. 25. Ley 29783, art.62.')
	organizacion_bol_2 = fields.Char('organizacion 2')
	organizacion_text_2 = fields.Text('organizacion 2')
	organizacion_char_3 = fields.Char('organizacion 3',default='D.S 005-2012-TR, art. 109.')
	organizacion_bol_3 = fields.Char('organizacion 3')
	organizacion_text_3 = fields.Text('organizacion 3')
	organizacion_char_4 = fields.Char('organizacion 4',default='Ley 29783, art.27.')
	organizacion_bol_4 = fields.Char('organizacion 4')
	organizacion_text_4 = fields.Text('organizacion 4')

	diagnostico_char_1 = fields.Char('diagnostico 1',default='Ley 29783, art. 37.')
	diagnostico_bol_1 = fields.Char('diagnostico 1')
	diagnostico_text_1 = fields.Text('diagnostico 1')
	diagnostico_char_2 = fields.Char('diagnostico 2',default='Ley 29783, art. 37.')
	diagnostico_bol_2 = fields.Char('diagnostico 2')
	diagnostico_text_2 = fields.Text('diagnostico 2')

	planteamiento_char_1 = fields.Char('planteamiento 1',default='D.S 005-2012-TR, art.38.')
	planteamiento_bol_1 = fields.Char('planteamiento 1')
	planteamiento_text_1 = fields.Text('planteamiento 1')
	planteamiento_char_2 = fields.Char('planteamiento 2',default='D.S 005-2012-TR, art.37, inciso B.')
	planteamiento_bol_2 = fields.Char('planteamiento 2')
	planteamiento_text_2 = fields.Text('planteamiento 2')
	planteamiento_char_3 = fields.Char('planteamiento 3',default='Ley 29783, art.50, incisos A,B,C,D,E y F.')
	planteamiento_bol_3 = fields.Char('planteamiento 3')
	planteamiento_text_3 = fields.Text('planteamiento 3')
	planteamiento_char_4 = fields.Char('planteamiento 4',default='Ley 29783, art. 57.')
	planteamiento_bol_4 = fields.Char('planteamiento 4')
	planteamiento_text_4 = fields.Text('planteamiento 4')
	planteamiento_char_5 = fields.Char('planteamiento 5',default='Ley 29783, art.57, incisos A y B.')
	planteamiento_bol_5 = fields.Char('planteamiento 5')
	planteamiento_text_5 = fields.Text('planteamiento 5')
	planteamiento_char_6 = fields.Char('planteamiento 6',default='Ley 29783, art. 75.')
	planteamiento_bol_6 = fields.Char('planteamiento 6')
	planteamiento_text_6 = fields.Text('planteamiento 6')

	objetivos_char_1 = fields.Char('objetivos 1',default='Ley 29783, art.39, inciso B.')
	objetivos_bol_1 = fields.Char('objetivos 1')
	objetivos_text_1 = fields.Text('objetivos 1')
	objetivos_char_2 = fields.Char('objetivos 2',default='D.S 005-2012-TR, art.80, inciso A.')
	objetivos_bol_2 = fields.Char('objetivos 2')
	objetivos_text_2 = fields.Text('objetivos 2')

	programa_char_1 = fields.Char('programa 1',default='D.S 005-2012-TR, art.32, inciso F.')
	programa_bol_1 = fields.Char('programa 1')
	programa_text_1 = fields.Text('programa 1')
	programa_char_2 = fields.Char('programa 2',default='Ley 29783, art.39.')
	programa_bol_2 = fields.Char('programa 2')
	programa_text_2 = fields.Text('programa 2')
	programa_char_3 = fields.Char('programa 3',default='Ley 29783, art.26.')
	programa_bol_3 = fields.Char('programa 3')
	programa_text_3 = fields.Text('programa 3')
	programa_char_4 = fields.Char('programa 4',default='Ley 29783, art.25.')
	programa_bol_4 = fields.Char('programa 4')
	programa_text_4 = fields.Text('programa 4')
	programa_char_5 = fields.Char('programa 5',default='Ley 29783, art.25. D.S 005-2012-TR, art. 80, inciso B.')
	programa_bol_5 = fields.Char('programa 5')
	programa_text_5 = fields.Text('programa 5')
	programa_char_6 = fields.Char('programa 6',default='Ley 29783, art.65.')
	programa_bol_6 = fields.Char('programa 6')
	programa_text_6 = fields.Text('programa 6')

	# despuesdeaquifalta
	estructura_char_1 = fields.Char('estructura 1',default='Ley 29783, art.29.')
	estructura_bol_1 = fields.Char('estructura 1')
	estructura_text_1 = fields.Text('estructura 1')
	estructura_char_2 = fields.Char('estructura 2',default='Ley 29783, art.49, incisos A,B,C y D.')
	estructura_bol_2 = fields.Char('estructura 2')
	estructura_text_2 = fields.Text('estructura 2')
	estructura_char_3 = fields.Char('estructura 3',default='Ley 29783, art.49, incisos A,B,C y D.')
	estructura_bol_3 = fields.Char('estructura 3')
	estructura_text_3 = fields.Text('estructura 3')
	estructura_char_4 = fields.Char('estructura 4',default='Ley 29783, art.27, art.51.')
	estructura_bol_4 = fields.Char('estructura 4')
	estructura_text_4 = fields.Text('estructura 4')
	estructura_char_5 = fields.Char('estructura 5',default='Ley 29783, art.55.')
	estructura_bol_5 = fields.Char('estructura 5')
	estructura_text_5 = fields.Text('estructura 5')
	estructura_char_6 = fields.Char('estructura 6',default='Ley 29783, art.56, inciso G. D.S 005.2012-TR, art.32.')
	estructura_bol_6 = fields.Char('estructura 6')
	estructura_text_6 = fields.Text('estructura 6')
	estructura_char_7 = fields.Char('estructura 7',default='Ley 29783, art.35, inciso D.')
	estructura_bol_7 = fields.Char('estructura 7')
	estructura_text_7 = fields.Text('estructura 7')

	capacitacion_char_1 = fields.Char('capacitacion 1',default='Ley 29783, art.25.')
	capacitacion_bol_1 = fields.Char('capacitacion 1')
	capacitacion_text_1 = fields.Text('capacitacion 1')
	capacitacion_char_2 = fields.Char('capacitacion 2',default='Ley 29783, art.27. D.S 005-2012-TR, art.28.')
	capacitacion_bol_2 = fields.Char('capacitacion 2')
	capacitacion_text_2 = fields.Text('capacitacion 2')
	capacitacion_char_3 = fields.Char('capacitacion 3',default='Ley 29783, art.62. D.S 005-2012-TR, art.28.')
	capacitacion_bol_3 = fields.Char('capacitacion 3')
	capacitacion_text_3 = fields.Text('capacitacion 3')
	capacitacion_char_4 = fields.Char('capacitacion 4',default='Ley 29783, art.74.')
	capacitacion_bol_4 = fields.Char('capacitacion 4')
	capacitacion_text_4 = fields.Text('capacitacion 4')
	capacitacion_char_5 = fields.Char('capacitacion 5',default='D.S 005.2012-TR, art.29, inciso B.')
	capacitacion_bol_5 = fields.Char('capacitacion 5')
	capacitacion_text_5 = fields.Text('capacitacion 5')
	capacitacion_char_6 = fields.Char('capacitacion 6',default='D.S 005.2012-TR, art.66.')
	capacitacion_bol_6 = fields.Char('capacitacion 6')
	capacitacion_text_6 = fields.Text('capacitacion 6')
	capacitacion_char_7 = fields.Char('capacitacion 7',default='D.S 005-2012-TR, art.29, inciso F.')
	capacitacion_bol_7 = fields.Char('capacitacion 7')
	capacitacion_text_7 = fields.Text('capacitacion 7')
	capacitacion_char_8 = fields.Char('capacitacion 8',default='Ley 29783, art.49 inciso G. D.S 005-2012-TR, art.27, inciso A.')
	capacitacion_bol_8 = fields.Char('capacitacion 8')
	capacitacion_text_8 = fields.Text('capacitacion 8')

	medidas_char_1 = fields.Char('medidas 1',default='Ley 29783, art.21, incisos A,B,C,D y E.')
	medidas_bol_1 = fields.Char('medidas 1')
	medidas_text_1 = fields.Text('medidas 1')

	preparacion_char_1 = fields.Char('preparacion 1',default='Ley 29783, art.34, inciso B.')
	preparacion_bol_1 = fields.Char('preparacion 1')
	preparacion_text_1 = fields.Text('preparacion 1')
	preparacion_char_2 = fields.Char('preparacion 2',default='D.S 005-2012-TR, art.83,inciso C.')
	preparacion_bol_2 = fields.Char('preparacion 2')
	preparacion_text_2 = fields.Text('preparacion 2')
	preparacion_char_3 = fields.Char('preparacion 3',default='Ley 29783, art.47. D.S 005-2012-TR, art.85.')
	preparacion_bol_3 = fields.Char('preparacion 3')
	preparacion_text_3 = fields.Text('preparacion 3')
	preparacion_char_4 = fields.Char('preparacion 4',default='Ley 29783, art.63.')
	preparacion_bol_4 = fields.Char('preparacion 4')
	preparacion_text_4 = fields.Text('preparacion 4')

	contratista_char_1 = fields.Char('contratista 1',default='Ley 29783, art.68, incisos A,B,C y D.')
	contratista_bol_1 = fields.Char('contratista 1')
	contratista_text_1 = fields.Text('contratista 1')
	contratista_char_2 = fields.Char('contratista 2',default='Ley 29783, art.77.')
	contratista_bol_2 = fields.Char('contratista 2')
	contratista_text_2 = fields.Text('contratista 2')

	consulta_char_1 = fields.Char('consulta 1',default='Ley 29783, art.19, incisos A,B y C. D.S 005-2012-TR, art.88.')
	consulta_bol_1 = fields.Char('consulta 1')
	consulta_text_1 = fields.Text('consulta 1')
	consulta_char_2 = fields.Char('consulta 2',default='D.S 005-2012-TR, art. Ley 29783, art.70.')
	consulta_bol_2 = fields.Char('consulta 2')
	consulta_text_2 = fields.Text('consulta 2')
	consulta_char_3 = fields.Char('consulta 3',default='Ley 29783, art.52.')
	consulta_bol_3 = fields.Char('consulta 3')
	consulta_text_3 = fields.Text('consulta 3')

	requisitos_char_1 = fields.Char('requisitos 1',default='D.S 005-2012-TR, art.84, inciso A.')
	requisitos_bol_1 = fields.Char('requisitos 1')
	requisitos_text_1 = fields.Text('requisitos 1')
	requisitos_char_2 = fields.Char('requisitos 2',default='D.S 005-2012-TR, art.7. Ley 29783, art.34.')
	requisitos_bol_2 = fields.Char('requisitos 2')
	requisitos_text_2 = fields.Text('requisitos 2')
	requisitos_char_3 = fields.Char('requisitos 3',default='D.S 005-2012-TR, art.49. art.42, inciso 5.')
	requisitos_bol_3 = fields.Char('requisitos 3')
	requisitos_text_3 = fields.Text('requisitos 3')
	requisitos_char_4 = fields.Char('requisitos 4',default='D.S 005-2012-TR, art.96.')
	requisitos_bol_4 = fields.Char('requisitos 4')
	requisitos_text_4 = fields.Text('requisitos 4')
	requisitos_char_5 = fields.Char('requisitos 5',default='Ley 29783, art.64.')
	requisitos_bol_5 = fields.Char('requisitos 5')
	requisitos_text_5 = fields.Text('requisitos 5')
	requisitos_char_6 = fields.Char('requisitos 6',default='Ley 29783, art.66. D.S 005-2012-TR, art.92.')
	requisitos_bol_6 = fields.Char('requisitos 6')
	requisitos_text_6 = fields.Text('requisitos 6')
	requisitos_char_7 = fields.Char('requisitos 7',default='Ley 29783, art.67.')
	requisitos_bol_7 = fields.Char('requisitos 7')
	requisitos_text_7 = fields.Text('requisitos 7')
	requisitos_char_8 = fields.Char('requisitos 8',default='Ley 29783, art.67.')
	requisitos_bol_8 = fields.Char('requisitos 8')
	requisitos_text_8 = fields.Text('requisitos 8')
	requisitos_char_9 = fields.Char('requisitos 9',default='Ley 29783, art.69, incisos A,B,C,D y E.')
	requisitos_bol_9 = fields.Char('requisitos 9')
	requisitos_text_9 = fields.Text('requisitos 9')
	requisitos_char_10 = fields.Char('requisitos 10',default='Ley 29783, art.79, incisos A,B,C,D,E,F,G y H.')
	requisitos_bol_10 = fields.Char('requisitos 10')
	requisitos_text_10 = fields.Text('requisitos 10')

	supervision_char_1 = fields.Char('supervision 1',default='Ley 29783, art.40.')
	supervision_bol_1 = fields.Char('supervision 1')
	supervision_text_1 = fields.Text('supervision 1')
	supervision_char_2 = fields.Char('supervision 2',default='Ley 29783, art.41, incisos A y B.')
	supervision_bol_2 = fields.Char('supervision 2')
	supervision_text_2 = fields.Text('supervision 2')
	supervision_char_3 = fields.Char('supervision 3',default='D.S 005.2012-TR, art.86.')
	supervision_bol_3 = fields.Char('supervision 3')
	supervision_text_3 = fields.Text('supervision 3')
	supervision_char_4 = fields.Char('supervision 4',default='D.S 005.2012-TR, art.86.')
	supervision_bol_4 = fields.Char('supervision 4')
	supervision_text_4 = fields.Text('supervision 4')

	salud_char_1 = fields.Char('salud 1',default='Ley 29783, art.67, 49, inciso C. D.S 005-2012-TR, art.101.')
	salud_bol_1 = fields.Char('salud 1')
	salud_text_1 = fields.Text('salud 1')
	salud_char_2 = fields.Char('salud 2',default='Ley 29783, art. 71, incisos A y B.')
	salud_bol_2 = fields.Char('salud 2')
	salud_text_2 = fields.Text('salud 2')
	salud_char_3 = fields.Char('salud 3',default='D.S 005.2012-TR, art.102.')
	salud_bol_3 = fields.Char('salud 3')
	salud_text_3 = fields.Text('salud 3')
	salud_char_4 = fields.Char('salud 4',default='Ley 29783, art.82, inciso A.')
	salud_bol_4 = fields.Char('salud 4')
	salud_text_4 = fields.Text('salud 4')
	salud_char_5 = fields.Char('salud 5',default='Ley 29783, art.82, inciso B. D.S 005-2012-TR, art.111.')
	salud_bol_5 = fields.Char('salud 5')
	salud_text_5 = fields.Text('salud 5')
	salud_char_6 = fields.Char('salud 6',default='D.S 005-2012-TR, art.34.')
	salud_bol_6 = fields.Char('salud 6')
	salud_text_6 = fields.Text('salud 6')
	salud_char_7 = fields.Char('salud 7',default='Ley 29783, art.45.')
	salud_bol_7 = fields.Char('salud 7')
	salud_text_7 = fields.Text('salud 7')
	salud_char_8 = fields.Char('salud 8',default='D.S 005-2012-TR, art.33.')
	salud_bol_8 = fields.Char('salud 8')
	salud_text_8 = fields.Text('salud 8')

	investigacion_char_1 = fields.Char('investigacion 1')
	investigacion_bol_1 = fields.Char('investigacion 1')
	investigacion_text_1 = fields.Text('investigacion 1')
	investigacion_char_2 = fields.Char('investigacion 2')
	investigacion_bol_2 = fields.Char('investigacion 2')
	investigacion_text_2 = fields.Text('investigacion 2')
	investigacion_char_3 = fields.Char('investigacion 3')
	investigacion_bol_3 = fields.Char('investigacion 3')
	investigacion_text_3 = fields.Text('investigacion 3')
	investigacion_char_4 = fields.Char('investigacion 4')
	investigacion_bol_4 = fields.Char('investigacion 4')
	investigacion_text_4 = fields.Text('investigacion 4')
	investigacion_char_5 = fields.Char('investigacion 5')
	investigacion_bol_5 = fields.Char('investigacion 5')
	investigacion_text_5 = fields.Text('investigacion 5')

	control_char_1 = fields.Char('control 1',default='Ley 29783, art.52. D.S 005-2012-TR, art.27, inciso D.')
	control_bol_1 = fields.Char('control 1')
	control_text_1 = fields.Text('control 1')
	control_char_2 = fields.Char('control 2',default='Ley 29783, art.36, inciso C.')
	control_bol_2 = fields.Char('control 2')
	control_text_2 = fields.Text('control 2')

	gestion_char_1 = fields.Char('gestion 1',default='Ley 29783, art.36, inciso C.')
	gestion_bol_1 = fields.Char('gestion 1')
	gestion_text_1 = fields.Text('gestion 1')
	gestion_char_2 = fields.Char('gestion 2',default='D.S 005-2012-TR, art.33, inciso H.')
	gestion_bol_2 = fields.Char('gestion 2')
	gestion_text_2 = fields.Text('gestion 2')
	gestion_char_3 = fields.Char('gestion 3',default='Ley 29783, art.43.')
	gestion_bol_3 = fields.Char('gestion 3')
	gestion_text_3 = fields.Text('gestion 3')
	gestion_char_4 = fields.Char('gestion 4',default='Ley 29783, art.43.')
	gestion_bol_4 = fields.Char('gestion 4')
	gestion_text_4 = fields.Text('gestion 4')
	gestion_char_5 = fields.Char('gestion 5',default='Ley 29783, art.46, inciso C.')
	gestion_bol_5 = fields.Char('gestion 5')
	gestion_text_5 = fields.Text('gestion 5')

	documentos_char_1 = fields.Char('documentos 1',default='Ley 29783, art.28.')
	documentos_bol_1 = fields.Char('documentos 1')
	documentos_text_1 = fields.Text('documentos 1')
	documentos_char_2 = fields.Char('documentos 2',default='Ley 29783, art.47.')
	documentos_bol_2 = fields.Char('documentos 2')
	documentos_text_2 = fields.Text('documentos 2')
	documentos_char_3 = fields.Char('documentos 3',default='D.S 005-2012-TR, art.37, incisos A,B y C.')
	documentos_bol_3 = fields.Char('documentos 3')
	documentos_text_3 = fields.Text('documentos 3')
	documentos_char_4 = fields.Char('documentos 4',default='Ley 29783, art.35, inciso C. D.S 005-2012-TR, art.30.')
	documentos_bol_4 = fields.Char('documentos 4')
	documentos_text_4 = fields.Text('documentos 4')
	documentos_char_5 = fields.Char('documentos 5',default='Ley 29783, art.35, incisos A,B,C,D y E.')
	documentos_bol_5 = fields.Char('documentos 5')
	documentos_text_5 = fields.Text('documentos 5')
	documentos_char_6 = fields.Char('documentos 6',default='D.S 005-2012-TR, art.84, inciso A.')
	documentos_bol_6 = fields.Char('documentos 6')
	documentos_text_6 = fields.Text('documentos 6')

	datos_char_1 = fields.Char('datos 1',default='Ley 29783, art.28.')
	datos_bol_1 = fields.Char('datos 1')
	datos_text_1 = fields.Text('datos 1')
	datos_char_2 = fields.Char('datos 2',default='Ley 29783, art.28.')
	datos_bol_2 = fields.Char('datos 2')
	datos_text_2 = fields.Text('datos 2')

	registros_char_1 = fields.Char('registros 1',default='D.S 005-2012-TR, art.33, inciso A.')
	registros_bol_1 = fields.Char('registros 1')
	registros_text_1 = fields.Text('registros 1')
	registros_char_2 = fields.Char('registros 2',default='D.S 005-2012-TR, art.33, inciso B.')
	registros_bol_2 = fields.Char('registros 2')
	registros_text_2 = fields.Text('registros 2')
	registros_char_3 = fields.Char('registros 3',default='D.S 005-2012-TR, art.33, inciso C.')
	registros_bol_3 = fields.Char('registros 3')
	registros_text_3 = fields.Text('registros 3')
	registros_char_4 = fields.Char('registros 4',default='D.S 005-2012-TR, art.33, inciso D.')
	registros_bol_4 = fields.Char('registros 4')
	registros_text_4 = fields.Text('registros 4')
	registros_char_5 = fields.Char('registros 5',default='D.S 005-2012-TR, art.33, inciso E.')
	registros_bol_5 = fields.Char('registros 5')
	registros_text_5 = fields.Text('registros 5')
	registros_char_6 = fields.Char('registros 6',default='D.S 005-2012-TR, art.33, inciso F.')
	registros_bol_6 = fields.Char('registros 6')
	registros_text_6 = fields.Text('registros 6')
	registros_char_7 = fields.Char('registros 7',default='D.S 005-2012-TR, art.33, inciso G.')
	registros_bol_7 = fields.Char('registros 7')
	registros_text_7 = fields.Text('registros 7')
	registros_char_8 = fields.Char('registros 8',default='D.S 005-2012-TR, art.33, inciso H.')
	registros_bol_8 = fields.Char('registros 8')
	registros_text_8 = fields.Text('registros 8')
	registros_char_9 = fields.Char('registros 9',default='D.S 005-2012-TR, art.34.')
	registros_bol_9 = fields.Char('registros 9')
	registros_text_9 = fields.Text('registros 9')
	registros_char_10 = fields.Char('registros 10',default='D.S 005-2012-TR, art.34.')
	registros_bol_10 = fields.Char('registros 10')
	registros_text_10 = fields.Text('registros 10')

	mejora_char_1 = fields.Char('mejora 1',default='Ley 29783, art.47.')
	mejora_bol_1 = fields.Char('mejora 1')
	mejora_text_1 = fields.Text('mejora 1')
	mejora_char_2 = fields.Char('mejora 2',default='Ley 29783, art. 46, incisos A,B,C,D,E,F,G.H e I.')
	mejora_bol_2 = fields.Char('mejora 2')
	mejora_text_2 = fields.Text('mejora 2')
	mejora_char_3 = fields.Char('mejora 3',default='Ley 29783, art. 20, inciso A.')
	mejora_bol_3 = fields.Char('mejora 3')
	mejora_text_3 = fields.Text('mejora 3')
	mejora_char_4 = fields.Char('mejora 4',default='Ley 29783, art.44.')
	mejora_bol_4 = fields.Char('mejora 4')
	mejora_text_4 = fields.Text('mejora 4')
	mejora_char_5 = fields.Char('mejora 5',default='Ley 29783, art.42.')
	mejora_bol_5 = fields.Char('mejora 5')
	mejora_text_5 = fields.Text('mejora 5')
	mejora_char_6 = fields.Char('mejora 6',default='Ley 29783,art. 93, inciso B.')
	mejora_bol_6 = fields.Char('mejora 6')
	mejora_text_6 = fields.Text('mejora 6')


	def file_excel(self):
		# lista = Workbook()
		# style1_0 = easyxf('font: height 210, name Arial Narrow, colour_index black; align:wrap on, horiz center, vertical center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;')
		# style1_2 = easyxf('font: bold on, height 210, name Arial Narrow, colour_index white; pattern: pattern solid, fore_colour green; align:wrap on, horiz center, vertical center; borders: top_color black, bottom_color black, right_color black, left_color black, left thin, right thin, top thin, bottom thin;')

		# ws = lista.add_sheet(u'lista_verificacion')
		# ws.write_merge(0, 0, 0, 2, u"{}".format(self.name if self.name else ""), style1_2)
		# ws.write_merge(0, 0, 3, 8, u"PERMISO DE TRABAJO", style1_2)
		# ws.write(0, 1, u"EVALUADO POR"), style1_0)
		# ws.write(1, 1, u"{}".format(self.evaluado if self.evaluado else ""), style1_0)
		# ws.write(2, 2, u"{}".format(self.empresa if self.empresa else ""), style1_0)

		# file_name = io.BytesIO()
		# lista.save(file_name)

		# self.write({
		#     'txt_excel_cal': u'PermisosTrabajo.xls',
		#     'txt_binary_excel_cal': base64.encodestring(file_name.getvalue())
		# })
			self.ensure_one()
			# workbook = xlsxwriter.Workbook(u'C:\\Program Files (x86)\\Odoo 13.0\\server\\addons\\excel.xlsx')
			workbook = xlsxwriter.Workbook(u'/odoopreventor/custom/excel.xlsx')
			reporte = workbook.add_format()
			head = workbook.add_format()
			tbody = workbook.add_format()
			codigo = workbook.add_format()
			cabecera = workbook.add_format()
			titulo = workbook.add_format()
			texto = workbook.add_format()

			head.set_bold()
			reporte.set_bold()
			reporte.set_align('vcenter')
			reporte.set_font_size(16)
			reporte.set_fg_color('#FFFF00')
			reporte.set_align('center')
			head.set_font_color("white")
			head.set_font_name('Arial')
			head.set_font_size(10)
			head.set_align('center')
			codigo.set_align('right')
			codigo.set_border(1)
			head.set_align('vcenter')
			head.set_text_wrap()
			head.set_fg_color('#7da7d8')
			head.set_border(1)
			tbody.set_border(1)
			formato = workbook.add_format()
			formato.set_font_color("black")
			formato.set_font_name('Arial')
			formato.set_font_size(8)
			formato.set_align('center')
			formato.set_align('vcenter')
			formato.set_text_wrap()
			formato.set_border(1)
			formatos = workbook.add_format()
			formatos.set_font_color("black")
			formatos.set_font_name('Arial')
			formatos.set_font_size(8)
			formatos.set_align('center')
			formatos.set_align('vcenter')
			formatos.set_text_wrap()
			formatos.set_fg_color('#7da7d8')
			formatos.set_border(1)
			formaton = workbook.add_format()
			formaton.set_font_color("black")
			formaton.set_font_name('Arial')
			formaton.set_font_size(8)
			formaton.set_align('center')
			formaton.set_align('vcenter')
			formaton.set_text_wrap()
			formaton.set_fg_color('#7da7d8')
			formaton.set_border(1)
			cabecera.set_align('vcenter')
			cabecera.set_align('center')
			cabecera.set_text_wrap()
			cabecera.set_bold()
			cabecera.set_border(2)
			cabecera.set_fg_color('#000080')
			cabecera.set_font_color("white")
			cabecera.set_font_name('Arial')
			cabecera.set_font_size(10)
			titulo.set_align('vcenter')
			titulo.set_align('left')
			titulo.set_text_wrap()
			titulo.set_bold()
			titulo.set_border(2)
			titulo.set_font_name('Arial')
			titulo.set_font_size(8)
			texto.set_align('vcenter')
			texto.set_align('left')
			texto.set_text_wrap()
			texto.set_border(2)
			texto.set_font_name('Arial')
			texto.set_font_size(8)
			worksheet = workbook.add_worksheet(u"ListaVerificación")
			worksheet.set_row(0, 30)
			worksheet.set_column('A:A', 20)
			worksheet.set_column('B:B', 0.1)
			worksheet.set_column('C:D', 20)
			worksheet.set_column('E:E', 5)
			worksheet.set_column('F:G', 0.1)
			worksheet.set_column('H:H', 12)
			worksheet.set_column('I:I', 0.1)
			worksheet.set_column('J:K', 8)
			worksheet.set_column('L:M', 12)
			# worksheet.set_row(0, 40)
			today = date.today()
			my_date = datetime.now(pytz.timezone('America/Lima'))
			now = datetime.now()
			fecha_actual = today.strftime("%d/%m/%Y")
			hora_actual = my_date.strftime('%H:%M:%S')

			worksheet.merge_range('A1:M1', u"REPORTE LISTA DE VERIFICACIÓN", reporte)
			worksheet.write(2, 0, u"CÓDIGO", head)
			worksheet.write(3, 0, u"FECHA", head)
			worksheet.write(4, 0, u"HORA", head)
			worksheet.write(5, 0, u"EVALUADO POR", head)
			worksheet.write(6, 0, u"EMPRESA", head)
			worksheet.write(7, 0, u"PUNTAJE OBTENIDO", head)
			worksheet.write(10, 0, u"ACTIVIDADES", head)
			worksheet.merge_range('B11:C11', u"Nº", head)
			worksheet.write(11, 0, u"ACTIVIDADES CUMPLIDAS", head)
			worksheet.write(12, 0, u"ACTIVIDADES SIN CUMPLIR", head)
			worksheet.write(13, 0, u"ACTIVIDADES FALTANTES", head)
			worksheet.write(14, 0, u"% CUMPLIMIENTO", head)
			worksheet.merge_range('B3:C3', self.name, codigo)
			worksheet.merge_range('B4:C4', fecha_actual, codigo)
			worksheet.merge_range('B5:C5', hora_actual, codigo)
			worksheet.merge_range('B6:C6', self.evaluado, codigo)
			worksheet.merge_range('B7:C7', self.empresa, codigo)
			worksheet.merge_range('B8:C8', self.puntaje, codigo)
			worksheet.merge_range('B12:C12', self.count_si, tbody)
			worksheet.merge_range('B13:C13', self.count_no, tbody)
			worksheet.merge_range('B14:C14', self.count_total-(self.count_si+self.count_no), tbody)
			worksheet.merge_range('B15:C15', self.puntaje, tbody)



			# worksheet.write(1, 2, u"Puesto de Trabajo", head)
			# worksheet.write(1, 3, u"Ubicación del Punto", head)
			# worksheet.write(1, 4, u"Actividades", head)
			# worksheet.write(1, 5, u"Fuentes de Peligro", head)
			# worksheet.write(1, 6, u"Controles Existentes", head)
			# worksheet.write(1, 7, u"Tarea Visual", head)
			# worksheet.write(1, 8, u"Nivel de Iluminación (lux)", head)
			# worksheet.write(1, 9, u"Nivel Mínimo Recomendado (lux)", head)
			# worksheet.write(1, 10, u"¿Cumple con la R.M. N°375-2008-TR?", head)
			# data = [10, 40, 50, 20, 10, 50]
			# worksheet.write_column('C1', data)
			chart = workbook.add_chart({
				'type': 'column'
				})
			chart.add_series({
				'name': 'Actividades',
				'categories': '=ListaVerificación!$A$12:$A$14',
				'values': '=ListaVerificación!$B$12:$B$14',
				'fill':   {'color': '#FF9900'}
			})
			chart.set_legend({'none': True})
			chart.set_size({'width': 435})
			worksheet.insert_chart('E2', chart)

			worksheet.merge_range('A17:B17', u"LINEAMIENTOS", cabecera)
			worksheet.merge_range('C17:G17', u"INDICADOR", cabecera)
			worksheet.merge_range('H17:I17', u"FUENTE", cabecera)
			worksheet.write('J17', "SI", cabecera)
			worksheet.write('K17', "NO", cabecera)
			worksheet.merge_range('L17:M17', u"OBSERVACIÓN", cabecera)
			worksheet.merge_range('A19:B38', u"Principios", titulo)
			worksheet.merge_range('A18:M18', u"I. Compromiso e Involucramiento", titulo)
			worksheet.merge_range('C19:G20', u"El empleador proporciona los recursos necesarios para que se implemente un sistema de gestión de seguridad y salud en el trabajo", texto)
			worksheet.merge_range('C21:G22', u"Se ha cumplido lo planificado en los diferentes programas de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C23:G24', u"Se implementan acciones preventivas de seguridad y salud en el trabajo para asegurar la mejora continua.", texto)
			worksheet.merge_range('C25:G26', u"Se reconoce el desempeño del trabajador para mejorar la autoestima y se fomenta el trabajo en equipo.", texto)
			worksheet.merge_range('C27:G28', u"Se realizan actividades para fomentar una cultura de prevención de riesgos del trabajo en toda la empresa, entidad pública o privada.", texto)
			worksheet.merge_range('C29:G30', u"Se promueve un buen clima laboral para reforzar la empatía entre empleador y trabajador y viceversa", texto)
			worksheet.merge_range('C31:G32', u"Existen medios que permiten el aporte de los trabajadores al empleador en materia de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C33:G34', u"Existen mecanismos de reconocimiento del personal proactivo interesado en el mejoramiento continuo de la seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C35:G36', u"Se tiene evaluado los principales riesgos que ocasionan mayores pérdidas.", texto)
			worksheet.merge_range('C37:G38', u"Se fomenta la participación de los representantes de trabajadores y de las organizaciones sindicales en las decisiones sobre la seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('H19:I20', self.principios_char_1, texto)
			worksheet.merge_range('H21:I22', self.principios_char_2, texto)
			worksheet.merge_range('H23:I24', self.principios_char_3, texto)
			worksheet.merge_range('H25:I26', self.principios_char_4, texto)
			worksheet.merge_range('H27:I28', self.principios_char_5, texto)
			worksheet.merge_range('H29:I30', self.principios_char_6, texto)
			worksheet.merge_range('H31:I32', self.principios_char_7, texto)
			worksheet.merge_range('H33:I34', self.principios_char_8, texto)
			worksheet.merge_range('H35:I36', self.principios_char_9, texto)
			worksheet.merge_range('H37:I38', self.principios_char_10, texto)
			worksheet.merge_range('L19:M20', "{}".format(self.principios_text_1 if self.principios_text_1 else ""), texto)
			worksheet.merge_range('L21:M22', "{}".format(self.principios_text_2 if self.principios_text_2 else ""), texto)
			worksheet.merge_range('L23:M24', "{}".format(self.principios_text_3 if self.principios_text_3 else ""), texto)
			worksheet.merge_range('L25:M26', "{}".format(self.principios_text_4 if self.principios_text_4 else ""), texto)
			worksheet.merge_range('L27:M28', "{}".format(self.principios_text_5 if self.principios_text_5 else ""), texto)
			worksheet.merge_range('L29:M30', "{}".format(self.principios_text_6 if self.principios_text_6 else ""), texto)
			worksheet.merge_range('L31:M32', "{}".format(self.principios_text_7 if self.principios_text_7 else ""), texto)
			worksheet.merge_range('L33:M34', "{}".format(self.principios_text_8 if self.principios_text_8 else ""), texto)
			worksheet.merge_range('L35:M36', "{}".format(self.principios_text_9 if self.principios_text_9 else ""), texto)
			worksheet.merge_range('L37:M38', "{}".format(self.principios_text_10 if self.principios_text_10 else ""), texto)
			if self.principios_bol_1 == "SI":
				worksheet.merge_range('J19:J20', 'X', texto)
				worksheet.merge_range('K19:K20', '', texto)
			elif self.principios_bol_1 == "NO":
				worksheet.merge_range('J19:J20', '', texto)
				worksheet.merge_range('K19:K20', 'X', texto)
			else:
				worksheet.merge_range('J19:J20', '', texto)
				worksheet.merge_range('K19:K20', '', texto)
			if self.principios_bol_2 == "SI":
				worksheet.merge_range('J21:J22', 'X', texto)
				worksheet.merge_range('K21:K22', '', texto)
			elif self.principios_bol_2 == "NO":
				worksheet.merge_range('J21:J22', '', texto)
				worksheet.merge_range('K21:K22', 'X', texto)
			else:
				worksheet.merge_range('J21:J22', '', texto)
				worksheet.merge_range('K21:K22', '', texto)
			if self.principios_bol_3 == "SI":
				worksheet.merge_range('J23:J24', 'X', texto)
				worksheet.merge_range('K23:K24', '', texto)
			elif self.principios_bol_3 == "NO":
				worksheet.merge_range('J23:J24', '', texto)
				worksheet.merge_range('K23:K24', 'X', texto)
			else:
				worksheet.merge_range('J23:J24', '', texto)
				worksheet.merge_range('K23:K24', '', texto)
			if self.principios_bol_4 == "SI":
				worksheet.merge_range('J25:J26', 'X', texto)
				worksheet.merge_range('K25:K26', '', texto)
			elif self.principios_bol_4 == "NO":
				worksheet.merge_range('J25:J26', '', texto)
				worksheet.merge_range('K25:K26', 'X', texto)
			else:
				worksheet.merge_range('J25:J26', '', texto)
				worksheet.merge_range('K25:K26', '', texto)
			if self.principios_bol_5 == "SI":
				worksheet.merge_range('J27:J28', 'X', texto)
				worksheet.merge_range('K27:K28', '', texto)
			elif self.principios_bol_5 == "NO":
				worksheet.merge_range('J27:J28', '', texto)
				worksheet.merge_range('K27:K28', 'X', texto)
			else:
				worksheet.merge_range('J27:J28', '', texto)
				worksheet.merge_range('K27:K28', '', texto)
			if self.principios_bol_6 == "SI":
				worksheet.merge_range('J29:J30', 'X', texto)
				worksheet.merge_range('K29:K30', '', texto)
			elif self.principios_bol_6 == "NO":
				worksheet.merge_range('J29:J30', '', texto)
				worksheet.merge_range('K29:K30', 'X', texto)
			else:
				worksheet.merge_range('J29:J30', '', texto)
				worksheet.merge_range('K29:K30', '', texto)
			if self.principios_bol_7 == "SI":
				worksheet.merge_range('J31:J32', 'X', texto)
				worksheet.merge_range('K31:K32', '', texto)
			elif self.principios_bol_7 == "NO":
				worksheet.merge_range('J31:J32', '', texto)
				worksheet.merge_range('K31:K32', 'X', texto)
			else:
				worksheet.merge_range('J31:J32', '', texto)
				worksheet.merge_range('K31:K32', '', texto)
			if self.principios_bol_8 == "SI":
				worksheet.merge_range('J33:J34', 'X', texto)
				worksheet.merge_range('K33:K34', '', texto)
			elif self.principios_bol_8 == "NO":
				worksheet.merge_range('J33:J34', '', texto)
				worksheet.merge_range('K33:K34', 'X', texto)
			else:
				worksheet.merge_range('J33:J34', '', texto)
				worksheet.merge_range('K33:K34', '', texto)
			if self.principios_bol_9 == "SI":
				worksheet.merge_range('J35:J36', 'X', texto)
				worksheet.merge_range('K35:K36', '', texto)
			elif self.principios_bol_9 == "NO":
				worksheet.merge_range('J35:J36', '', texto)
				worksheet.merge_range('K35:K36', 'X', texto)
			else:
				worksheet.merge_range('J35:J36', '', texto)
				worksheet.merge_range('K35:K36', '', texto)
			if self.principios_bol_10 == "SI":
				worksheet.merge_range('J37:J38', 'X', texto)
				worksheet.merge_range('K37:K38', '', texto)
			elif self.principios_bol_10 == "NO":
				worksheet.merge_range('J37:J38', '', texto)
				worksheet.merge_range('K37:K38', 'X', texto)
			else:
				worksheet.merge_range('J37:J38', '', texto)
				worksheet.merge_range('K37:K38', '', texto)

			worksheet.merge_range('A40:B53', u"Política", titulo)
			worksheet.merge_range('A39:M39', u"II. Política de seguridad y salud ocupacional", titulo)
			worksheet.merge_range('C40:G41', u"Existe una política documentada en materia de seguridad y salud en el trabajo, específica y apropiada para la empresa, entidad pública o privada.", texto)
			worksheet.merge_range('C42:G43', u"La política de seguridad y salud en el trabajo está firmada por la máxima autoridad de la empresa, entidad pública o privada.", texto)
			worksheet.merge_range('C44:G45', u"Los trabajadores conocen y están comprometidos con lo establecido en la política de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C46:G53', u"Su contenido comprende:\n- El compromiso de protección de todos los miembros de la organización.\n- Cumplimiento de la normatividad.\n- Garantía de protección, participación, consulta y participación en los elementos del sistema de gestión de seguridad y salud en el trabajo por parte de los trabajadores y sus representantes.\n- La mejora continua en materia de seguridad y salud en el trabajo.\n- Integración del Sistema de Gestión de Seguridad y Salud en el Trabajo con otros sistemas de ser el caso.", texto)
			worksheet.merge_range('H40:I41', self.politica_char_1, texto)
			worksheet.merge_range('H42:I43', self.politica_char_2, texto)
			worksheet.merge_range('H44:I45', self.politica_char_3, texto)
			worksheet.merge_range('H46:I53', self.politica_char_4, texto)
			worksheet.merge_range('L40:M41', "{}".format(self.politica_text_1 if self.politica_text_1 else ""), texto)
			worksheet.merge_range('L42:M43', "{}".format(self.politica_text_2 if self.politica_text_2 else ""), texto)
			worksheet.merge_range('L44:M45', "{}".format(self.politica_text_3 if self.politica_text_3 else ""), texto)
			worksheet.merge_range('L46:M53', "{}".format(self.politica_text_4 if self.politica_text_4 else ""), texto)

			if self.politica_bol_1 == "SI":
				worksheet.merge_range('J40:J41', 'X', texto)
				worksheet.merge_range('K40:K41', '', texto)
			elif self.politica_bol_1 == "NO":
				worksheet.merge_range('J40:J41', '', texto)
				worksheet.merge_range('K40:K41', 'X', texto)
			else:
				worksheet.merge_range('J40:J41', '', texto)
				worksheet.merge_range('K40:K41', '', texto)
			if self.politica_bol_2 == "SI":
				worksheet.merge_range('J42:J43', 'X', texto)
				worksheet.merge_range('K42:K43', '', texto)
			elif self.politica_bol_2 == "NO":
				worksheet.merge_range('J42:J43', '', texto)
				worksheet.merge_range('K42:K43', 'X', texto)
			else:
				worksheet.merge_range('J42:J43', '', texto)
				worksheet.merge_range('K42:K43', '', texto)
			if self.politica_bol_3 == "SI":
				worksheet.merge_range('J44:J45', 'X', texto)
				worksheet.merge_range('K44:K45', '', texto)
			elif self.politica_bol_3 == "NO":
				worksheet.merge_range('J44:J45', '', texto)
				worksheet.merge_range('K44:K45', 'X', texto)
			else:
				worksheet.merge_range('J44:J45', '', texto)
				worksheet.merge_range('K44:K45', '', texto)
			if self.politica_bol_4 == "SI":
				worksheet.merge_range('J46:J53', 'X', texto)
				worksheet.merge_range('K46:K53', '', texto)
			elif self.politica_bol_4 == "NO":
				worksheet.merge_range('J46:J53', '', texto)
				worksheet.merge_range('K46:K53', 'X', texto)
			else:
				worksheet.merge_range('J46:J53', '', texto)
				worksheet.merge_range('K46:K53', '', texto)

			worksheet.merge_range('A54:B59', u"Direccion", titulo)
			worksheet.merge_range('C54:G57', u"Se toman decisiones en base al análisis de inspecciones, auditorias, informes de investigación de accidentes, informe de estadísticas, avances de programas de seguridad y salud en el trabajo y opiniones de trabajadores, dando el seguimiento de las mismas", texto)
			worksheet.merge_range('C58:G59', u"El empleador delega funciones y autoridad al personal encargado de implementar el sistema de gestión de Seguridad y Salud en el Trabajo.", texto)
			worksheet.merge_range('H54:I57', self.direccion_char_1, texto)
			worksheet.merge_range('H58:I59', self.direccion_char_2, texto)
			worksheet.merge_range('L54:M57', "{}".format(self.direccion_text_1 if self.direccion_text_2 else ""), texto)
			worksheet.merge_range('L58:M59', "{}".format(self.direccion_text_2 if self.direccion_text_2 else ""), texto)
			if self.direccion_bol_1 == "SI":
				worksheet.merge_range('J54:J57', 'X', texto)
				worksheet.merge_range('K54:K57', '', texto)
			elif self.direccion_bol_1 == "NO":
				worksheet.merge_range('J54:J57', '', texto)
				worksheet.merge_range('K54:K57', 'X', texto)
			else:
				worksheet.merge_range('J54:J57', '', texto)
				worksheet.merge_range('K54:K57', '', texto)
			if self.direccion_bol_2 == "SI":
				worksheet.merge_range('J58:J59', 'X', texto)
				worksheet.merge_range('K58:K59', '', texto)
			elif self.direccion_bol_2 == "NO":
				worksheet.merge_range('J58:J59', '', texto)
				worksheet.merge_range('K58:K59', 'X', texto)
			else:
				worksheet.merge_range('J58:J59', '', texto)
				worksheet.merge_range('K58:K59', '', texto)

			worksheet.merge_range('A60:B63', u"Liderazgo", titulo)
			worksheet.merge_range('C60:G61', u"El empleador asume el liderazgo en la gestión de la seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C62:G63', u"El empleador dispone los recursos necesarios para mejorar la gestión de la seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('H60:I61', self.liderazgo_char_1, texto)
			worksheet.merge_range('H62:I63', self.liderazgo_char_2, texto)
			worksheet.merge_range('L60:M61', "{}".format(self.liderazgo_text_1 if self.liderazgo_text_1 else ""), texto)
			worksheet.merge_range('L62:M63', "{}".format(self.liderazgo_text_2 if self.liderazgo_text_2 else ""), texto)
			if self.liderazgo_bol_1 == "SI":
				worksheet.merge_range('J60:J61', 'X', texto)
				worksheet.merge_range('K60:K61', '', texto)
			elif self.liderazgo_bol_1 == "NO":
				worksheet.merge_range('J60:J61', '', texto)
				worksheet.merge_range('K60:K61', 'X', texto)
			else:
				worksheet.merge_range('J60:J61', '', texto)
				worksheet.merge_range('K60:K61', '', texto)
			if self.liderazgo_bol_2 == "SI":
				worksheet.merge_range('J62:J63', 'X', texto)
				worksheet.merge_range('K62:K63', '', texto)
			elif self.liderazgo_bol_2 == "NO":
				worksheet.merge_range('J62:J63', '', texto)
				worksheet.merge_range('K62:K63', 'X', texto)
			else:
				worksheet.merge_range('J62:J63', '', texto)
				worksheet.merge_range('K62:K63', '', texto)

			worksheet.merge_range('A64:B69', u"Organizacion", titulo)
			worksheet.merge_range('C64:G65', u"Existen responsabilidades específicas en seguridad y salud en el trabajo de los niveles de mando de la empresa, entidad pública o privada.", texto)
			worksheet.merge_range('C66:G67', u"Se ha destinado presupuesto para implementar o mejorar el sistema de gestión de seguridad y salud el trabajo.", texto)
			worksheet.merge_range('C68:G69', u"El Comité o Supervisor de Seguridad y Salud en el Trabajo participa en la definición de estímulos y sanciones.", texto)
			worksheet.merge_range('H64:I65', self.organizacion_char_1, texto)
			worksheet.merge_range('H66:I67', self.organizacion_char_2, texto)
			worksheet.merge_range('H68:I69', self.organizacion_char_3, texto)
			worksheet.merge_range('L64:M65', "{}".format(self.organizacion_text_1 if self.organizacion_text_1 else ""), texto)
			worksheet.merge_range('L66:M67', "{}".format(self.organizacion_text_2 if self.organizacion_text_2 else ""), texto)
			worksheet.merge_range('L68:M69', "{}".format(self.organizacion_text_3 if self.organizacion_text_3 else ""), texto)
			if self.organizacion_bol_1 == "SI":
				worksheet.merge_range('J64:J65', 'X', texto)
				worksheet.merge_range('K64:K65', '', texto)
			elif self.organizacion_bol_1 == "NO":
				worksheet.merge_range('J64:J65', '', texto)
				worksheet.merge_range('K64:K65', 'X', texto)
			else:
				worksheet.merge_range('J64:J65', '', texto)
				worksheet.merge_range('K64:K65', '', texto)
			if self.organizacion_bol_2 == "SI":
				worksheet.merge_range('J66:J67', 'X', texto)
				worksheet.merge_range('K66:K67', '', texto)
			elif self.organizacion_bol_2 == "NO":
				worksheet.merge_range('J66:J67', '', texto)
				worksheet.merge_range('K66:K67', 'X', texto)
			else:
				worksheet.merge_range('J66:J67', '', texto)
				worksheet.merge_range('K66:K67', '', texto)
			if self.organizacion_bol_3 == "SI":
				worksheet.merge_range('J68:J69', 'X', texto)
				worksheet.merge_range('K68:K69', '', texto)
			elif self.organizacion_bol_3 == "NO":
				worksheet.merge_range('J68:J69', '', texto)
				worksheet.merge_range('K68:K69', 'X', texto)
			else:
				worksheet.merge_range('J68:J69', '', texto)
				worksheet.merge_range('K68:K69', '', texto)

			worksheet.merge_range('A70:B73', u"Competencia", titulo)
			worksheet.merge_range('C70:G73', u"Existen responsabilidades específicas en seguridad y salud en el trabajo de los niveles de mando de la empresa, entidad pública o privada.", texto)
			worksheet.merge_range('H70:I73', self.organizacion_char_4, texto)
			worksheet.merge_range('L70:M73', "{}".format(self.organizacion_text_4 if self.organizacion_text_4 else ""), texto)
			if self.organizacion_bol_4 == "SI":
				worksheet.merge_range('J70:J73', 'X', texto)
				worksheet.merge_range('K70:K73', '', texto)
			elif self.organizacion_bol_4 == "NO":
				worksheet.merge_range('J70:J73', '', texto)
				worksheet.merge_range('K70:K73', 'X', texto)
			else:
				worksheet.merge_range('J70:J73', '', texto)
				worksheet.merge_range('K70:K73', '', texto)

			worksheet.merge_range('A74:M74', u"III. Planeamiento y aplicación", titulo)
			worksheet.merge_range('A75:B84', u"Diagnostico", titulo)
			worksheet.merge_range('C75:G76', u"Se ha realizado una evaluación inicial o estudio de línea base como diagnóstico participativo del estado de la salud y seguridad en el trabajo.", texto)
			worksheet.merge_range('C77:G84', u"Los resultados han sido comparados con lo establecido en la Ley de SST y su Reglamento y otros dispositivos legales pertinentes, y servirán de base para planificar, aplicar el sistema y como referencia para medir su mejora continua.\nLa planificación permite:\n- Cumplir con normas nacionales\n- Mejorar el desempeño\n- Mantener procesos productivos seguros o de servicios seguros", texto)
			worksheet.merge_range('H75:I76', self.diagnostico_char_1, texto)
			worksheet.merge_range('H77:I84', self.diagnostico_char_2, texto)
			worksheet.merge_range('L75:M76', "{}".format(self.diagnostico_text_1 if self.diagnostico_text_1 else ""), texto)
			worksheet.merge_range('L77:M84', "{}".format(self.diagnostico_text_2 if self.diagnostico_text_2 else ""), texto)
			if self.diagnostico_bol_1 == "SI":
				worksheet.merge_range('J75:J76', 'X', texto)
				worksheet.merge_range('K75:K76', '', texto)
			elif self.diagnostico_bol_1 == "NO":
				worksheet.merge_range('J75:J76', '', texto)
				worksheet.merge_range('K75:K76', 'X', texto)
			else:
				worksheet.merge_range('J75:J76', '', texto)
				worksheet.merge_range('K75:K76', '', texto)
			if self.diagnostico_bol_2 == "SI":
				worksheet.merge_range('J77:J84', 'X', texto)
				worksheet.merge_range('K77:K84', '', texto)
			elif self.diagnostico_bol_2 == "NO":
				worksheet.merge_range('J77:J84', '', texto)
				worksheet.merge_range('K77:K84', 'X', texto)
			else:
				worksheet.merge_range('J77:J84', '', texto)
				worksheet.merge_range('K77:K84', '', texto)

			worksheet.merge_range('A85:B107', u"Planeamiento para la identificación de peligros, evaluación y control de riesgos", titulo)
			worksheet.merge_range('C85:G86', u"El empleador ha establecido procedimientos para identificar peligros y evaluar riesgos.", texto)
			worksheet.merge_range('C87:G90', u"Comprende estos procedimientos:\n- Todas las actividades\n- Todo el personal\n- Todas las instalaciones", texto)
			worksheet.merge_range('C91:G98', u"El empleador aplica medidas para:\n- Gestionar, eliminar y controlar riesgos.\n- Diseñar ambiente y puesto de trabajo, seleccionar equipos y métodos de trabajo que garanticen la seguridad y salud del trabajador.\n- Eliminar las situaciones y agentes peligrosos o sustituirlos.\n- Modernizar los planes y programas de prevención de riesgos laborales.\n- Mantener políticas de protección.\n- Capacitar anticipadamente al trabajador.", texto)
			worksheet.merge_range('C99:G100', u"El empleador actualiza la evaluación de riesgo una (01) vez al año como mínimo o cuando cambien las condiciones o se hayan producido daños.", texto)
			worksheet.merge_range('C101:G104', u"La evaluación de riesgo considera:\n- Controles periódicos de las condiciones de trabajo y de la salud de los trabajadores.\n- Medidas de prevención.", texto)
			worksheet.merge_range('C105:G107', u"Los representantes de los trabajadores han participado en la identificación de peligros y evaluación de riesgos, han sugerido las medidas de control y verificado su aplicación.", texto)
			worksheet.merge_range('H85:I86', self.planteamiento_char_1, texto)
			worksheet.merge_range('H87:I90', self.planteamiento_char_2, texto)
			worksheet.merge_range('H91:I98', self.planteamiento_char_3, texto)
			worksheet.merge_range('H99:I100', self.planteamiento_char_4, texto)
			worksheet.merge_range('H101:I104', self.planteamiento_char_5, texto)
			worksheet.merge_range('H105:I107', self.planteamiento_char_6, texto)
			worksheet.merge_range('L85:M86', "{}".format(self.planteamiento_text_1 if self.planteamiento_text_1 else ""), texto)
			worksheet.merge_range('L87:M90', "{}".format(self.planteamiento_text_2 if self.planteamiento_text_2 else ""), texto)
			worksheet.merge_range('L91:M98', "{}".format(self.planteamiento_text_3 if self.planteamiento_text_3 else ""), texto)
			worksheet.merge_range('L99:M100', "{}".format(self.planteamiento_text_4 if self.planteamiento_text_4 else ""), texto)
			worksheet.merge_range('L101:M104', "{}".format(self.planteamiento_text_5 if self.planteamiento_text_5 else ""), texto)
			worksheet.merge_range('L105:M107', "{}".format(self.planteamiento_text_6 if self.planteamiento_text_6 else ""), texto)
			if self.planteamiento_bol_1 == "SI":
				worksheet.merge_range('J85:J86', 'X', texto)
				worksheet.merge_range('K85:K86', '', texto)
			elif self.planteamiento_bol_1 == "NO":
				worksheet.merge_range('J85:J86', '', texto)
				worksheet.merge_range('K85:K86', 'X', texto)
			else:
				worksheet.merge_range('J85:J86', '', texto)
				worksheet.merge_range('K85:K86', '', texto)
			if self.planteamiento_bol_2 == "SI":
				worksheet.merge_range('J87:J90', 'X', texto)
				worksheet.merge_range('K87:K90', '', texto)
			elif self.planteamiento_bol_2 == "NO":
				worksheet.merge_range('J87:J90', '', texto)
				worksheet.merge_range('K87:K90', 'X', texto)
			else:
				worksheet.merge_range('J87:J90', '', texto)
				worksheet.merge_range('K87:K90', '', texto)
			if self.planteamiento_bol_3 == "SI":
				worksheet.merge_range('J91:J98', 'X', texto)
				worksheet.merge_range('K91:K98', '', texto)
			elif self.planteamiento_bol_3 == "NO":
				worksheet.merge_range('J91:J98', '', texto)
				worksheet.merge_range('K91:K98', 'X', texto)
			else:
				worksheet.merge_range('J91:J98', '', texto)
				worksheet.merge_range('K91:K98', '', texto)
			if self.planteamiento_bol_4 == "SI":
				worksheet.merge_range('J99:J100', 'X', texto)
				worksheet.merge_range('K99:K100', '', texto)
			elif self.planteamiento_bol_4 == "NO":
				worksheet.merge_range('J99:J100', '', texto)
				worksheet.merge_range('K99:K100', 'X', texto)
			else:
				worksheet.merge_range('J99:J100', '', texto)
				worksheet.merge_range('K99:K100', '', texto)
			if self.planteamiento_bol_5 == "SI":
				worksheet.merge_range('J101:J104', 'X', texto)
				worksheet.merge_range('K101:K104', '', texto)
			elif self.planteamiento_bol_5 == "NO":
				worksheet.merge_range('J101:J104', '', texto)
				worksheet.merge_range('K101:K104', 'X', texto)
			else:
				worksheet.merge_range('J101:J104', '', texto)
				worksheet.merge_range('K101:K104', '', texto)
			if self.planteamiento_bol_6 == "SI":
				worksheet.merge_range('J105:J107', 'X', texto)
				worksheet.merge_range('K105:K107', '', texto)
			elif self.planteamiento_bol_6 == "NO":
				worksheet.merge_range('J105:J107', '', texto)
				worksheet.merge_range('K105:K107', 'X', texto)
			else:
				worksheet.merge_range('J105:J107', '', texto)
				worksheet.merge_range('K105:K107', '', texto)

			worksheet.merge_range('A108:B119', u"Objetivos", titulo)
			worksheet.merge_range('C108:G116', u"Los objetivos se centran en el logro de resultados realistas y posibles de aplicar, que comprende:\n- Reducción de los riesgos del trabajo.\n- Reducción de los accidentes de trabajo y enfermedades ocupacionales.\n- La mejora continua de los procesos, la gestión del cambio, la preparación y respuesta a situaciones de emergencia.\n- Definición de metas, indicadores, responsabilidades.\n- Selección de criterios de medición para confirmar su logro.", texto)
			worksheet.merge_range('C117:G119', u"La empresa, entidad pública o privada cuenta con objetivos cuantificables de seguridad y salud en el trabajo que abarca a todos los niveles de la organización y están documentados.", texto)
			worksheet.merge_range('H108:I116', self.objetivos_char_1, texto)
			worksheet.merge_range('H117:I119', self.objetivos_char_2, texto)
			worksheet.merge_range('L108:M116', "{}".format(self.objetivos_text_1 if self.objetivos_text_1 else ""), texto)
			worksheet.merge_range('L117:M119', "{}".format(self.objetivos_text_2 if self.objetivos_text_2 else ""), texto)
			if self.objetivos_bol_1 == "SI":
				worksheet.merge_range('J108:J116', 'X', texto)
				worksheet.merge_range('K108:K116', '', texto)
			elif self.objetivos_bol_1 == "NO":
				worksheet.merge_range('J108:J116', '', texto)
				worksheet.merge_range('K108:K116', 'X', texto)
			else:
				worksheet.merge_range('J108:J116', '', texto)
				worksheet.merge_range('K108:K116', '', texto)
			if self.objetivos_bol_2 == "SI":
				worksheet.merge_range('J117:J119', 'X', texto)
				worksheet.merge_range('K117:K119', '', texto)
			elif self.objetivos_bol_2 == "NO":
				worksheet.merge_range('J117:J119', '', texto)
				worksheet.merge_range('K117:K119', 'X', texto)
			else:
				worksheet.merge_range('J117:J119', '', texto)
				worksheet.merge_range('K117:K119', '', texto)

			worksheet.merge_range('A120:B129', u"Programa de seguridad y salud en el trabajo", titulo)
			worksheet.merge_range('C120:G120', u"Existe un programa anual de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C121:G122', u"Las actividades programadas están relacionadas con el logro de los objetivos.", texto)
			worksheet.merge_range('C123:G124', u"Se definen responsables de las actividades en el programa de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C125:G126', u"Se definen tiempos y plazos para el cumplimiento y se realiza seguimiento periódico.", texto)
			worksheet.merge_range('C127:G127', u"Se señala dotación de recursos humanos y económicos.", texto)
			worksheet.merge_range('C128:G129', u"Se establecen actividades preventivas ante los riesgos que inciden en la función de procreación del trabajador.", texto)
			worksheet.merge_range('H120:I120', self.programa_char_1, texto)
			worksheet.merge_range('H121:I122', self.programa_char_2, texto)
			worksheet.merge_range('H123:I124', self.programa_char_3, texto)
			worksheet.merge_range('H125:I126', self.programa_char_4, texto)
			worksheet.merge_range('H127:I127', self.programa_char_5, texto)
			worksheet.merge_range('H128:I129', self.programa_char_6, texto)
			worksheet.merge_range('L120:M120', "{}".format(self.programa_text_1 if self.programa_text_1 else ""), texto)
			worksheet.merge_range('L121:M122', "{}".format(self.programa_text_2 if self.programa_text_2 else ""), texto)
			worksheet.merge_range('L123:M124', "{}".format(self.programa_text_3 if self.programa_text_3 else ""), texto)
			worksheet.merge_range('L125:M126', "{}".format(self.programa_text_4 if self.programa_text_4 else ""), texto)
			worksheet.merge_range('L127:M127', "{}".format(self.programa_text_5 if self.programa_text_5 else ""), texto)
			worksheet.merge_range('L128:M129', "{}".format(self.programa_text_6 if self.programa_text_6 else ""), texto)
			if self.programa_bol_1 == "SI":
				worksheet.write('J120', 'X', texto)
				worksheet.write('K120', '', texto)
			elif self.programa_bol_1 == "NO":
				worksheet.write('J120', '', texto)
				worksheet.write('K120', 'X', texto)
			else:
				worksheet.write('J120', '', texto)
				worksheet.write('K120', '', texto)
			if self.programa_bol_2 == "SI":
				worksheet.merge_range('J121:J122', 'X', texto)
				worksheet.merge_range('K121:K122', '', texto)
			elif self.programa_bol_2 == "NO":
				worksheet.merge_range('J121:J122', '', texto)
				worksheet.merge_range('K121:K122', 'X', texto)
			else:
				worksheet.merge_range('J121:J122', '', texto)
				worksheet.merge_range('K121:K122', '', texto)
			if self.programa_bol_3 == "SI":
				worksheet.merge_range('J123:J124', 'X', texto)
				worksheet.merge_range('K123:K124', '', texto)
			elif self.programa_bol_3 == "NO":
				worksheet.merge_range('J123:J124', '', texto)
				worksheet.merge_range('K123:K124', 'X', texto)
			else:
				worksheet.merge_range('J123:J124', '', texto)
				worksheet.merge_range('K123:K124', '', texto)
			if self.programa_bol_4 == "SI":
				worksheet.merge_range('J125:J126', 'X', texto)
				worksheet.merge_range('K125:K126', '', texto)
			elif self.programa_bol_4 == "NO":
				worksheet.merge_range('J125:J126', '', texto)
				worksheet.merge_range('K125:K126', 'X', texto)
			else:
				worksheet.merge_range('J125:J126', '', texto)
				worksheet.merge_range('K125:K126', '', texto)
			if self.programa_bol_5 == "SI":
				worksheet.write('J127', 'X', texto)
				worksheet.write('K127', '', texto)
			elif self.programa_bol_5 == "NO":
				worksheet.write('J127', '', texto)
				worksheet.write('K127', 'X', texto)
			else:
				worksheet.write('J127', '', texto)
				worksheet.write('K127', '', texto)
			if self.programa_bol_6 == "SI":
				worksheet.merge_range('J128:J129', 'X', texto)
				worksheet.merge_range('K128:K129', '', texto)
			elif self.programa_bol_6 == "NO":
				worksheet.merge_range('J128:J129', '', texto)
				worksheet.merge_range('K128:K129', 'X', texto)
			else:
				worksheet.merge_range('J128:J129', '', texto)
				worksheet.merge_range('K128:K129', '', texto)

			worksheet.merge_range('A130:M130', u"IV. Implementación y operación", titulo)
			worksheet.merge_range('A131:B150', u"Estructura y responsabilidades", titulo)
			worksheet.merge_range('C131:G132', u"El Comité de Seguridad y Salud en el Trabajo está constituido de forma paritaria. (Para el caso de empleadores con 20 o más trabajadores).", texto)
			worksheet.merge_range('C133:G134', u"Existe al menos un Supervisor de Seguridad y Salud (para el caso de empleadores con menos de 20 trabajadores).", texto)
			worksheet.merge_range('C135:G141', u"El empleador es responsable de:\n- Garantizar la seguridad y salud de los trabajadores.\n- Actúa para mejorar el nivel de seguridad y salud en el trabajo.\n- Actúa en tomar medidas de prevención de riesgo ante modificaciones de las condiciones de trabajo.\n- Realiza los exámenes médicos ocupacionales al trabajador antes, durante y al término de la relación laboral.", texto)
			worksheet.merge_range('C142:G143', u"El empleador considera las competencias del trabajador en materia de seguridad y salud en el trabajo, al asignarle sus labores.", texto)
			worksheet.merge_range('C144:G145', u"El empleador controla que solo el personal capacitado y protegido acceda a zonas de alto riesgo.", texto)
			worksheet.merge_range('C146:G148', u"El empleador prevé que la exposición a agentes físicos, químicos, biológicos, disergonómicos y psicosociales no generen daño al trabajador o trabajadora.", texto)
			worksheet.merge_range('C149:G150', u"El empleador asume los costos de las acciones de seguridad y salud ejecutadas en el centro de trabajo.", texto)
			worksheet.merge_range('H131:I132', self.estructura_char_1, texto)
			worksheet.merge_range('H133:I134', self.estructura_char_2, texto)
			worksheet.merge_range('H135:I141', self.estructura_char_3, texto)
			worksheet.merge_range('H142:I143', self.estructura_char_4, texto)
			worksheet.merge_range('H144:I145', self.estructura_char_5, texto)
			worksheet.merge_range('H146:I148', self.estructura_char_6, texto)
			worksheet.merge_range('H149:I150', self.estructura_char_7, texto)
			worksheet.merge_range('L131:M132', "{}".format(self.estructura_text_1 if self.estructura_text_1 else ""), texto)
			worksheet.merge_range('L133:M134', "{}".format(self.estructura_text_2 if self.estructura_text_2 else ""), texto)
			worksheet.merge_range('L135:M141', "{}".format(self.estructura_text_3 if self.estructura_text_3 else ""), texto)
			worksheet.merge_range('L142:M143', "{}".format(self.estructura_text_4 if self.estructura_text_4 else ""), texto)
			worksheet.merge_range('L144:M145', "{}".format(self.estructura_text_5 if self.estructura_text_5 else ""), texto)
			worksheet.merge_range('L146:M148', "{}".format(self.estructura_text_6 if self.estructura_text_6 else ""), texto)
			worksheet.merge_range('L149:M150', "{}".format(self.estructura_text_7 if self.estructura_text_7 else ""), texto)
			if self.estructura_bol_1 == "SI":
				worksheet.merge_range('J131:J132', 'X', texto)
				worksheet.merge_range('K131:K132', '', texto)
			elif self.estructura_bol_1 == "NO":
				worksheet.merge_range('J131:J132', '', texto)
				worksheet.merge_range('K131:K132', 'X', texto)
			else:
				worksheet.merge_range('J131:J132', '', texto)
				worksheet.merge_range('K131:K132', '', texto)
			if self.estructura_bol_2 == "SI":
				worksheet.merge_range('J133:J134', 'X', texto)
				worksheet.merge_range('K133:K134', '', texto)
			elif self.estructura_bol_2 == "NO":
				worksheet.merge_range('J133:J134', '', texto)
				worksheet.merge_range('K133:K134', 'X', texto)
			else:
				worksheet.merge_range('J133:J134', '', texto)
				worksheet.merge_range('K133:K134', '', texto)
			if self.estructura_bol_3 == "SI":
				worksheet.merge_range('J135:J141', 'X', texto)
				worksheet.merge_range('K135:K141', '', texto)
			elif self.estructura_bol_3 == "NO":
				worksheet.merge_range('J135:J141', '', texto)
				worksheet.merge_range('K135:K141', 'X', texto)
			else:
				worksheet.merge_range('J135:J141', '', texto)
				worksheet.merge_range('K135:K141', '', texto)
			if self.estructura_bol_4 == "SI":
				worksheet.merge_range('J142:J143', 'X', texto)
				worksheet.merge_range('K142:K143', '', texto)
			elif self.estructura_bol_4 == "NO":
				worksheet.merge_range('J142:J143', '', texto)
				worksheet.merge_range('K142:K143', 'X', texto)
			else:
				worksheet.merge_range('J142:J143', '', texto)
				worksheet.merge_range('K142:K143', '', texto)
			if self.estructura_bol_5 == "SI":
				worksheet.merge_range('J144:J145', 'X', texto)
				worksheet.merge_range('K144:K145', '', texto)
			elif self.estructura_bol_5 == "NO":
				worksheet.merge_range('J144:J145', '', texto)
				worksheet.merge_range('K144:K145', 'X', texto)
			else:
				worksheet.merge_range('J144:J145', '', texto)
				worksheet.merge_range('K144:K145', '', texto)
			if self.estructura_bol_6 == "SI":
				worksheet.merge_range('J146:J148', 'X', texto)
				worksheet.merge_range('K146:K148', '', texto)
			elif self.estructura_bol_6 == "NO":
				worksheet.merge_range('J146:J148', '', texto)
				worksheet.merge_range('K146:K148', 'X', texto)
			else:
				worksheet.merge_range('J146:J148', '', texto)
				worksheet.merge_range('K146:K148', '', texto)
			if self.estructura_bol_7 == "SI":
				worksheet.merge_range('J149:J150', 'X', texto)
				worksheet.merge_range('K149:K150', '', texto)
			elif self.estructura_bol_7 == "NO":
				worksheet.merge_range('J149:J150', '', texto)
				worksheet.merge_range('K149:K150', 'X', texto)
			else:
				worksheet.merge_range('J149:J150', '', texto)
				worksheet.merge_range('K149:K150', '', texto)

			worksheet.merge_range('A151:B180', u"Capacitacion", titulo)
			worksheet.merge_range('C151:G153', u"El empleador toma medidas para transmitir al trabajador información sobre los riesgos en el centro de trabajo y las medidas de protección que corresponda.", texto)
			worksheet.merge_range('C154:G154', u"El empleador imparte la capacitación dentro de la jornada de trabajo.", texto)
			worksheet.merge_range('C155:G156', u"El costo de las capacitaciones es íntegramente asumido por el empleador.", texto)
			worksheet.merge_range('C157:G158', u"Los representantes de los trabajadores han revisado el programa de capacitación.", texto)
			worksheet.merge_range('C159:G160', u"La capacitación se imparte por personal competente y con experiencia en la materia.", texto)
			worksheet.merge_range('C161:G162', u"Se ha capacitado a los integrantes del comité de seguridad y salud en el trabajo o al supervisor de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C163:G163', u"Las capacitaciones están documentadas.", texto)
			worksheet.merge_range('C164:G180', u"Se han realizado capacitaciones de seguridad y salud en el trabajo:\n- Al momento de la contratación, cualquiera sea la modalidad o duración.\n- Durante el desempeño de la labor.\n- Específica en el puesto de trabajo o en la función que cada trabajador desempeña, cualquiera que sea la naturaleza del vínculo, modalidad o duración de su contrato.\n- Cuando se produce cambios en las funciones que desempeña el trabajador.\n- Cuando se produce cambios en las tecnologías o en los equipos de trabajo.\n- En las medidas que permitan la adaptación a la evolución de los riesgos y la prevención de nuevos riesgos.\n- Para la actualización periódica de los conocimientos.\n- Utilización y mantenimiento preventivo de las maquinarias y equipos.\n- Uso apropiado de los materiales peligrosos.", texto)
			worksheet.merge_range('H151:I153', self.capacitacion_char_1, texto)
			worksheet.merge_range('H154:I154', self.capacitacion_char_2, texto)
			worksheet.merge_range('H155:I156', self.capacitacion_char_3, texto)
			worksheet.merge_range('H157:I158', self.capacitacion_char_4, texto)
			worksheet.merge_range('H159:I160', self.capacitacion_char_5, texto)
			worksheet.merge_range('H161:I162', self.capacitacion_char_6, texto)
			worksheet.merge_range('H163:I163', self.capacitacion_char_7, texto)
			worksheet.merge_range('H164:I180', self.capacitacion_char_8, texto)
			worksheet.merge_range('L151:M153', "{}".format(self.capacitacion_text_1 if self.capacitacion_text_1 else ""), texto)
			worksheet.merge_range('L154:M154', "{}".format(self.capacitacion_text_2 if self.capacitacion_text_2 else ""), texto)
			worksheet.merge_range('L155:M156', "{}".format(self.capacitacion_text_3 if self.capacitacion_text_3 else ""), texto)
			worksheet.merge_range('L157:M158', "{}".format(self.capacitacion_text_4 if self.capacitacion_text_4 else ""), texto)
			worksheet.merge_range('L159:M160', "{}".format(self.capacitacion_text_5 if self.capacitacion_text_5 else ""), texto)
			worksheet.merge_range('L161:M162', "{}".format(self.capacitacion_text_6 if self.capacitacion_text_6 else ""), texto)
			worksheet.merge_range('L163:M163', "{}".format(self.capacitacion_text_7 if self.capacitacion_text_7 else ""), texto)
			worksheet.merge_range('L164:M180', "{}".format(self.capacitacion_text_8 if self.capacitacion_text_8 else ""), texto)
			if self.capacitacion_bol_1 == "SI":
				worksheet.merge_range('J151:J153', 'X', texto)
				worksheet.merge_range('K151:K153', '', texto)
			elif self.capacitacion_bol_1 == "NO":
				worksheet.merge_range('J151:J153', '', texto)
				worksheet.merge_range('K151:K153', 'X', texto)
			else:
				worksheet.merge_range('J151:J153', '', texto)
				worksheet.merge_range('K151:K153', '', texto)

			if self.capacitacion_bol_2 == "SI":
				worksheet.write('J154', 'X', texto)
				worksheet.write('K154', '', texto)
			elif self.capacitacion_bol_2 == "NO":
				worksheet.write('J154', '', texto)
				worksheet.write('K154', 'X', texto)
			else:
				worksheet.write('J154', '', texto)
				worksheet.write('K154', '', texto)

			if self.capacitacion_bol_3 == "SI":
				worksheet.merge_range('J155:J156', 'X', texto)
				worksheet.merge_range('K155:K156', '', texto)
			elif self.capacitacion_bol_3 == "NO":
				worksheet.merge_range('J155:J156', '', texto)
				worksheet.merge_range('K155:K156', 'X', texto)
			else:
				worksheet.merge_range('J155:J156', '', texto)
				worksheet.merge_range('K155:K156', '', texto)

			if self.capacitacion_bol_4 == "SI":
				worksheet.merge_range('J157:J158', 'X', texto)
				worksheet.merge_range('K157:K158', '', texto)
			elif self.capacitacion_bol_4 == "NO":
				worksheet.merge_range('J157:J158', '', texto)
				worksheet.merge_range('K157:K158', 'X', texto)
			else:
				worksheet.merge_range('J157:J158', '', texto)
				worksheet.merge_range('K157:K158', '', texto)

			if self.capacitacion_bol_5 == "SI":
				worksheet.merge_range('J159:J160', 'X', texto)
				worksheet.merge_range('K159:K160', '', texto)
			elif self.capacitacion_bol_5 == "NO":
				worksheet.merge_range('J159:J160', '', texto)
				worksheet.merge_range('K159:K160', 'X', texto)
			else:
				worksheet.merge_range('J159:J160', '', texto)
				worksheet.merge_range('K159:K160', '', texto)

			if self.capacitacion_bol_6 == "SI":
				worksheet.merge_range('J161:J162', 'X', texto)
				worksheet.merge_range('K161:K162', '', texto)
			elif self.capacitacion_bol_6 == "NO":
				worksheet.merge_range('J161:J162', '', texto)
				worksheet.merge_range('K161:K162', 'X', texto)
			else:
				worksheet.merge_range('J161:J162', '', texto)
				worksheet.merge_range('K161:K162', '', texto)

			if self.capacitacion_bol_7 == "SI":
				worksheet.write('J163', 'X', texto)
				worksheet.write('K163', '', texto)
			elif self.capacitacion_bol_7 == "NO":
				worksheet.write('J163', '', texto)
				worksheet.write('K163', 'X', texto)
			else:
				worksheet.merge_range('J163', '', texto)
				worksheet.write('K163', '', texto)

			if self.capacitacion_bol_8 == "SI":
				worksheet.merge_range('J164:J180', 'X', texto)
				worksheet.merge_range('K164:K180', '', texto)
			elif self.capacitacion_bol_8 == "NO":
				worksheet.merge_range('J164:J180', '', texto)
				worksheet.merge_range('K164:K180', 'X', texto)
			else:
				worksheet.merge_range('J164:J180', '', texto)
				worksheet.merge_range('K164:K180', '', texto)

			worksheet.merge_range('A181:B194', u"Medidas de prevención", titulo)
			worksheet.merge_range('C181:G194', u"Las medidas de prevención y protección se aplican en el orden de prioridad:\n- Eliminación de los peligros y riesgos.\n- Tratamiento, control o aislamiento de los peligros y riesgos, adoptando medidas técnicas o administrativas\n- Minimizar los peligros y riesgos, adoptando sistemas de trabajo seguro que incluyan disposiciones administrativas de control.\n- Programar la sustitución progresiva y en la brevedad posible, de los procedimientos, técnicas, medios, sustancias y productos peligrosos por aquellos que produzcan un menor riesgo o ningún riesgo para el trabajador.\n- En último caso, facilitar equipos de protección personal adecuados, asegurándose que los trabajadores los utilicen y conserven en forma correcta.", texto)
			worksheet.merge_range('H181:I194', self.medidas_char_1, texto)
			worksheet.merge_range('L181:M194', "{}".format(self.medidas_text_1 if self.medidas_text_1 else ""), texto)
			if self.medidas_bol_1 == "SI":
				worksheet.merge_range('J181:J194', 'X', texto)
				worksheet.merge_range('K181:K194', '', texto)
			elif self.medidas_bol_1 == "NO":
				worksheet.merge_range('J181:J194', '', texto)
				worksheet.merge_range('K181:K194', 'X', texto)
			else:
				worksheet.merge_range('J181:J194', '', texto)
				worksheet.merge_range('K181:K194', '', texto)

			worksheet.merge_range('A195:B204', u"Preparación y respuestas ante emergencias", titulo)
			worksheet.merge_range('C195:G197', u"La empresa, entidad pública o privada ha elaborado planes y procedimientos para enfrentar y responder ante situaciones de emergencias.", texto)
			worksheet.merge_range('C198:G199', u"Se tiene organizada la brigada para actuar en caso de: incendios, primeros auxilios, evacuación.", texto)
			worksheet.merge_range('C200:G201', u"La empresa, entidad pública o privada revisa los planes y procedimientos ante situaciones de emergencias en forma periódica.", texto)
			worksheet.merge_range('C202:G204', u"El empleador ha dado las instrucciones a los trabajadores para que en caso de un peligro grave e inminente puedan interrumpir sus labores y/o evacuar la zona de riesgo.", texto)
			worksheet.merge_range('H195:I197', self.preparacion_char_1, texto)
			worksheet.merge_range('H198:I199', self.preparacion_char_2, texto)
			worksheet.merge_range('H200:I201', self.preparacion_char_3, texto)
			worksheet.merge_range('H202:I204', self.preparacion_char_4, texto)
			worksheet.merge_range('L195:M197', "{}".format(self.preparacion_text_1 if self.preparacion_text_1 else ""), texto)
			worksheet.merge_range('L198:M199', "{}".format(self.preparacion_text_2 if self.preparacion_text_2 else ""), texto)
			worksheet.merge_range('L200:M201', "{}".format(self.preparacion_text_3 if self.preparacion_text_3 else ""), texto)
			worksheet.merge_range('L202:M204', "{}".format(self.preparacion_text_4 if self.preparacion_text_4 else ""), texto)
			if self.preparacion_bol_1 == "SI":
				worksheet.merge_range('J195:J197', 'X', texto)
				worksheet.merge_range('K195:K197', '', texto)
			elif self.preparacion_bol_1 == "NO":
				worksheet.merge_range('J195:J197', '', texto)
				worksheet.merge_range('K195:K197', 'X', texto)
			else:
				worksheet.merge_range('J195:J197', '', texto)
				worksheet.merge_range('K195:K197', '', texto)
			if self.preparacion_bol_2 == "SI":
				worksheet.merge_range('J198:J199', 'X', texto)
				worksheet.merge_range('K198:K199', '', texto)
			elif self.preparacion_bol_2 == "NO":
				worksheet.merge_range('J198:J199', '', texto)
				worksheet.merge_range('K198:K199', 'X', texto)
			else:
				worksheet.merge_range('J198:J199', '', texto)
				worksheet.merge_range('K198:K199', '', texto)
			if self.preparacion_bol_3 == "SI":
				worksheet.merge_range('J200:J201', 'X', texto)
				worksheet.merge_range('K200:K201', '', texto)
			elif self.preparacion_bol_3 == "NO":
				worksheet.merge_range('J200:J201', '', texto)
				worksheet.merge_range('K200:K201', 'X', texto)
			else:
				worksheet.merge_range('J200:J201', '', texto)
				worksheet.merge_range('K200:K201', '', texto)
			if self.preparacion_bol_4 == "SI":
				worksheet.merge_range('J202:J204', 'X', texto)
				worksheet.merge_range('K202:K204', '', texto)
			elif self.preparacion_bol_4 == "NO":
				worksheet.merge_range('J202:J204', '', texto)
				worksheet.merge_range('K202:K204', 'X', texto)
			else:
				worksheet.merge_range('J202:J204', '', texto)
				worksheet.merge_range('K202:K204', '', texto)

			worksheet.merge_range('A205:B219', u"Contratistas, Subcontratistas, empresa, entidad pública o privada, de servicios y cooperativas", titulo)
			worksheet.merge_range('C205:G215', u"El empleador que asume el contrato principal en cuyas instalaciones desarrollan actividades, trabajadores de contratistas, subcontratistas, empresas especiales de servicios y cooperativas de trabajadores, garantiza:\n- La coordinación de la gestión en prevención de riesgos laborales.\n- La seguridad y salud de los trabajadores.\n- La verificación de la contratación de los seguros de acuerdo a ley por cada empleador.\n- La vigilancia del cumplimiento de la normatividad en materia de seguridad y salud en el trabajo por parte de la empresa, entidad pública o privada que destacan su personal.", texto)
			worksheet.merge_range('C216:G219', u"Se tiene organizada la brigada para actuar en caso de: incendios, primeros auxilios, evacuación.", texto)
			worksheet.merge_range('H205:I215', self.contratista_char_1, texto)
			worksheet.merge_range('H216:I219', self.contratista_char_2, texto)
			worksheet.merge_range('L205:M215', "{}".format(self.contratista_text_1 if self.contratista_text_1 else ""), texto)
			worksheet.merge_range('L216:M219', "{}".format(self.contratista_text_2 if self.contratista_text_2 else ""), texto)
			if self.contratista_bol_1 == "SI":
				worksheet.merge_range('J205:J215', 'X', texto)
				worksheet.merge_range('K205:K215', '', texto)
			elif self.contratista_bol_1 == "NO":
				worksheet.merge_range('J205:J215', '', texto)
				worksheet.merge_range('K205:K215', 'X', texto)
			else:
				worksheet.merge_range('J205:J215', '', texto)
				worksheet.merge_range('K205:K215', '', texto)
			if self.contratista_bol_2 == "SI":
				worksheet.merge_range('J216:J219', 'X', texto)
				worksheet.merge_range('K216:K219', '', texto)
			elif self.contratista_bol_2 == "NO":
				worksheet.merge_range('J216:J219', '', texto)
				worksheet.merge_range('K216:K219', 'X', texto)
			else:
				worksheet.merge_range('J216:J219', '', texto)
				worksheet.merge_range('K216:K219', '', texto)

			worksheet.merge_range('A220:B233', u"Consulta y comunicación", titulo)
			worksheet.merge_range('C220:G226', u"Los trabajadores han participado en:\n- La consulta, información y capacitación en seguridad y salud en el trabajo.\n- La elección de sus representantes ante el Comité de seguridad y salud en el trabajo.\n- La conformación del Comité de seguridad y salud en el trabajo.\n- El reconocimiento de sus representantes por parte del empleador.", texto)
			worksheet.merge_range('C227:G230', u"Los trabajadores han sido consultados ante los cambios realizados en las operaciones, procesos y organización del trabajo que repercuta en su seguridad y salud.", texto)
			worksheet.merge_range('C231:G233', u"Existen procedimientos para asegurar que las informaciones pertinentes lleguen a los trabajadores correspondientes de la organización", texto)
			worksheet.merge_range('H220:I226', self.consulta_char_1, texto)
			worksheet.merge_range('H227:I230', self.consulta_char_2, texto)
			worksheet.merge_range('H231:I233', self.consulta_char_3, texto)
			worksheet.merge_range('L220:M226', "{}".format(self.consulta_text_1 if self.consulta_text_1 else ""), texto)
			worksheet.merge_range('L227:M230', "{}".format(self.consulta_text_2 if self.consulta_text_2 else ""), texto)
			worksheet.merge_range('L231:M233', "{}".format(self.consulta_text_3 if self.consulta_text_3 else ""), texto)
			if self.consulta_bol_1 == "SI":
				worksheet.merge_range('J220:J226', 'X', texto)
				worksheet.merge_range('K220:K226', '', texto)
			elif self.consulta_bol_1 == "NO":
				worksheet.merge_range('J220:J226', '', texto)
				worksheet.merge_range('K220:K226', 'X', texto)
			else:
				worksheet.merge_range('J220:J226', '', texto)
				worksheet.merge_range('K220:K226', '', texto)

			if self.consulta_bol_2 == "SI":
				worksheet.merge_range('J227:J230', 'X', texto)
				worksheet.merge_range('K227:K230', '', texto)
			elif self.consulta_bol_2 == "NO":
				worksheet.merge_range('J227:J230', '', texto)
				worksheet.merge_range('K227:K230', 'X', texto)
			else:
				worksheet.merge_range('J227:J230', '', texto)
				worksheet.merge_range('K227:K230', '', texto)

			if self.consulta_bol_3 == "SI":
				worksheet.merge_range('J231:J233', 'X', texto)
				worksheet.merge_range('K231:K233', '', texto)
			elif self.consulta_bol_3 == "NO":
				worksheet.merge_range('J231:J233', '', texto)
				worksheet.merge_range('K231:K233', 'X', texto)
			else:
				worksheet.merge_range('J231:J233', '', texto)
				worksheet.merge_range('K231:K233', '', texto)

			worksheet.merge_range('A234:M234', u"V. Evaluación normativa", titulo)
			worksheet.merge_range('A235:B297', u"Requisitos legales y de otro tipo", titulo)
			worksheet.merge_range('C235:G238', u"La empresa, entidad pública o privada tiene un procedimiento para identificar, acceder y monitorear el cumplimiento de la normatividad aplicable al sistema de gestión de seguridad y salud en el trabajo y se mantiene actualizada.", texto)
			worksheet.merge_range('C239:G240', u"La empresa, entidad pública o privada con 20 o más trabajadores ha elaborado su Reglamento Interno de Seguridad y Salud en el Trabajo.", texto)
			worksheet.merge_range('C241:G243', u"La empresa, entidad pública o privada con 20 o más trabajadores tiene un Libro del Comité de Seguridad y Salud en el Trabajo (Salvo que una norma sectorial no establezca un número mínimo inferior).", texto)
			worksheet.merge_range('C244:G245', u"Los equipos a presión que posee la empresa entidad pública o privada tienen su libro de servicio autorizado por el MTPE.", texto)
			worksheet.merge_range('C246:G249', u"El empleador adopta las medidas necesarias y oportunas, cuando detecta que la utilización de ropas y/o equipos de trabajo o de protección personal representan riesgos específicos para la seguridad y salud de los trabajadores.", texto)
			worksheet.merge_range('C250:G251', u"El empleador toma medidas que eviten las labores peligrosas a trabajadoras en periodo de embarazo o lactancia conforme a ley.", texto)
			worksheet.merge_range('C252:G253', u"El empleador no emplea a niños, ni adolescentes en actividades peligrosas.", texto)
			worksheet.merge_range('C254:G257', u"El empleador evalúa el puesto de trabajo que va a desempeñar un adolescente trabajador previamente a su incorporación laboral a fin de determinar la naturaleza, el grado y la duración de la exposición al riesgo, con el objeto de adoptar medidas preventivas necesarias.", texto)
			worksheet.merge_range('C258:G271', u"La empresa, entidad pública o privada dispondrá lo necesario para que:\n- Las máquinas, equipos, sustancias, productos o útiles de trabajo no constituyan una fuente de peligro.\n- Se proporcione información y capacitación sobre la instalación, adecuada utilización y mantenimiento preventivo de las maquinarias y equipos\n- Se proporcione información y capacitación para el uso apropiado de los materiales peligrosos.\n- Las instrucciones, manuales, avisos de peligro u otras medidas de precaución colocadas en los equipos y maquinarias estén traducido al castellano.\n- Las informaciones relativas a las máquinas, equipos, productos, sustancias o útiles de trabajo son comprensibles para los trabajadores.", texto)
			worksheet.merge_range('C272:G297', u"Los trabajadores cumplen con:\n- Las normas, reglamentos e instrucciones de los programas de seguridad y salud en el trabajo que se apliquen en el lugar de trabajo y con las instrucciones que les impartan sus superiores jerárquicos directos.\n- Usar adecuadamente los instrumentos y materiales de trabajo, así como los equipos de protección personal y colectiva.\n- No operar o manipular equipos, maquinarias, herramientas u otros elementos para los cuales no hayan sido autorizados y, en caso de ser necesario, capacitados.\n- Cooperar y participar en el proceso de investigación de los accidentes de trabajo, incidentes peligrosos, otros incidentes y las enfermedades ocupacionales cuando la autoridad competente lo requier\n- Velar por el cuidado integral individual y colectivo, de su salud física y mental.\n- Someterse a exámenes médicos obligatorios.\n- Participar en los organismos paritarios de seguridad y salud en el trabajo.\n- Comunicar al empleador situaciones que ponga o pueda poner en riesgo su seguridad y salud y/o las instalaciones físicas.\n- Reportar a los representantes de seguridad de forma inmediata, la ocurrencia de cualquier accidente de trabajo, incidente peligroso o incidente.\n- Concurrir a la capacitación y entrenamiento sobre seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('H235:I238', self.requisitos_char_1, texto)
			worksheet.merge_range('H239:I240', self.requisitos_char_2, texto)
			worksheet.merge_range('H241:I243', self.requisitos_char_3, texto)
			worksheet.merge_range('H244:I245', self.requisitos_char_4, texto)
			worksheet.merge_range('H246:I249', self.requisitos_char_5, texto)
			worksheet.merge_range('H250:I251', self.requisitos_char_6, texto)
			worksheet.merge_range('H252:I253', self.requisitos_char_7, texto)
			worksheet.merge_range('H254:I257', self.requisitos_char_8, texto)
			worksheet.merge_range('H258:I271', self.requisitos_char_9, texto)
			worksheet.merge_range('H272:I297', self.requisitos_char_10, texto)
			worksheet.merge_range('L235:M238', "{}".format(self.requisitos_text_1 if self.requisitos_text_1 else ""), texto)
			worksheet.merge_range('L239:M240', "{}".format(self.requisitos_text_2 if self.requisitos_text_2 else ""), texto)
			worksheet.merge_range('L241:M243', "{}".format(self.requisitos_text_3 if self.requisitos_text_3 else ""), texto)
			worksheet.merge_range('L244:M245', "{}".format(self.requisitos_text_4 if self.requisitos_text_4 else ""), texto)
			worksheet.merge_range('L246:M249', "{}".format(self.requisitos_text_5 if self.requisitos_text_5 else ""), texto)
			worksheet.merge_range('L250:M251', "{}".format(self.requisitos_text_6 if self.requisitos_text_6 else ""), texto)
			worksheet.merge_range('L252:M253', "{}".format(self.requisitos_text_7 if self.requisitos_text_7 else ""), texto)
			worksheet.merge_range('L254:M257', "{}".format(self.requisitos_text_8 if self.requisitos_text_8 else ""), texto)
			worksheet.merge_range('L258:M271', "{}".format(self.requisitos_text_9 if self.requisitos_text_9 else ""), texto)
			worksheet.merge_range('L272:M297', "{}".format(self.requisitos_text_10 if self.requisitos_text_10 else ""), texto)
			if self.requisitos_bol_1 == "SI":
				worksheet.merge_range('J235:J238', 'X', texto)
				worksheet.merge_range('K235:K238', '', texto)
			elif self.requisitos_bol_1 == "NO":
				worksheet.merge_range('J235:J238', '', texto)
				worksheet.merge_range('K235:K238', 'X', texto)
			else:
				worksheet.merge_range('J235:J238', '', texto)
				worksheet.merge_range('K235:K238', '', texto)

			if self.requisitos_bol_2 == "SI":
				worksheet.merge_range('J239:J240', 'X', texto)
				worksheet.merge_range('K239:K240', '', texto)
			elif self.requisitos_bol_2 == "NO":
				worksheet.merge_range('J239:J240', '', texto)
				worksheet.merge_range('K239:K240', 'X', texto)
			else:
				worksheet.merge_range('J239:J240', '', texto)
				worksheet.merge_range('K239:K240', '', texto)

			if self.requisitos_bol_3 == "SI":
				worksheet.merge_range('J241:J243', 'X', texto)
				worksheet.merge_range('K241:K243', '', texto)
			elif self.requisitos_bol_3 == "NO":
				worksheet.merge_range('J241:J243', '', texto)
				worksheet.merge_range('K241:K243', 'X', texto)
			else:
				worksheet.merge_range('J241:J243', '', texto)
				worksheet.merge_range('K241:K243', '', texto)

			if self.requisitos_bol_4 == "SI":
				worksheet.merge_range('J244:J245', 'X', texto)
				worksheet.merge_range('K244:K245', '', texto)
			elif self.requisitos_bol_4 == "NO":
				worksheet.merge_range('J244:J245', '', texto)
				worksheet.merge_range('K244:K245', 'X', texto)
			else:
				worksheet.merge_range('J244:J245', '', texto)
				worksheet.merge_range('K244:K245', '', texto)

			if self.requisitos_bol_5 == "SI":
				worksheet.merge_range('J246:J249', 'X', texto)
				worksheet.merge_range('K246:K249', '', texto)
			elif self.requisitos_bol_5 == "NO":
				worksheet.merge_range('J246:J249', '', texto)
				worksheet.merge_range('K246:K249', 'X', texto)
			else:
				worksheet.merge_range('J246:J249', '', texto)
				worksheet.merge_range('K246:K249', '', texto)

			if self.requisitos_bol_6 == "SI":
				worksheet.merge_range('J250:J251', 'X', texto)
				worksheet.merge_range('K250:K251', '', texto)
			elif self.requisitos_bol_6 == "NO":
				worksheet.merge_range('J250:J251', '', texto)
				worksheet.merge_range('K250:K251', 'X', texto)
			else:
				worksheet.merge_range('J250:J251', '', texto)
				worksheet.merge_range('K250:K251', '', texto)

			if self.requisitos_bol_7 == "SI":
				worksheet.merge_range('J252:J253', 'X', texto)
				worksheet.merge_range('K252:K253', '', texto)
			elif self.requisitos_bol_7 == "NO":
				worksheet.merge_range('J252:J253', '', texto)
				worksheet.merge_range('K252:K253', 'X', texto)
			else:
				worksheet.merge_range('J252:J253', '', texto)
				worksheet.merge_range('K252:K253', '', texto)

			if self.requisitos_bol_8 == "SI":
				worksheet.merge_range('J254:J257', 'X', texto)
				worksheet.merge_range('K254:K257', '', texto)
			elif self.requisitos_bol_8 == "NO":
				worksheet.merge_range('J254:J257', '', texto)
				worksheet.merge_range('K254:K257', 'X', texto)
			else:
				worksheet.merge_range('J254:J257', '', texto)
				worksheet.merge_range('K254:K257', '', texto)

			if self.requisitos_bol_9 == "SI":
				worksheet.merge_range('J258:J271', 'X', texto)
				worksheet.merge_range('K258:K271', '', texto)
			elif self.requisitos_bol_9 == "NO":
				worksheet.merge_range('J258:J271', '', texto)
				worksheet.merge_range('K258:K271', 'X', texto)
			else:
				worksheet.merge_range('J258:J271', '', texto)
				worksheet.merge_range('K258:K271', '', texto)

			if self.requisitos_bol_10 == "SI":
				worksheet.merge_range('J272:J297', 'X', texto)
				worksheet.merge_range('K272:K297', '', texto)
			elif self.requisitos_bol_10 == "NO":
				worksheet.merge_range('J272:J297', '', texto)
				worksheet.merge_range('K272:K297', 'X', texto)
			else:
				worksheet.merge_range('J272:J297', '', texto)
				worksheet.merge_range('K272:K297', '', texto)

			worksheet.merge_range('A298:M298', u"VI. Verificación", titulo)
			worksheet.merge_range('A299:B308', u"Supervisión, monitoreo y seguimiento de desempeño", titulo)
			worksheet.merge_range('C299:G301', u"La vigilancia y control de la seguridad y salud en el trabajo permite evaluar con regularidad los resultados logrados en materia de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C302:G305', u"La supervisión permite:\n- Identificar las fallas o deficiencias en el sistema de gestión de la seguridad y salud en el trabajo.\n- Adoptar las medidas preventivas y correctivas.", texto)
			worksheet.merge_range('C306:G306', u"El monitoreo permite la medición cuantitativa y cualitativa apropiadas.", texto)
			worksheet.merge_range('C307:G308', u"Se monitorea el grado de cumplimiento de los objetivos de la seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('H299:I301', self.supervision_char_1, texto)
			worksheet.merge_range('H302:I305', self.supervision_char_2, texto)
			worksheet.merge_range('H306:I306', self.supervision_char_3, texto)
			worksheet.merge_range('H307:I308', self.supervision_char_4, texto)
			worksheet.merge_range('L299:M301', "{}".format(self.supervision_text_1 if self.supervision_text_1 else ""), texto)
			worksheet.merge_range('L302:M305', "{}".format(self.supervision_text_2 if self.supervision_text_2 else ""), texto)
			worksheet.merge_range('L306:M306', "{}".format(self.supervision_text_3 if self.supervision_text_3 else ""), texto)
			worksheet.merge_range('L307:M308', "{}".format(self.supervision_text_4 if self.supervision_text_4 else ""), texto)
			if self.supervision_bol_1 == "SI":
				worksheet.merge_range('J299:J301', 'X', texto)
				worksheet.merge_range('K299:K301', '', texto)
			elif self.supervision_bol_1 == "NO":
				worksheet.merge_range('J299:J301', '', texto)
				worksheet.merge_range('K299:K301', 'X', texto)
			else:
				worksheet.merge_range('J299:J301', '', texto)
				worksheet.merge_range('K299:K301', '', texto)

			if self.supervision_bol_2 == "SI":
				worksheet.merge_range('J302:J305', 'X', texto)
				worksheet.merge_range('K302:K305', '', texto)
			elif self.supervision_bol_2 == "NO":
				worksheet.merge_range('J302:J305', '', texto)
				worksheet.merge_range('K302:K305', 'X', texto)
			else:
				worksheet.merge_range('J302:J305', '', texto)
				worksheet.merge_range('K302:K305', '', texto)

			if self.supervision_bol_3 == "SI":
				worksheet.write('J306', 'X', texto)
				worksheet.write('K306', '', texto)
			elif self.supervision_bol_3 == "NO":
				worksheet.write('J306', '', texto)
				worksheet.write('K306', 'X', texto)
			else:
				worksheet.write('J306', '', texto)
				worksheet.write('K306', '', texto)

			if self.supervision_bol_4 == "SI":
				worksheet.merge_range('J307:J308', 'X', texto)
				worksheet.merge_range('K307:K308', '', texto)
			elif self.supervision_bol_4 == "NO":
				worksheet.merge_range('J307:J308', '', texto)
				worksheet.merge_range('K307:K308', 'X', texto)
			else:
				worksheet.merge_range('J307:J308', '', texto)
				worksheet.merge_range('K307:K308', '', texto)

			worksheet.merge_range('A309:B330', u"Salud en el trabajo", titulo)
			worksheet.merge_range('C309:G310', u"El empleador realiza exámenes médicos antes, durante y al término de la relación laboral a los trabajadores (incluyendo a los adolescentes).", texto)
			worksheet.merge_range('C311:G317', u"Los trabajadores son informados:\n- A título grupal, de las razones para los exámenes de salud ocupacional.\n- A título personal, sobre los resultados de los informes médicos relativos a la evaluación de su salud.\n- Los resultados de los exámenes médicos no son pasibles de uso para ejercer discriminación.", texto)
			worksheet.merge_range('C318:G319', u"Los resultados de los exámenes médicos son considerados para tomar acciones preventivas o correctivas al respecto.", texto)
			worksheet.merge_range('C320:G321', u"El empleador notifica al Ministerio de Trabajo y Promoción del Empleo los accidentes de trabajo mortales dentro de las 24 horas de ocurridos.", texto)
			worksheet.merge_range('C322:G325', u"El empleador notifica al Ministerio de Trabajo y Promoción del Empleo, dentro de las 24 horas de producidos, los incidentes peligrosos que han puesto en riesgo la salud y la integridad física de los trabajadores y/o a la población.", texto)
			worksheet.merge_range('C326:G327', u"Se implementan las medidas correctivas propuestas en los registros de accidentes de trabajo, incidentes peligrosos y otros incidentes.", texto)
			worksheet.merge_range('C328:G329', u"Se implementan las medidas correctivas producto de la no conformidad hallada en las auditorías de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C330:G330', u"Se implementan medidas preventivas de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('H309:I310', self.salud_char_1, texto)
			worksheet.merge_range('H311:I317', self.salud_char_2, texto)
			worksheet.merge_range('H318:I319', self.salud_char_3, texto)
			worksheet.merge_range('H320:I321', self.salud_char_4, texto)
			worksheet.merge_range('H322:I325', self.salud_char_5, texto)
			worksheet.merge_range('H326:I327', self.salud_char_6, texto)
			worksheet.merge_range('H328:I329', self.salud_char_7, texto)
			worksheet.merge_range('H330:I330', self.salud_char_8, texto)
			worksheet.merge_range('L309:M310', "{}".format(self.salud_text_1 if self.salud_text_1 else ""), texto)
			worksheet.merge_range('L311:M317', "{}".format(self.salud_text_2 if self.salud_text_2 else ""), texto)
			worksheet.merge_range('L318:M319', "{}".format(self.salud_text_3 if self.salud_text_3 else ""), texto)
			worksheet.merge_range('L320:M321', "{}".format(self.salud_text_4 if self.salud_text_4 else ""), texto)
			worksheet.merge_range('L322:M325', "{}".format(self.salud_text_5 if self.salud_text_5 else ""), texto)
			worksheet.merge_range('L326:M327', "{}".format(self.salud_text_6 if self.salud_text_6 else ""), texto)
			worksheet.merge_range('L328:M329', "{}".format(self.salud_text_7 if self.salud_text_7 else ""), texto)
			worksheet.merge_range('L330:M330', "{}".format(self.salud_text_8 if self.salud_text_8 else ""), texto)

			if self.salud_bol_1 == "SI":
				worksheet.merge_range('J309:J310', 'X', texto)
				worksheet.merge_range('K309:K310', '', texto)
			elif self.salud_bol_1 == "NO":
				worksheet.merge_range('J309:J310', '', texto)
				worksheet.merge_range('K309:K310', 'X', texto)
			else:
				worksheet.merge_range('J309:J310', '', texto)
				worksheet.merge_range('K309:K310', '', texto)

			if self.salud_bol_2 == "SI":
				worksheet.merge_range('J311:J317', 'X', texto)
				worksheet.merge_range('K311:K317', '', texto)
			elif self.salud_bol_2 == "NO":
				worksheet.merge_range('J311:J317', '', texto)
				worksheet.merge_range('K311:K317', 'X', texto)
			else:
				worksheet.merge_range('J311:J317', '', texto)
				worksheet.merge_range('K311:K317', '', texto)

			if self.salud_bol_3 == "SI":
				worksheet.merge_range('J318:J319', 'X', texto)
				worksheet.merge_range('K318:K319', '', texto)
			elif self.salud_bol_3 == "NO":
				worksheet.merge_range('J318:J319', '', texto)
				worksheet.merge_range('K318:K319', 'X', texto)
			else:
				worksheet.merge_range('J318:J319', '', texto)
				worksheet.merge_range('K318:K319', '', texto)

			if self.salud_bol_4 == "SI":
				worksheet.merge_range('J320:J321', 'X', texto)
				worksheet.merge_range('K320:K321', '', texto)
			elif self.salud_bol_4 == "NO":
				worksheet.merge_range('J320:J321', '', texto)
				worksheet.merge_range('K320:K321', 'X', texto)
			else:
				worksheet.merge_range('J320:J321', '', texto)
				worksheet.merge_range('K320:K321', '', texto)

			if self.salud_bol_5 == "SI":
				worksheet.merge_range('J322:J325', 'X', texto)
				worksheet.merge_range('K322:K325', '', texto)
			elif self.salud_bol_5 == "NO":
				worksheet.merge_range('J322:J325', '', texto)
				worksheet.merge_range('K322:K325', 'X', texto)
			else:
				worksheet.merge_range('J322:J325', '', texto)
				worksheet.merge_range('K322:K325', '', texto)

			if self.salud_bol_6 == "SI":
				worksheet.merge_range('J326:J327', 'X', texto)
				worksheet.merge_range('K326:K327', '', texto)
			elif self.salud_bol_6 == "NO":
				worksheet.merge_range('J326:J327', '', texto)
				worksheet.merge_range('K326:K327', 'X', texto)
			else:
				worksheet.merge_range('J326:J327', '', texto)
				worksheet.merge_range('K326:K327', '', texto)

			if self.salud_bol_7 == "SI":
				worksheet.merge_range('J328:J329', 'X', texto)
				worksheet.merge_range('K328:K329', '', texto)
			elif self.salud_bol_7 == "NO":
				worksheet.merge_range('J328:J329', '', texto)
				worksheet.merge_range('K328:K329', 'X', texto)
			else:
				worksheet.merge_range('J328:J329', '', texto)
				worksheet.merge_range('K328:K329', '', texto)

			if self.salud_bol_8 == "SI":
				worksheet.write('J330', 'X', texto)
				worksheet.write('K330', '', texto)
			elif self.salud_bol_8 == "NO":
				worksheet.write('J330', '', texto)
				worksheet.write('K330', 'X', texto)
			else:
				worksheet.write('J330', '', texto)
				worksheet.write('K330', '', texto)

			worksheet.merge_range('A331:B346', u"Investigación de accidentes y enfermedades ocupacionales", titulo)
			worksheet.merge_range('C331:G334', u"El empleador ha realizado las investigaciones de accidentes de trabajo, enfermedades ocupacionales e incidentes peligrosos, y ha comunicado a la autoridad administrativa de trabajo, indicando las medidas correctivas y preventivas adoptadas.", texto)
			worksheet.merge_range('C335:G340', u"Se investiga los accidentes de trabajo, enfermedades ocupacionales e incidentes peligrosos para:\n- Determinar las causas e implementar las medidas correctivas.\n- Comprobar la eficacia de las medidas de seguridad y salud vigentes al momento de hecho.\n- Determinar la necesidad modificar dichas medidas.", texto)
			worksheet.merge_range('C341:G342', u"Se toma medidas correctivas para reducir las consecuencias de accidentes.", texto)
			worksheet.merge_range('C343:G344', u"Se ha documentado los cambios en los procedimientos como consecuencia de las acciones correctivas.", texto)
			worksheet.merge_range('C345:G346', u"El trabajador ha sido transferido en caso de accidente de trabajo o enfermedad ocupacional a otro puesto que implique menos riesgo.", texto)
			worksheet.merge_range('H331:I334', self.investigacion_char_1, texto)
			worksheet.merge_range('H335:I340', self.investigacion_char_2, texto)
			worksheet.merge_range('H341:I342', self.investigacion_char_3, texto)
			worksheet.merge_range('H343:I344', self.investigacion_char_4, texto)
			worksheet.merge_range('H345:I346', self.investigacion_char_5, texto)
			worksheet.merge_range('L331:M334', "{}".format(self.investigacion_text_1 if self.investigacion_text_1 else ""), texto)
			worksheet.merge_range('L335:M340', "{}".format(self.investigacion_text_2 if self.investigacion_text_2 else ""), texto)
			worksheet.merge_range('L341:M342', "{}".format(self.investigacion_text_3 if self.investigacion_text_3 else ""), texto)
			worksheet.merge_range('L343:M344', "{}".format(self.investigacion_text_4 if self.investigacion_text_4 else ""), texto)
			worksheet.merge_range('L345:M346', "{}".format(self.investigacion_text_5 if self.investigacion_text_5 else ""), texto)
			if self.investigacion_bol_1 == "SI":
				worksheet.merge_range('J331:J334', 'X', texto)
				worksheet.merge_range('K331:K334', '', texto)
			elif self.investigacion_bol_1 == "NO":
				worksheet.merge_range('J331:J334', '', texto)
				worksheet.merge_range('K331:K334', 'X', texto)
			else:
				worksheet.merge_range('J331:J334', '', texto)
				worksheet.merge_range('K331:K334', '', texto)

			if self.investigacion_bol_2 == "SI":
				worksheet.merge_range('J335:J340', 'X', texto)
				worksheet.merge_range('K335:K340', '', texto)
			elif self.investigacion_bol_2 == "NO":
				worksheet.merge_range('J335:J340', '', texto)
				worksheet.merge_range('K335:K340', 'X', texto)
			else:
				worksheet.merge_range('J335:J340', '', texto)
				worksheet.merge_range('K335:K340', '', texto)

			if self.investigacion_bol_3 == "SI":
				worksheet.merge_range('J341:J342', 'X', texto)
				worksheet.merge_range('K341:K342', '', texto)
			elif self.investigacion_bol_3 == "NO":
				worksheet.merge_range('J341:J342', '', texto)
				worksheet.merge_range('K341:K342', 'X', texto)
			else:
				worksheet.merge_range('J341:J342', '', texto)
				worksheet.merge_range('K341:K342', '', texto)

			if self.investigacion_bol_4 == "SI":
				worksheet.merge_range('J343:J344', 'X', texto)
				worksheet.merge_range('K343:K344', '', texto)
			elif self.investigacion_bol_4 == "NO":
				worksheet.merge_range('J343:J344', '', texto)
				worksheet.merge_range('K343:K344', 'X', texto)
			else:
				worksheet.merge_range('J343:J344', '', texto)
				worksheet.merge_range('K343:K344', '', texto)

			if self.investigacion_bol_5 == "SI":
				worksheet.merge_range('J345:J346', 'X', texto)
				worksheet.merge_range('K345:K346', '', texto)
			elif self.investigacion_bol_5 == "NO":
				worksheet.merge_range('J345:J346', '', texto)
				worksheet.merge_range('K345:K346', 'X', texto)
			else:
				worksheet.merge_range('J345:J346', '', texto)
				worksheet.merge_range('K345:K346', '', texto)

			worksheet.merge_range('A347:B353', u"Control de las operaciones", titulo)
			worksheet.merge_range('C347:G349', u"La empresa, entidad pública o privada ha identificado las operaciones y actividades que están asociadas con riesgos donde las medidas de control necesitan ser aplicadas.", texto)
			worksheet.merge_range('C350:G353', u"La empresa, entidad pública o privada ha establecido procedimientos para el diseño del lugar de trabajo, procesos operativos, instalaciones, maquinarias y organización del trabajo que incluye la adaptación a las capacidades humanas a modo de reducir los riesgos en sus fuentes.", texto)
			worksheet.merge_range('H347:I349', self.control_char_1, texto)
			worksheet.merge_range('H350:I353', self.control_char_1, texto)
			worksheet.merge_range('L347:M349', "{}".format(self.control_text_1 if self.control_text_1 else ""), texto)
			worksheet.merge_range('L350:M353', "{}".format(self.control_text_2 if self.control_text_2 else ""), texto)

			if self.control_bol_1 == "SI":
				worksheet.merge_range('J347:J349', 'X', texto)
				worksheet.merge_range('K347:K349', '', texto)
			elif self.control_bol_1 == "NO":
				worksheet.merge_range('J347:J349', '', texto)
				worksheet.merge_range('K347:K349', 'X', texto)
			else:
				worksheet.merge_range('J347:J349', '', texto)
				worksheet.merge_range('K347:K349', '', texto)

			if self.control_bol_2 == "SI":
				worksheet.merge_range('J350:J353', 'X', texto)
				worksheet.merge_range('K350:K353', '', texto)
			elif self.control_bol_2 == "NO":
				worksheet.merge_range('J350:J353', '', texto)
				worksheet.merge_range('K350:K353', 'X', texto)
			else:
				worksheet.merge_range('J350:J353', '', texto)
				worksheet.merge_range('K350:K353', '', texto)

			worksheet.merge_range('A354:B366', u"Gestión del cambio", titulo)
			worksheet.merge_range('C354:G358', u"Se ha evaluado las medidas de seguridad debido a cambios internos, método de trabajo, estructura organizativa y cambios externos normativos, conocimientos en el campo de la seguridad, cambios tecnológicos, adaptándose las medidas de prevención antes de introducirlos.", texto)
			worksheet.merge_range('C359:G359', u"Se cuenta con un programa de auditorías.", texto)
			worksheet.merge_range('C360:G362', u"El empleador realiza auditorías internas periódicas para comprobar la adecuada aplicación del sistema de gestión de la seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C363:G364', u"Las auditorías externas son realizadas por auditores independientes con la participación de los trabajadores o sus representantes.", texto)
			worksheet.merge_range('C365:G366', u"Los resultados de las auditorías son comunicados a la alta dirección de la empresa, entidad pública o privada.", texto)
			worksheet.merge_range('H354:I358', self.gestion_char_1, texto)
			worksheet.merge_range('H359:I359', self.gestion_char_2, texto)
			worksheet.merge_range('H360:I362', self.gestion_char_3, texto)
			worksheet.merge_range('H363:I364', self.gestion_char_4, texto)
			worksheet.merge_range('H365:I366', self.gestion_char_5, texto)
			worksheet.merge_range('L354:M358', "{}".format(self.gestion_text_1 if self.gestion_text_1 else ""), texto)
			worksheet.merge_range('L359:M359', "{}".format(self.gestion_text_2 if self.gestion_text_2 else ""), texto)
			worksheet.merge_range('L360:M362', "{}".format(self.gestion_text_3 if self.gestion_text_3 else ""), texto)
			worksheet.merge_range('L363:M364', "{}".format(self.gestion_text_4 if self.gestion_text_4 else ""), texto)
			worksheet.merge_range('L365:M366', "{}".format(self.gestion_text_5 if self.gestion_text_5 else ""), texto)
			if self.gestion_bol_1 == "SI":
				worksheet.merge_range('J354:J358', 'X', texto)
				worksheet.merge_range('K354:K358', '', texto)
			elif self.gestion_bol_1 == "NO":
				worksheet.merge_range('J354:J358', '', texto)
				worksheet.merge_range('K354:K358', 'X', texto)
			else:
				worksheet.merge_range('J354:J358', '', texto)
				worksheet.merge_range('K354:K358', '', texto)

			if self.gestion_bol_2 == "SI":
				worksheet.write('J359', 'X', texto)
				worksheet.write('K359', '', texto)
			elif self.gestion_bol_2 == "NO":
				worksheet.write('J359', '', texto)
				worksheet.write('K359', 'X', texto)
			else:
				worksheet.write('J359', '', texto)
				worksheet.write('K359', '', texto)

			if self.gestion_bol_3 == "SI":
				worksheet.merge_range('J360:J362', 'X', texto)
				worksheet.merge_range('K360:K362', '', texto)
			elif self.gestion_bol_3 == "NO":
				worksheet.merge_range('J360:J362', '', texto)
				worksheet.merge_range('K360:K362', 'X', texto)
			else:
				worksheet.merge_range('J360:J362', '', texto)
				worksheet.merge_range('K360:K362', '', texto)

			if self.gestion_bol_4 == "SI":
				worksheet.merge_range('J363:J364', 'X', texto)
				worksheet.merge_range('K363:K364', '', texto)
			elif self.gestion_bol_4 == "NO":
				worksheet.merge_range('J363:J364', '', texto)
				worksheet.merge_range('K363:K364', 'X', texto)
			else:
				worksheet.merge_range('J363:J364', '', texto)
				worksheet.merge_range('K363:K364', '', texto)

			if self.gestion_bol_5 == "SI":
				worksheet.merge_range('J365:J366', 'X', texto)
				worksheet.merge_range('K365:K366', '', texto)
			elif self.gestion_bol_5 == "NO":
				worksheet.merge_range('J365:J366', '', texto)
				worksheet.merge_range('K365:K366', 'X', texto)
			else:
				worksheet.merge_range('J365:J366', '', texto)
				worksheet.merge_range('K365:K366', '', texto)

			worksheet.merge_range('A367:M367', u"VII. Control de información y documentos", titulo)
			worksheet.merge_range('A368:B410', u"Documentos", titulo)
			worksheet.merge_range('C368:G370', u"La empresa, entidad pública o privada establece y mantiene información en medios apropiados para describir los componentes del sistema de gestión y su relación entre ellos.", texto)
			worksheet.merge_range('C371:G372', u"Los procedimientos de la empresa, entidad pública o privada, en la gestión de la seguridad y salud en el trabajo, se revisan periódicamente.", texto)
			worksheet.merge_range('C373:G383', u"El empleador establece y mantiene disposiciones y procedimientos para:\n- Recibir, documentar y responder adecuadamente a las comunicaciones internas y externas relativas a la seguridad y salud en el trabajo\n- Garantizar la comunicación interna de la información relativa a la seguridad y salud en el trabajo entre los distintos niveles y cargos de la organización.\n- Garantizar que las sugerencias de los trabajadores o de sus representantes sobre seguridad y salud en el trabajo se reciban y atiendan en forma oportuna y adecuada.", texto)
			worksheet.merge_range('C384:G387', u"El empleador entrega adjunto a los contratos de trabajo las recomendaciones de seguridad y salud considerando los riesgos del centro de labores y los relacionados con el puesto o función del trabajador.", texto)
			worksheet.merge_range('C388:G400', u"El empleador ha:\n- Facilitado al trabajador una copia del reglamento interno de seguridad y salud en el trabajo.\n- Capacitado al trabajador en referencia al contenido del reglamento interno de seguridad.\n- Asegurado poner en práctica las medidas de seguridad y salud en el trabajo\n- Elaborado un mapa de riesgos del centro de trabajo y lo exhibe en un lugar visible.\n- El empleador entrega al trabajador las recomendaciones de seguridad y salud en el trabajo considerando los riesgos del centro de labores y los relacionados con el puesto o función, el primer día de labores.", texto)
			worksheet.merge_range('C401:G410', u"El empleador mantiene procedimientos para garantizan que:\n- Se identifiquen, evalúen e incorporen en las especificaciones relativas a compras y arrendamiento financiero, disposiciones relativas al cumplimiento por parte de la organización de los requisitos de seguridad y salud.\n- Se identifiquen las obligaciones y los requisitos tanto legales como de la propia organización en materia de seguridad y salud en el trabajo antes de la adquisición de bienes y servicios\n- Se adopten disposiciones para que se cumplan dichos requisitos antes de utilizar los bienes y servicios mencionados", texto)
			worksheet.merge_range('H368:I370', self.documentos_char_1, texto)
			worksheet.merge_range('H371:I372', self.documentos_char_2, texto)
			worksheet.merge_range('H373:I383', self.documentos_char_3, texto)
			worksheet.merge_range('H384:I387', self.documentos_char_4, texto)
			worksheet.merge_range('H388:I400', self.documentos_char_5, texto)
			worksheet.merge_range('H401:I410', self.documentos_char_6, texto)
			worksheet.merge_range('L368:M370', "{}".format(self.documentos_text_1 if self.documentos_text_1 else ""), texto)
			worksheet.merge_range('L371:M372', "{}".format(self.documentos_text_2 if self.documentos_text_2 else ""), texto)
			worksheet.merge_range('L373:M383', "{}".format(self.documentos_text_3 if self.documentos_text_3 else ""), texto)
			worksheet.merge_range('L384:M387', "{}".format(self.documentos_text_4 if self.documentos_text_4 else ""), texto)
			worksheet.merge_range('L388:M400', "{}".format(self.documentos_text_5 if self.documentos_text_5 else ""), texto)
			worksheet.merge_range('L401:M410', "{}".format(self.documentos_text_6 if self.documentos_text_6 else ""), texto)
			if self.documentos_bol_1 == "SI":
				worksheet.merge_range('J368:J370', 'X', texto)
				worksheet.merge_range('K368:K370', '', texto)
			elif self.documentos_bol_1 == "NO":
				worksheet.merge_range('J368:J370', '', texto)
				worksheet.merge_range('K368:K370', 'X', texto)
			else:
				worksheet.merge_range('J368:J370', '', texto)
				worksheet.merge_range('K368:K370', '', texto)

			if self.documentos_bol_2 == "SI":
				worksheet.merge_range('J371:J372', 'X', texto)
				worksheet.merge_range('K371:K372', '', texto)
			elif self.documentos_bol_2 == "NO":
				worksheet.merge_range('J371:J372', '', texto)
				worksheet.merge_range('K371:K372', 'X', texto)
			else:
				worksheet.merge_range('J371:J372', '', texto)
				worksheet.merge_range('K371:K372', '', texto)

			if self.documentos_bol_3 == "SI":
				worksheet.merge_range('J373:J383', 'X', texto)
				worksheet.merge_range('K373:K383', '', texto)
			elif self.documentos_bol_3 == "NO":
				worksheet.merge_range('J373:J383', '', texto)
				worksheet.merge_range('K373:K383', 'X', texto)
			else:
				worksheet.merge_range('J373:J383', '', texto)
				worksheet.merge_range('K373:K383', '', texto)

			if self.documentos_bol_4 == "SI":
				worksheet.merge_range('J384:J387', 'X', texto)
				worksheet.merge_range('K384:K387', '', texto)
			elif self.documentos_bol_4 == "NO":
				worksheet.merge_range('J384:J387', '', texto)
				worksheet.merge_range('K384:K387', 'X', texto)
			else:
				worksheet.merge_range('J384:J387', '', texto)
				worksheet.merge_range('K384:K387', '', texto)

			if self.documentos_bol_5 == "SI":
				worksheet.merge_range('J388:J400', 'X', texto)
				worksheet.merge_range('K388:K400', '', texto)
			elif self.documentos_bol_5 == "NO":
				worksheet.merge_range('J388:J400', '', texto)
				worksheet.merge_range('K388:K400', 'X', texto)
			else:
				worksheet.merge_range('J388:J400', '', texto)
				worksheet.merge_range('K388:K400', '', texto)

			if self.documentos_bol_6 == "SI":
				worksheet.merge_range('J401:J410', 'X', texto)
				worksheet.merge_range('K401:K410', '', texto)
			elif self.documentos_bol_6 == "NO":
				worksheet.merge_range('J401:J410', '', texto)
				worksheet.merge_range('K401:K410', 'X', texto)
			else:
				worksheet.merge_range('J401:J410', '', texto)
				worksheet.merge_range('K401:K410', '', texto)

			worksheet.merge_range('A411:B418', u"Control de la documentación y de los datos", titulo)
			worksheet.merge_range('C411:G412', u"La empresa, entidad pública o privada establece procedimientos para el control de los documentos que se generen por esta lista de verificación.", texto)
			worksheet.merge_range('C413:G418', u"Este control asegura que los documentos y datos:\n- Puedan ser fácilmente localizados.\n- Puedan ser analizados y verificados periódicamente.\n- Están disponibles en los locales.\n- Sean removidos cuando los datos sean obsoletos.\n- Sean adecuadamente archivados.", texto)
			worksheet.merge_range('H411:I412', self.datos_char_1, texto)
			worksheet.merge_range('H413:I418', self.datos_char_2, texto)
			worksheet.merge_range('L411:M412', "{}".format(self.datos_text_1 if self.datos_text_1 else ""), texto)
			worksheet.merge_range('L413:M418', "{}".format(self.datos_text_2 if self.datos_text_2 else ""), texto)
			if self.datos_bol_1 == "SI":
				worksheet.merge_range('J411:J412', 'X', texto)
				worksheet.merge_range('K411:K412', '', texto)
			elif self.datos_bol_1 == "NO":
				worksheet.merge_range('J411:J412', '', texto)
				worksheet.merge_range('K411:K412', 'X', texto)
			else:
				worksheet.merge_range('J411:J412', '', texto)
				worksheet.merge_range('K411:K412', '', texto)

			if self.datos_bol_2 == "SI":
				worksheet.merge_range('J413:J418', 'X', texto)
				worksheet.merge_range('K413:K418', '', texto)
			elif self.datos_bol_2 == "NO":
				worksheet.merge_range('J413:J418', '', texto)
				worksheet.merge_range('K413:K418', 'X', texto)
			else:
				worksheet.merge_range('J413:J418', '', texto)
				worksheet.merge_range('K413:K418', '', texto)


			worksheet.merge_range('A419:B446', u"Gestión de los registros", titulo)
			worksheet.merge_range('C419:G423', u"El empleador ha implementado registros y documentos del sistema de gestión actualizados y a disposición del trabajador referido a:\n- Registro de accidentes de trabajo, enfermedades ocupacionales, incidentes peligrosos y otros incidentes, en el que deben constar la investigación y las medidas correctivas.", texto)
			worksheet.merge_range('C424:G424', u"Registro de exámenes médicos ocupacionales.", texto)
			worksheet.merge_range('C425:G426', u"Registro del monitoreo de agentes físicos, químicos, biológicos, psicosociales y factores de riesgo disergonómicos.", texto)
			worksheet.merge_range('C427:G428', u"Registro de inspecciones internas de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C429:G429', u"Registro de estadísticas de seguridad y salud.", texto)
			worksheet.merge_range('C430:G430', u"Registro de equipos de seguridad o emergencia.", texto)
			worksheet.merge_range('C431:G432', u"Registro de inducción, capacitación, entrenamiento y simulacros de emergencia.", texto)
			worksheet.merge_range('C433:G433', u"Registro de auditorías.", texto)
			worksheet.merge_range('C434:G442', u"La empresa, entidad pública o privada cuenta con registro de accidente de trabajo y enfermedad ocupacional e incidentes peligrosos y otros incidentes ocurridos a:\n- Sus trabajadores.\n- Trabajadores de intermediación laboral y/o tercerización.\n- Beneficiarios bajo modalidades formativas.\n- Personal que presta servicios de manera independiente, desarrollando sus actividades total o parcialmente en las instalaciones de la empresa, entidad pública o privada.", texto)
			worksheet.merge_range('C443:G446', u"Los registros mencionados son:\n- Legibles e identificables.\n- Permite su seguimiento.\n- Son archivados y adecuadamente protegidos.", texto)
			worksheet.merge_range('H419:I423', self.registros_char_1, texto)
			worksheet.merge_range('H424:I424', self.registros_char_2, texto)
			worksheet.merge_range('H425:I426', self.registros_char_3, texto)
			worksheet.merge_range('H427:I428', self.registros_char_4, texto)
			worksheet.merge_range('H429:I429', self.registros_char_5, texto)
			worksheet.merge_range('H430:I430', self.registros_char_6, texto)
			worksheet.merge_range('H431:I432', self.registros_char_7, texto)
			worksheet.merge_range('H433:I433', self.registros_char_8, texto)
			worksheet.merge_range('H434:I442', self.registros_char_9, texto)
			worksheet.merge_range('H443:I446', self.registros_char_10, texto)
			worksheet.merge_range('L419:M423', "{}".format(self.registros_text_1 if self.registros_text_1 else ""), texto)
			worksheet.merge_range('L424:M424', "{}".format(self.registros_text_2 if self.registros_text_2 else ""), texto)
			worksheet.merge_range('L425:M426', "{}".format(self.registros_text_3 if self.registros_text_3 else ""), texto)
			worksheet.merge_range('L427:M428', "{}".format(self.registros_text_4 if self.registros_text_4 else ""), texto)
			worksheet.merge_range('L429:M429', "{}".format(self.registros_text_5 if self.registros_text_5 else ""), texto)
			worksheet.merge_range('L430:M430', "{}".format(self.registros_text_6 if self.registros_text_6 else ""), texto)
			worksheet.merge_range('L431:M432', "{}".format(self.registros_text_7 if self.registros_text_7 else ""), texto)
			worksheet.merge_range('L433:M433', "{}".format(self.registros_text_8 if self.registros_text_8 else ""), texto)
			worksheet.merge_range('L434:M442', "{}".format(self.registros_text_9 if self.registros_text_9 else ""), texto)
			worksheet.merge_range('L443:M446', "{}".format(self.registros_text_10 if self.registros_text_10 else ""), texto)
			if self.registros_bol_1 == "SI":
				worksheet.merge_range('J419:J423', 'X', texto)
				worksheet.merge_range('K419:K423', '', texto)
			elif self.registros_bol_1 == "NO":
				worksheet.merge_range('J419:J423', '', texto)
				worksheet.merge_range('K419:K423', 'X', texto)
			else:
				worksheet.merge_range('J419:J423', '', texto)
				worksheet.merge_range('K419:K423', '', texto)

			if self.registros_bol_2 == "SI":
				worksheet.merge_range('J424:J424', 'X', texto)
				worksheet.merge_range('K424:K424', '', texto)
			elif self.registros_bol_2 == "NO":
				worksheet.merge_range('J424:J424', '', texto)
				worksheet.merge_range('K424:K424', 'X', texto)
			else:
				worksheet.merge_range('J424:J424', '', texto)
				worksheet.merge_range('K424:K424', '', texto)

			if self.registros_bol_3 == "SI":
				worksheet.merge_range('J425:J426', 'X', texto)
				worksheet.merge_range('K425:K426', '', texto)
			elif self.registros_bol_3 == "NO":
				worksheet.merge_range('J425:J426', '', texto)
				worksheet.merge_range('K425:K426', 'X', texto)
			else:
				worksheet.merge_range('J425:J426', '', texto)
				worksheet.merge_range('K425:K426', '', texto)

			if self.registros_bol_4 == "SI":
				worksheet.merge_range('J427:J428', 'X', texto)
				worksheet.merge_range('K427:K428', '', texto)
			elif self.registros_bol_4 == "NO":
				worksheet.merge_range('J427:J428', '', texto)
				worksheet.merge_range('K427:K428', 'X', texto)
			else:
				worksheet.merge_range('J427:J428', '', texto)
				worksheet.merge_range('K427:K428', '', texto)

			if self.registros_bol_5 == "SI":
				worksheet.write('J429', 'X', texto)
				worksheet.write('K429', '', texto)
			elif self.registros_bol_5 == "NO":
				worksheet.write('J429', '', texto)
				worksheet.write('K429', 'X', texto)
			else:
				worksheet.write('J429', '', texto)
				worksheet.write('K429', '', texto)

			if self.registros_bol_6 == "SI":
				worksheet.write('J430', 'X', texto)
				worksheet.write('K430', '', texto)
			elif self.registros_bol_6 == "NO":
				worksheet.write('J430', '', texto)
				worksheet.write('K430', 'X', texto)
			else:
				worksheet.write('J430', '', texto)
				worksheet.write('K430', '', texto)

			if self.registros_bol_7 == "SI":
				worksheet.merge_range('J431:J432', 'X', texto)
				worksheet.merge_range('K431:K432', '', texto)
			elif self.registros_bol_7 == "NO":
				worksheet.merge_range('J431:J432', '', texto)
				worksheet.merge_range('K431:K432', 'X', texto)
			else:
				worksheet.merge_range('J431:J432', '', texto)
				worksheet.merge_range('K431:K432', '', texto)

			if self.registros_bol_8 == "SI":
				worksheet.merge_range('J433:J433', 'X', texto)
				worksheet.merge_range('K433:K433', '', texto)
			elif self.registros_bol_8 == "NO":
				worksheet.merge_range('J433:J433', '', texto)
				worksheet.merge_range('K433:K433', 'X', texto)
			else:
				worksheet.merge_range('J433:J433', '', texto)
				worksheet.merge_range('K433:K433', '', texto)

			if self.registros_bol_9 == "SI":
				worksheet.merge_range('J434:J442', 'X', texto)
				worksheet.merge_range('K434:K442', '', texto)
			elif self.registros_bol_9 == "NO":
				worksheet.merge_range('J434:J442', '', texto)
				worksheet.merge_range('K434:K442', 'X', texto)
			else:
				worksheet.merge_range('J434:J442', '', texto)
				worksheet.merge_range('K434:K442', '', texto)

			if self.registros_bol_10 == "SI":
				worksheet.merge_range('J443:J446', 'X', texto)
				worksheet.merge_range('K443:K446', '', texto)
			elif self.registros_bol_10 == "NO":
				worksheet.merge_range('J443:J446', '', texto)
				worksheet.merge_range('K443:K446', 'X', texto)
			else:
				worksheet.merge_range('J443:J446', '', texto)
				worksheet.merge_range('K443:K446', '', texto)

			worksheet.merge_range('A447:M447', u"VIII. Revisión por la dirección", titulo)
			worksheet.merge_range('A448:B496', u"Gestión de la mejora continua", titulo)
			worksheet.merge_range('C448:G450', u"La alta dirección:\n- Revisa y analiza periódicamente el sistema de gestión para asegurar que es apropiada y efectiva.", texto)
			worksheet.merge_range('C451:G470', u"Las disposiciones adoptadas por la dirección para la mejora continua del sistema de gestión de la seguridad y salud en el trabajo, deben tener en cuenta:\n- Los objetivos de la seguridad y salud en el trabajo de la empresa, entidad pública o privada.\n- Los resultados de la identificación de los peligros y evaluación de los riesgos.\n- Los resultados de la supervisión y medición de la eficiencia.\n- La investigación de accidentes, enfermedades ocupacionales, incidentes peligrosos y otros incidentes relacionados con el trabajo.\n- Los resultados y recomendaciones de las auditorías y evaluaciones realizadas por la dirección de la empresa, entidad pública o privada.\n- Las recomendaciones del Comité de seguridad y salud, o del Supervisor de seguridad y salud.\n- Los cambios en las normas.\n- La información pertinente nueva.\n- Los resultados de los programas anuales de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C471:G477', u"La metodología de mejoramiento continuo considera:\n- La identificación de las desviaciones de las prácticas y condiciones aceptadas como seguras.\n- El establecimiento de estándares de seguridad.\n- La medición y evaluación periódica del desempeño con respecto a los estándares de la empresa, entidad pública o privada.\n- La corrección y reconocimiento del desempeño.", texto)
			worksheet.merge_range('C478:G481', u"La investigación y auditorías permiten a la dirección de la empresa, entidad pública o privada lograr los fines previstos y determinar, de ser el caso, cambios en la política y objetivos del sistema de gestión de seguridad y salud en el trabajo.", texto)
			worksheet.merge_range('C482:G487', u"La investigación de los accidentes, enfermedades ocupacionales, incidentes peligrosos y otros incidentes, permite identificar:\n- Las causas inmediatas (actos y condiciones subestándares),\n- Las causas básicas (factores personales y factores del trabajo)\n- Deficiencia del sistema de gestión de la seguridad y salud en el trabajo, para la planificación de la acción correctiva pertinente.", texto)
			worksheet.merge_range('C488:G496', u"El empleador ha modificado las medidas de prevención de riesgos laborales cuando resulten inadecuadas e insuficientes para garantizar la seguridad y salud de los trabajadores incluyendo al personal de los regímenes de intermediación y tercerización, modalidad formativa e incluso a los que prestan servicios de manera independiente, siempre que éstos desarrollen sus actividades total o parcialmente en las instalaciones de la empresa, entidad pública o privada durante el desarrollo de las operaciones.", texto)
			worksheet.merge_range('H448:I450', self.mejora_char_1, texto)
			worksheet.merge_range('H451:I470', self.mejora_char_2, texto)
			worksheet.merge_range('H471:I477', self.mejora_char_3, texto)
			worksheet.merge_range('H478:I481', self.mejora_char_4, texto)
			worksheet.merge_range('H482:I487', self.mejora_char_5, texto)
			worksheet.merge_range('H488:I496', self.mejora_char_6, texto)
			worksheet.merge_range('L448:M450', "{}".format(self.mejora_text_1 if self.mejora_text_1 else ""), texto)
			worksheet.merge_range('L451:M470', "{}".format(self.mejora_text_2 if self.mejora_text_2 else ""), texto)
			worksheet.merge_range('L471:M477', "{}".format(self.mejora_text_3 if self.mejora_text_3 else ""), texto)
			worksheet.merge_range('L478:M481', "{}".format(self.mejora_text_4 if self.mejora_text_4 else ""), texto)
			worksheet.merge_range('L482:M487', "{}".format(self.mejora_text_5 if self.mejora_text_5 else ""), texto)
			worksheet.merge_range('L488:M496', "{}".format(self.mejora_text_6 if self.mejora_text_6 else ""), texto)
			if self.mejora_bol_1 == "SI":
				worksheet.merge_range('J448:J450', 'X', texto)
				worksheet.merge_range('K448:K450', '', texto)
			elif self.mejora_bol_1 == "NO":
				worksheet.merge_range('J448:J450', '', texto)
				worksheet.merge_range('K448:K450', 'X', texto)
			else:
				worksheet.merge_range('J448:J450', '', texto)
				worksheet.merge_range('K448:K450', '', texto)

			if self.mejora_bol_2 == "SI":
				worksheet.merge_range('J451:J470', 'X', texto)
				worksheet.merge_range('K451:K470', '', texto)
			elif self.mejora_bol_2 == "NO":
				worksheet.merge_range('J451:J470', '', texto)
				worksheet.merge_range('K451:K470', 'X', texto)
			else:
				worksheet.merge_range('J451:J470', '', texto)
				worksheet.merge_range('K451:K470', '', texto)

			if self.mejora_bol_3 == "SI":
				worksheet.merge_range('J471:J477', 'X', texto)
				worksheet.merge_range('K471:K477', '', texto)
			elif self.mejora_bol_3 == "NO":
				worksheet.merge_range('J471:J477', '', texto)
				worksheet.merge_range('K471:K477', 'X', texto)
			else:
				worksheet.merge_range('J471:J477', '', texto)
				worksheet.merge_range('K471:K477', '', texto)

			if self.mejora_bol_4 == "SI":
				worksheet.merge_range('J478:J481', 'X', texto)
				worksheet.merge_range('K478:K481', '', texto)
			elif self.mejora_bol_4 == "NO":
				worksheet.merge_range('J478:J481', '', texto)
				worksheet.merge_range('K478:K481', 'X', texto)
			else:
				worksheet.merge_range('J478:J481', '', texto)
				worksheet.merge_range('K478:K481', '', texto)

			if self.mejora_bol_5 == "SI":
				worksheet.merge_range('J482:J487', 'X', texto)
				worksheet.merge_range('K482:K487', '', texto)
			elif self.mejora_bol_5 == "NO":
				worksheet.merge_range('J482:J487', '', texto)
				worksheet.merge_range('K482:K487', 'X', texto)
			else:
				worksheet.merge_range('J482:J487', '', texto)
				worksheet.merge_range('K482:K487', '', texto)

			if self.mejora_bol_6 == "SI":
				worksheet.merge_range('J488:J496', 'X', texto)
				worksheet.merge_range('K488:K496', '', texto)
			elif self.mejora_bol_6 == "NO":
				worksheet.merge_range('J488:J496', '', texto)
				worksheet.merge_range('K488:K496', 'X', texto)
			else:
				worksheet.merge_range('J488:J496', '', texto)
				worksheet.merge_range('K488:K496', '', texto)
			k = 496
			for o in self.otros_ids:
				worksheet.merge_range(k,2,k+1,6, u"{}".format(o.otros_indicador if o.otros_indicador else ""), texto)
				worksheet.merge_range(k,7,k+1,8, u"{}".format(o.otros_fuente if o.otros_fuente else ""), texto)
				worksheet.merge_range(k,11,k+1,12, u"{}".format(o.otros_observacion if o.otros_observacion else ""), texto)
				if o.otros_cumplimiento == "SI":
					worksheet.merge_range(k,9,k+1,9, 'X', texto)
					worksheet.merge_range(k,10,k+1,10, '', texto)
				elif o.otros_cumplimiento == "NO":
					worksheet.merge_range(k,9,k+1,9, '', texto)
					worksheet.merge_range(k,10,k+1,10, 'X', texto)
				else:
					worksheet.merge_range(k,9,k+1,9, '', texto)
					worksheet.merge_range(k,10,k+1,10, '', texto)
				k += 2
			if self.otros_ids:
				worksheet.merge_range(496,0,k-1,1, u"Otros", titulo)

			workbook.close()

			f = open('/odoopreventor/custom/excel.xlsx', 'rb')
			# f = open('C:\\Program Files (x86)\\Odoo 13.0\\server\\addons\\excel.xlsx', 'rb')
			file_name = io.BytesIO(f.read())
			# workbook.save(file_name)
			self.write({
				'txt_excel_cal': u'ListadeVerificacion.xlsx',
				'txt_binary_excel_cal': base64.encodestring(file_name.getvalue())
			})

	@api.model
	def create(self, vals):
		if vals.get('name', _('Borrador')) == _('Borrador'):
			vals['name'] = self.env['ir.sequence'].next_by_code(
				'lista.verificacion') or _('Borrador')
		res = super(Sgsst, self).create(vals)
		return res

class SgssTransient(models.TransientModel):
	_name = 'lista.transient'

	def guardar_linea(self,linea_id,field,value):
		lineaedit = self.env["lista.verificacion"].search([('id','=',linea_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

class OtrosLineamiento(models.Model):
	_name = 'lista.otros'

	otros_id = fields.Many2one("lista.verificacion", string=u"Lista de verificación")
	otros_indicador = fields.Char('Indicador')
	otros_fuente = fields.Char('Fuente')
	otros_cumplimiento = fields.Char('Cumplimiento')
	otros_observacion = fields.Text('Observacion')



class OtrosTransient(models.TransientModel):
	_name = 'otros.transient'

	def guardar_linea(self,otros_id,field,value):
		lineaedit = self.env["lista.otros"].search([('id','=',otros_id)],limit=1)
		lineaedit.write({'{}'.format(field):value})
		return True

	def limites_permisos(self,plan_id):
		permiso_line = self.env["lista.verificacion"].search([('create_uid', '=',  self.env.user.id)])
		plan = self.env["planes.planes"].sudo().search([('id',  '=', plan_id)])
		if len(permiso_line) < plan.limite_registro:
			return True
		else:
			return False
