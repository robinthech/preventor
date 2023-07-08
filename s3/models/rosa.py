# -*- coding: utf-8 -*-
from odoo import models, fields, api,  _

tabla_1 = [[2,	2,	3,	4,	5,	6,	7,	8],
           [2,	2,	3,	4,	5,	6,	7,	8],
           [3,	3,	3,	4,	5,	6,	7,	8],
           [4,	4,	4,	4,	5,	6,	7,	8],
           [5,	5,	5,	5,	5,	7,	8,	9],
           [6,	6,	6,	7,	7,	8,	8,	9],
           [7,	7,	7,	8,	8,	9,	9,	9]]
tabla_2 = [[1,	1,	1,	2,	3,	4,	5,	6],
           [1,	1,	2,	2,	3,	4,	5,	6],
           [1,	2,	2,	3,	3,	4,	6,	7],
           [2,	2,	3,	3,	4,	5,	6,	8],
           [3,	3,	4,	4,	5,	6,	7,	8],
           [4,	4,	5,	5,	6,	7,	8,	9],
           [5,	5,	6,	7,	8,	8,	9,	9]]
tabla_3 = [[1,	1,	1,	2,	3,	4,	5,	6],
           [1,	1,	2,	3,	4,	5,	6,	7],
           [1,	2,	2,	3,	4,	5,	6,	7],
           [2,	3,	3,	3,	5,	6,	7,	8],
           [3,	4,	4,	5,	5,	6,	7,	8],
           [4,	5,	5,	6,	6,	7,	8,	9],
           [5,	6,	6,	7,	7,	8,	8,	9],
           [6,	7,	7,	8,	8,	9,	9,	9]]
tabla_4 = [[1,	2,	3,	4,	5,	6,	7,	8,	9],
           [2,	2,	3,	4,	5,	6,	7,	8,	9],
           [3,	3,	3,	4,	5,	6,	7,	8,	9],
           [4,	4,	4,	4,	5,	6,	7,	8,	9],
           [5,	5,	5,	5,	5,	6,	7,	8,	9],
           [6,	6,	6,	6,	6,	6,	7,	8,	9],
           [7,	7,	7,	7,	7,	7,	7,	8,	9],
           [8,	8,	8,	8,	8,	8,	8,	8,	9],
           [9,	9,	9,	9,	9,	9,	9,	9,	9]]
tabla_final = [[1,	2,	3,	4,	5,	6,	7,	8,	9,	10],
               [2,	2,	3,	4,	5,	6,	7,	8,	9,	10],
               [3,	3,	3,	4,	5,	6,	7,	8,	9,	10],
               [4,	4,	4,	4,	5,	6,	7,	8,	9,	10],
               [5,	5,	5,	5,	5,	6,	7,	8,	9,	10],
               [6,	6,	6,	6,	6,	6,	7,	8,	9,	10],
               [7,	7,	7,	7,	7,	7,	7,	8,	9,	10],
               [8,	8,	8,	8,	8,	8,	8,	8,	9,	10],
               [9,	9,	9,	9,	9,	9,	9,	9,	9,	10],
               [10, 10,	10,	10,	10,	10,	10,	10,	10,	10]]


class ProductProduct(models.Model):
    _inherit = "registro.monitoreo"

    rosa_ids = fields.One2many('rosa.rosa', 'registro_id', string=u'ROSA')
    puntos_rosa = fields.Integer(compute="_compute_puntos_rosa", string=u"ROSA")

    @api.depends("rosa_ids")
    def _compute_puntos_rosa(self):
        for record in self:
            record.puntos_rosa = len(record.rosa_ids)


class Rosa(models.Model):
    _name = 'rosa.rosa'
    _inherits = {'riesgo.disergonomico': 'riesgo_disergonomico_id'}

    riesgo_disergonomico_id = fields.Many2one('riesgo.disergonomico', required=True, ondelete='restrict',
                                              auto_join=True, string='Riesgo Disergonomico')

    sede_id = fields.Many2one('sede.sede', string=u'Sede')
    # sillas
    silla_puntuacion = fields.Integer(compute="_compute_silla_tabla", string="SILLA", store=True)

    # altura-longitud
    altura_longitud_puntuacion = fields.Integer(compute="_compute_silla",
                                                string="Altura del asiento más la pronfudidad",
                                                store=True)
    # respaldo-reposabrazos
    respaldo_reposabrazos_puntuacion = fields.Integer(compute="_compute_silla",
                                                      string="Respaldo del asiento más el reposabrazos",
                                                      store=True)

    # sillas-altura
    silla_altura_puntuacion = fields.Integer(compute="_compute_puntuacion_silla_altura",
                                             string="Altura del asiento",
                                             store=True)
    silla_altura_igual = fields.Boolean("A° es igual a 90 °",default=True)
    silla_altura_menor = fields.Boolean("Silla muy baja Rodillas A° < 90°",default=False)
    silla_altura_mayor = fields.Boolean("Silla muy alta Rodillas A°> 90°",default=False)
    silla_altura_sin_contacto = fields.Boolean("Sin contacto con el suelo")
    silla_altura_no_ajustable = fields.Boolean("Altura del asiento no ajustable")
    silla_altura_sin_espacio = fields.Boolean("Sin suficiente espacio bajo la mesa. Imposibilidad de cruzar las piernas")

    # silla-longitud
    silla_longitud_puntuacion = fields.Integer(compute="_compute_puntuacion_silla_longitud",
                                               string="Longitud del asiento",
                                               store=True)
    silla_longitud_igual = fields.Boolean("'d' = 08 cm de espacio",default=True)
    silla_longitud_menor = fields.Boolean("'d' es menor a 08 cm de espacio",default=False)
    silla_longitud_mayor = fields.Boolean("'d' es mayor a 08 cm de espacio",default=False)
    silla_longitud_no_ajustable = fields.Boolean("Profundidad no es ajustable Ajuste (+ 1)")

    # silla-respaldo
    silla_respaldo_puntuacion = fields.Integer(compute="_compute_puntuacion_silla_respaldo",
                                               string="Respaldo",
                                               store=True)
    silla_respaldo_recto = fields.Boolean("Respaldo Recto",default=True)
    silla_respaldo_plano = fields.Boolean("Respaldo Plano",default=False)
    silla_respaldo_obtuso = fields.Boolean("Respaldo Obtuso",default=False)
    silla_respaldo_agudo = fields.Boolean("Respaldo Agudo",default=False)
    silla_respaldo_ajustable = fields.Boolean("Respaldo no ajustable")
    silla_respaldo_mesa = fields.Boolean("Mesa de trabajo demasiado alta. Hombros encogidos")
    # silla-resposabrazos
    silla_reposabrazos_puntuacion = fields.Integer(compute="_compute_puntuacion_silla_reposabrazos",
                                                   string="Reposabrazos",
                                                   store=True)
    silla_reposabrazos_linea = fields.Boolean("Reposa brazos en linea con el hombro, relajado",default=True)
    silla_reposabrazos_alto = fields.Boolean("Reposa brazos muy alto o con poco soporte",default=False)
    silla_reposabrazos_dura = fields.Boolean("Superficie dura o dañada de reposabrazos")
    silla_reposabrazos_separados = fields.Boolean("Reposabrasos muy separados")
    silla_reposabrazos_ajustable = fields.Boolean("Separación entre reposabrazos no es ajustable")
    silla_reposabrazos_duracion = fields.Selection(selection=[("menor", "Menor a 1 hora por día o menor a 30 minutos ininterrumpidamente"),
                                                              ("entre", "Si se permanece entre 1 y 4 horas al día o entre 30 minutos y 1 hora seguida"),
                                                              ("mayor", "Si permanece más de 4 horas al día o más de una 1hora ininterrumpidamente")],
                                                   string="Duración de uso de Silla:",default="menor")

    # Monitor-Telefono
    monitor_telefono_puntuacion = fields.Integer(compute="_compute_monitor_telefono_tabla",
                                                 string="MONITOR MÁS TELÉFONO",
                                                 store=True)

    # Monitor
    monitor_puntuacion = fields.Integer(compute="_compute_puntuacion_monitor", string="MONITOR", store=True)
    monitor_ideal = fields.Boolean("Posición ideal",default=True)
    monitor_bajo = fields.Boolean("Monitor Bajo",default=False)
    monitor_alto = fields.Boolean("Monitor Alto",default=False)
    monitor_centrada = fields.Boolean("Existe pantalla no centrada. Cuello Girado")
    monitor_reflejos = fields.Boolean("Existen reflejos en la pantalla")
    monitor_documentos = fields.Boolean("No hay soporte para documentos y es necesario")
    monitor_alejado = fields.Boolean("Monitor esta muy alejado")
    monitor_duracion = fields.Selection(selection=[("menor", "Menor a 1 hora por día o menor a 30 minutos ininterrumpidamente"),
                                                   ("entre", "Si se permanece entre 1 y 4 horas al día o entre 30 minutos y 1 hora seguida"),
                                                   ("mayor", "Si permanece más de 4 horas al día o más de una 1hora ininterrumpidamente")],
                                        string="Duración de uso de Monitor:")

    # Telefono
    telefono_puntuacion = fields.Integer(compute="_compute_puntuacion_telefono", string="TELÉFONO", store=True)
    telefono_manos = fields.Boolean("Teléfono una mano o manos",default=True)
    telefono_alejado = fields.Boolean("Teléfono muy alejado",default=False)
    telefono_cuello = fields.Boolean("Mantener cuello girado y hombro encogido")
    telefono_mano_libre = fields.Boolean("Sin opcion a manos libres")
    telefono_duracion = fields.Selection(selection=[("menor", "Menor a 1 hora por día o menor a 30 minutos ininterrumpidamente"),
                                                    ("entre", "Si se permanece entre 1 y 4 horas al día o entre 30 minutos y 1 hora seguida"),
                                                    ("mayor", "Si permanece más de 4 horas al día o más de una 1hora ininterrumpidamente")],
                                         string="Duración de uso de Telefonos:")

    # teclado + raton
    teclado_raton_puntuacion = fields.Integer(compute="_compute_teclado_raton_tabla", string="TECLADO MÁS RATÓN",
                                              store=True)

    # teclado
    teclado_puntuacion = fields.Integer(compute="_compute_puntuacion_teclado", string="TECLADO", store=True)
    teclado_munecas_rectas = fields.Boolean("Muñecas rectas, hombros relajados",default=True)
    teclado_munecas_extendidas = fields.Boolean("Muñecas extendidas > 15°",default=False)
    teclado_munecas_desviadas = fields.Boolean("Escribir en el teclado con las muñecas desviadas")
    teclado_alto = fields.Boolean("Teclado demasiado alto. Hombros encogidos.")
    teclado_alcanza = fields.Boolean("Alcanza objetos por encima de la cabeza, mandos, documentos, etc.")
    teclado_ajustable = fields.Boolean("Plataforma no ajustable")
    teclado_duracion = fields.Selection(selection=[("menor", "Menor a 1 hora por día o menor a 30 minutos ininterrumpidamente"),
                                                   ("entre", "Si se permanece entre 1 y 4 horas al día o entre 30 minutos y 1 hora seguida"),
                                                   ("mayor", "Si permanece más de 4 horas al día o más de una 1hora ininterrumpidamente")],
                                        string="Duración de uso de Teclado:", store=True)

    # raton
    raton_puntuacion = fields.Integer(compute="_compute_puntuacion_raton", string="RATÓN", store=True)
    raton_linea = fields.Boolean("Ratón en línea con el hombro", store=True,default=True)
    raton_lejos = fields.Boolean("Raton con brazo lejos del cuerpo", store=True,default=False)
    raton_diferentes = fields.Boolean("El teclado y el ratón se encuentran en diferentes superficies a distintas alturas", store=True)
    raton_estirar = fields.Boolean("Agarre en pinza del ratón, es pequeño o no permite estirar la mano.", store=True)
    raton_reposamos = fields.Boolean("Reposamanos delante del ratón, hace doblar la muñeca.", store=True)
    raton_duracion = fields.Selection(selection=[("menor", "Menor a 1 hora por día o menor a 30 minutos ininterrumpidamente"),
                                                 ("entre", "Si se permanece entre 1 y 4 horas al día o entre 30 minutos y 1 hora seguida"),
                                                 ("mayor", "Si permanece más de 4 horas al día o más de una 1hora ininterrumpidamente")],
                                      string="Duración de uso de Raton:", store=True)

    # resultados
    resultado_grupo_a = fields.Integer(compute="_compute_silla_tabla", string="RESULTADO GRUPO A", store=True)
    resultado_grupo_b = fields.Integer(compute="_compute_resultado_b", string="RESULTADO GRUPO B", store=True)
    resultado_final = fields.Integer(compute="_compute_resultado_final", string="PUNTAJE FINAL", store=True)
    nivel_riesgo = fields.Char(compute="_compute_resultado_rosa", string="NIVEL DE RIESGO ", store=True)
    situacion_trabajo = fields.Char(compute="_compute_resultado_rosa", string="Situación de trabajo ", store=True)
    cumple = fields.Char(compute="_compute_resultado_rosa", string="¿Cumple?", store=True)
    cont_si = fields.Integer("si")
    cont_no = fields.Integer("no")
    cont = fields.Integer(" ")

    # compute silla-altura

    @api.depends("silla_altura_igual", "silla_altura_menor", "silla_altura_mayor", "silla_altura_sin_contacto",
                 "silla_altura_no_ajustable", "silla_altura_sin_espacio")
    def _compute_puntuacion_silla_altura(self):
        for record in self:
            cont = 0
            if record.silla_altura_igual:
                cont = 1
            if record.silla_altura_menor:
                cont = 2
            if record.silla_altura_mayor:
                cont = 2
            if record.silla_altura_sin_contacto:
                cont = 3
            if record.silla_altura_no_ajustable:
                cont = cont + 1
            if record.silla_altura_sin_espacio:
                cont = cont + 1

            record.silla_altura_puntuacion = cont

    @api.depends("silla_longitud_igual", "silla_longitud_menor", "silla_longitud_mayor", "silla_longitud_no_ajustable")
    def _compute_puntuacion_silla_longitud(self):
        for record in self:
            cont = 0
            if record.silla_longitud_igual:
                cont = 1
            if record.silla_longitud_menor:
                cont = 2
            if record.silla_longitud_mayor:
                cont = 2
            if record.silla_longitud_no_ajustable:
                cont = cont + 1

            record.silla_longitud_puntuacion = cont

    # compute silla-respaldo

    @api.depends("silla_respaldo_recto", "silla_respaldo_plano", "silla_respaldo_obtuso", "silla_respaldo_agudo",
                 "silla_respaldo_ajustable", "silla_respaldo_mesa")
    def _compute_puntuacion_silla_respaldo(self):
        for record in self:
            cont = 0
            if record.silla_respaldo_recto:
                cont = 1
            if record.silla_respaldo_plano:
                cont = 2
            if record.silla_respaldo_obtuso:
                cont = 2
            if record.silla_respaldo_agudo:
                cont = 2
            if record.silla_respaldo_ajustable:
                cont = cont + 1
            if record.silla_respaldo_mesa:
                cont = cont + 1
            record.silla_respaldo_puntuacion = cont

    # compute silla-resposabrazos

    @api.depends("silla_reposabrazos_linea", "silla_reposabrazos_alto", "silla_reposabrazos_dura",
                 "silla_reposabrazos_separados", "silla_reposabrazos_ajustable")
    def _compute_puntuacion_silla_reposabrazos(self):
        for record in self:
            cont = 0
            if record.silla_reposabrazos_linea:
                cont = 1
            if record.silla_reposabrazos_alto:
                cont = 2
            if record.silla_reposabrazos_dura:
                cont = cont + 1
            if record.silla_reposabrazos_separados:
                cont = cont + 1
            # check this line
            if record.silla_reposabrazos_ajustable:
                cont = cont + 1

            record.silla_reposabrazos_puntuacion = cont

    # compute silla
    @api.depends("silla_altura_puntuacion", "silla_longitud_puntuacion", "silla_respaldo_puntuacion",
                 "silla_reposabrazos_puntuacion")
    def _compute_silla(self):
        for record in self:
            record.altura_longitud_puntuacion = record.silla_altura_puntuacion + record.silla_longitud_puntuacion
            record.respaldo_reposabrazos_puntuacion = record.silla_respaldo_puntuacion + record.silla_reposabrazos_puntuacion

    # compute Monitor

    @api.depends("monitor_ideal", "monitor_bajo", "monitor_alto", "monitor_centrada", "monitor_reflejos",
                 "monitor_documentos", "monitor_alejado", "monitor_duracion")
    def _compute_puntuacion_monitor(self):
        for record in self:
            cont = 0
            if record.monitor_ideal:
                cont = 1
            if record.monitor_bajo:
                cont = 2
            if record.monitor_alto:
                cont = 2
            if record.monitor_centrada:
                cont = cont + 1
            if record.monitor_reflejos:
                cont = cont + 1
            if record.monitor_documentos:
                cont = cont + 1
            if record.monitor_alejado:
                cont = cont + 1

            record.monitor_puntuacion = cont

            if record.monitor_duracion == 'menor':
                record.monitor_puntuacion = cont - 1
            if record.monitor_duracion == 'entre':
                record.monitor_puntuacion = cont
            if record.monitor_duracion == 'mayor':
                record.monitor_puntuacion = cont + 1

    # compute Telefono

    @api.depends("telefono_manos", "telefono_alejado", "telefono_cuello", "telefono_mano_libre", "telefono_duracion")
    def _compute_puntuacion_telefono(self):
        for record in self:
            cont = 0
            if record.telefono_manos:
                cont = 1
            if record.telefono_alejado:
                cont = 2
            if record.telefono_cuello:
                cont = cont + 2
            if record.telefono_mano_libre:
                cont = cont + 1

            record.telefono_puntuacion = cont

            if record.telefono_duracion == 'menor':
                record.telefono_puntuacion = cont - 1
            if record.telefono_duracion == 'entre':
                record.telefono_puntuacion = cont
            if record.telefono_duracion == 'mayor':
                record.telefono_puntuacion = cont + 1

    # compute teclado

    @api.depends("teclado_munecas_rectas", "teclado_munecas_extendidas", "teclado_munecas_desviadas", "teclado_alto",
                 "teclado_alcanza", "teclado_ajustable", "teclado_duracion")
    def _compute_puntuacion_teclado(self):
        for record in self:
            cont = 0
            if record.teclado_munecas_rectas:
                cont = 1
            if record.teclado_munecas_extendidas:
                cont = 2
            if record.teclado_munecas_desviadas:
                cont = cont + 1
            if record.teclado_alto:
                cont = cont + 1
            if record.teclado_alcanza:
                cont = cont + 1
            if record.teclado_ajustable:
                cont = cont + 1

            record.teclado_puntuacion = cont

            if record.teclado_duracion == 'menor':
                record.teclado_puntuacion = cont - 1
            if record.teclado_duracion == 'entre':
                record.teclado_puntuacion = cont
            if record.teclado_duracion == 'mayor':
                record.teclado_puntuacion = cont + 1

    # compute raton

    @api.depends("raton_linea", "raton_lejos", "raton_diferentes", "raton_estirar", "raton_reposamos",
                 "raton_duracion")
    def _compute_puntuacion_raton(self):
        for record in self:
            cont = 0

            if record.raton_linea:
                cont = 1
            if record.raton_lejos:
                cont = 2
            if record.raton_diferentes:
                cont = cont + 2
            if record.raton_estirar:
                cont = cont + 1
            if record.raton_reposamos:
                cont = cont + 1

            record.raton_puntuacion = cont

            if record.raton_duracion == 'menor':
                record.raton_puntuacion = cont - 1
            if record.raton_duracion == 'entre':
                record.raton_puntuacion = cont
            if record.raton_duracion == 'mayor':
                record.raton_puntuacion = cont + 1

    # compute silla utilizando la tabla
    @api.depends("altura_longitud_puntuacion", "respaldo_reposabrazos_puntuacion", "silla_reposabrazos_duracion")
    def _compute_silla_tabla(self):
        for record in self:
            record.silla_puntuacion = tabla_1[record.altura_longitud_puntuacion - 2][record.respaldo_reposabrazos_puntuacion - 2]
            if record.silla_reposabrazos_duracion == 'menor':
                record.silla_puntuacion = record.silla_puntuacion - 1
            if record.silla_reposabrazos_duracion == 'entre':
                record.silla_puntuacion = record.silla_puntuacion
            if record.silla_reposabrazos_duracion == 'mayor':
                record.silla_puntuacion = record.silla_puntuacion + 1

            record.resultado_grupo_a = record.silla_puntuacion

    # compute MONITOR MÁS TELÉFONO

    @api.depends("monitor_puntuacion", "telefono_puntuacion")
    def _compute_monitor_telefono_tabla(self):
        for record in self:
            record.monitor_telefono_puntuacion = tabla_2[record.telefono_puntuacion][record.monitor_puntuacion]

    # compute teclado + raton

    @api.depends("teclado_puntuacion", "raton_puntuacion")
    def _compute_teclado_raton_tabla(self):
        for record in self:
            record.teclado_raton_puntuacion = tabla_3[record.raton_puntuacion][record.teclado_puntuacion]

    # compute  MONITOR MÁS TELÉFONO --- teclado + raton

    @api.depends("monitor_telefono_puntuacion", "teclado_raton_puntuacion")
    def _compute_resultado_b(self):
        for record in self:
            record.resultado_grupo_b = tabla_4[record.teclado_raton_puntuacion-1][record.monitor_telefono_puntuacion-1]

    # compute  PUNTAJE FINAL
    @api.depends("resultado_grupo_a", "resultado_grupo_b")
    def _compute_resultado_final(self):
        for record in self:
            record.resultado_final = tabla_final[record.resultado_grupo_b - 1][record.resultado_grupo_a - 1]

    # compute  resultados
    @api.depends("resultado_final")
    def _compute_resultado_rosa(self):
        for record in self:
            if record.resultado_final == 1:
                record.nivel_riesgo = u'INAPRECIABLE'
                record.cumple = u"SÍ CUMPLE"
                record.situacion_trabajo = u'Situaciones de trabajo aceptables'
            elif record.resultado_final == 2:
                record.nivel_riesgo = u'INAPRECIABLE'
                record.cumple = u"SÍ CUMPLE"
                record.situacion_trabajo = u'Situaciones de trabajo aceptables'
            elif record.resultado_final == 3:
                record.nivel_riesgo = u'BAJO'
                record.cumple = u"SÍ CUMPLE"
                record.situacion_trabajo = u'Situaciones de trabajo aceptables'
            elif record.resultado_final == 4:
                record.nivel_riesgo = u'BAJO'
                record.cumple = u"SÍ CUMPLE"
                record.situacion_trabajo = u'Situaciones de trabajo aceptables'
            elif record.resultado_final == 5:
                record.nivel_riesgo = u'MEDIO'
                record.cumple = u"SÍ CUMPLE"
                record.situacion_trabajo = u'Situacion de tarea de prioridad  Medio de intervención ergonómica'
            elif record.resultado_final == 6:
                record.nivel_riesgo = u'MEDIO'
                record.cumple = u"SÍ CUMPLE"
                record.situacion_trabajo = u'Situacion de tarea de prioridad  Medio de intervención ergonómica'
            elif record.resultado_final == 7:
                record.nivel_riesgo = u'ALTO'
                record.cumple = u"NO CUMPLE"
                record.situacion_trabajo = u'Situacion de tarea de prioridad  Alto de intervención ergonómica'
            elif record.resultado_final == 8:
                record.nivel_riesgo = u'ALTO'
                record.cumple = u"NO CUMPLE"
                record.situacion_trabajo = u'Situacion de tarea de prioridad  Alto de intervención ergonómica'
            elif record.resultado_final == 9:
                record.nivel_riesgo = u'MUY ALTO'
                record.cumple = u"NO CUMPLE"
                record.situacion_trabajo = u'Situacion de tarea de prioridad  Muy alto de intervención ergonómica'
            elif record.resultado_final == 10:
                record.nivel_riesgo = u'MUY ALTO'
                record.cumple = u"NO CUMPLE"
                record.situacion_trabajo = u'Situacion de tarea de prioridad  Muy alto de intervención ergonómica'
            if record.cumple == "SÍ CUMPLE":
                record.cont_si = 1
            else:
                record.cont_no = 1
            record.cont = 1
