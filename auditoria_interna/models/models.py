# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class Sede(models.Model):
    _name = 'sede.sede'

    name = fields.Char(u'Sede')
    active = fields.Boolean(u'Activo')


# class Usuario(models.Model):
#     _inherit = 'res.users'

#     sede_id = fields.Many2one('sede.sede', string=u'Sede')

class Auditoria(models.Model):
    _name = 'auditoria.interna'

    name = fields.Char("N° Auditoria", index=True,default=lambda self: _('Borrador'))
    cliente = fields.Char(u"Razon Social")
    ruc = fields.Char(u"RUC")
    domicilio = fields.Char(u"Domicilio")
    actividad = fields.Char(u"Actividad Economica")
    trabajadores = fields.Integer(u"Nº de Trabajadores")
    n_conformidad = fields.Integer(u"# No Conformidades",default="0")
    attachment = fields.Binary(string=u'attachment', attachment=True)
    descripcionnoconformidad = fields.Text(u"Descripcion")
    causasdenoconformidad = fields.Text(u"Causas")
    informacion = fields.Text(u"Información")
    auditor_ids = fields.One2many("auditor.auditor", "auditoria_id", string="Auditores")
    registro_ids = fields.One2many("registro.auditoria", "auditoria_id", string="Auditorias")
    no_conformidad_ids = fields.One2many("no.conformidad", "auditoria_id", string="No Conformiades")
    responsable = fields.Char(u"Responsable")
    cargo = fields.Char(u"Cargo")
    fecha = fields.Datetime(u"Fecha")
    Firma = fields.Binary(string=u'Firma', attachment=True)


    @api.model
    def create(self, vals):
        if vals.get('name', _('Borrador')) == _('Borrador'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'auditoria.interna') or _('Borrador')
        res = super(Auditoria, self).create(vals)
        return res

class AuditoriaTransient(models.TransientModel):
    _name = 'auditoriainterna.transient'

    def guardar_linea(self,linea_id,field,value):
        lineaedit = self.env["auditoria.interna"].search([('id','=',linea_id)],limit=1)
        lineaedit.write({'{}'.format(field):value})
        return True

class Auditor(models.Model):
    _name = 'auditor.auditor'

    name = fields.Char(u"Nombre del Auditor")
    registro = fields.Char(u"N° de Registro")
    auditoria_id = fields.Many2one("auditoria.interna", string="Auditoria")

class AuditorTransient(models.TransientModel):
    _name = 'auditor.transient'

    def guardar_linea(self,linea_id,field,value):
        lineaedit = self.env["auditor.auditor"].search([('id','=',linea_id)],limit=1)
        lineaedit.write({'{}'.format(field):value})
        return True

class RegistroAuditoria(models.Model):
    _name = 'registro.auditoria'

    name = fields.Char(u"Procesos Auditados")
    responsables = fields.Char(u"Nombre de los Responsables")
    fecha = fields.Datetime(u"Fecha de Auditoria")
    auditoria_id = fields.Many2one("auditoria.interna", string="Auditoria")


class RegistroTransient(models.TransientModel):
    _name = 'registro.transient'

    def guardar_linea(self,linea_id,field,value):
        lineaedit = self.env["registro.auditoria"].search([('id','=',linea_id)],limit=1)
        lineaedit.write({'{}'.format(field):value})
        return True

class NoConfomidad(models.Model):
    _name = 'no.conformidad'

    medida_correctiva = fields.Char(u"Medida Correctiva")
    responsable = fields.Char(u"Responsable")
    fecha_ejecucion = fields.Date(u"FechaEjecucion")
    fecha_termino = fields.Date(u"FechaTermino")
    estado = fields.Selection(selection=[('1', 'Pendiente'), ('2', 'En Ejecución'), ('3', 'Realizado')], string='Estado', default="1")
    auditoria_id = fields.Many2one("auditoria.interna", string="Auditoria")



class NoConfomidadTransient(models.TransientModel):
    _name = 'noconfomidad.transient'

    def guardar_linea(self,linea_id,field,value):
        lineaedit = self.env["no.conformidad"].search([('id','=',linea_id)],limit=1)
        lineaedit.write({'{}'.format(field):value})
        return True
