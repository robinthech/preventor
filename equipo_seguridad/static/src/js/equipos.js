odoo.define("equipo_seguridad.lista", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb


  publicWidget.registry.SectionEquipos = publicWidget.Widget.extend({
    selector: ".section_equipos",
    events: {
      'change .linea_datos': 'change_linea_datos',
      'change .linea_accidente': 'change_linea_accidente',
      'change .linea_medida': 'change_linea_medida',
      'change .linea_relacion': 'change_linea_relacion',
      'change .linea_enfermedad': 'change_linea_enfermedad',
      'change .linea_trabajador': 'change_linea_trabajador',
      'change .linea_responsable': 'change_linea_responsable',
      'change .change_linea_accidente': 'change_linea_accidente',
      'mouseup .linea_firma': 'change_linea_firma',
      'change .linea_datos_otros': 'change_linea_datos_otros',
      'change .equipo-emergencia': 'change_equipo_emergencia',
      'change .equipo-proteccion': 'change_equipo_proteccion',
      'change .change_trabajador_id': 'change_trabajador_id',
      'click .guardar-formulario': 'guardar_formulario',
      'click .nuevo-lista-otros': 'nuevo_lista_otros',
      'click .nueva_medida':'nueva_medida',
      'click .nueva_relacion':'nueva_relacion',
      'click .agregar_datos':'agregar_datos',
      'click .nuevo_responsable':'nuevo_responsable',
      'click .nuevo-equipo-emergencia':'nuevo_equipo_emergencia',
      'click .nuevo-equipo-proteccion':'nuevo_equipo_proteccion',
    },
    init:function(){
      this._super.apply(this,arguments)
      this.signature =[]
      var self = this;
      $(document).ready(function() {
          var canvas = document.getElementsByClassName("firma");
          canvas.width = $(".col-4").width();
          canvas.height = $(".col-4").height();
        });


      var canvas = document.querySelector("canvas");

          // var image = signaturePad.toDataURL("data:image/png;base64,")
      this.signaturePad = new SignaturePad(canvas);

    },
    change_linea_firma: function(ev){
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      var image = this.signaturePad.toDataURL("image/png")
      console.log('change_linea_firma')
      console.log(image)
      rpc.query({
        model: 'equipos.seguridad.transient',
        method: 'guardar_linea',
        args: [1, accidente_id, "firma", image]
      }).then(function() {
        // location.reload();
      });
    },
    change_trabajador_id: function(ev){
      var evento = $(ev.currentTarget)
      var trabajador_id = evento.val()
      var input_dni = evento.closest('tr').find("input[name='dni']")
      rpc.query({
        model: 'equipo.trabajadores.trabajadores',
        method: 'search_read',
        fields: ['id','name','dni'],
        domain: [['id', '=', trabajador_id]],
      }).then(function(res) {
        input_dni.val(res[0].dni)
      });
    },
    agregar_datos: function(ev){
      var evento = $(ev.currentTarget)
      var enfermedad_id = evento.data("enfermedad_id")
      var fecha_default = new Date().toISOString().split('T')[0]
      rpc.query({
        model: 'equipo.trabajadores.trabajadores',
        method: 'search_read',
        fields: ['id'],
      }).then(function(res) {
        rpc.query({
          model: 'equipo.trabajadores',
          method: 'create',
          args: [{
            "equipo_id": res[0].id,
            "trabajador_id": enfermedad_id,
            "fecha_entrega":fecha_default,
            "fecha_renovacion":fecha_default,
          }],
        }).then(function() {
          location.reload();
        });
      })
    },
    change_linea_accidente: async function(ev) {
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      var opcion = evento.val()
      var radioname = evento.attr("name")
      await rpc.query({
        model: 'equipos.seguridad.transient',
        method: 'guardar_linea',
        args: [1, accidente_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });
    },
    change_linea_trabajador: async function(ev) {
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.trabajador_id').data("trabajador_id")
      var opcion = evento.val()
      var radioname = evento.attr("name")
      await rpc.query({
        model: 'equipo.trabajadores.transient',
        method: 'guardar_linea',
        args: [1, accidente_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });
    },
    change_linea_responsable: async function(ev) {
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.responsable_id').data("responsable_id")
      var opcion = evento.val()
      var radioname = evento.attr("name")
      await rpc.query({
        model: 'seguridad.responsable.transient',
        method: 'guardar_linea',
        args: [1, accidente_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });
    },
    change_equipo_emergencia: async function(ev) {
      console.log('change_equipo_emergencia')
      var evento = $(ev.currentTarget)
      var accidente_id = evento.data("linea_id")
      var opcion = evento.val()
      var radioname = evento.attr("name")
      console.log(opcion)
      console.log(radioname)
      if(evento.is(':checked')){
        opcion = true
      }else{
        opcion = false
      }
      await rpc.query({
        model: 'equipo.emergencia.transient',
        method: 'guardar_linea',
        args: [1, accidente_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });
    },
    change_equipo_proteccion: async function(ev) {
      var evento = $(ev.currentTarget)
      var accidente_id = evento.data("linea_id")
      var opcion = evento.val()
      var radioname = evento.attr("name")
      console.log(opcion)
      console.log(radioname)
      if(evento.is(':checked')){
        opcion = true
      }else{
        opcion = false
      }
      await rpc.query({
        model: 'equipo.proteccion.transient',
        method: 'guardar_linea',
        args: [1, accidente_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });
    },

    nuevo_equipo_proteccion: function(ev){
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      var name = $(this.$el).find("input[name='new-equipo-proteccion']").val()
      rpc.query({
        model: 'equipo.proteccion',
        method: 'create',
        args: [{
          "equipo_id": accidente_id,
          "name": name
        }],
      }).then(function() {
        location.reload();
      });
    },
    nuevo_equipo_emergencia: function(ev){
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      var name = $(this.$el).find("input[name='new-equipo-emergencia']").val()
      rpc.query({
        model: 'equipo.emergencia',
        method: 'create',
        args: [{
          "emergencia_id": accidente_id,
          "name": name
        }],
      }).then(function() {
        location.reload();
      });
    },
    nuevo_responsable: function(ev){
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      rpc.query({
        model: 'seguridad.responsable',
        method: 'create',
        args: [{
          "responsable_id": accidente_id,
          "name": "Nuevo responsable"
        }],
      }).then(function() {
        location.reload();
      });
    },

  })

  publicWidget.registry.CrearEquipos = publicWidget.Widget.extend({
    selector: ".registro-equipos",
    jsLibs: [
      '/website_permiso/static/src/lib/notify.js',
    ],
    events: {
      'click .nuevo-registro-incidente': 'click_nueva_accidente',
      'click .botton-eliminar-verificacion': 'action_eliminar_verificacion',
      'click .file-gratis': 'file_gratis',
    },
    click_nueva_accidente: function(ev) {
      var razon = $(this.$el).find("input[name='new-accidente-razon']").val()
      var ruc = $(this.$el).find("input[name='new-accidente-ruc']").val()

      rpc.query({
        model: 'equipos.seguridad',
        method: 'create',
        args: [{
          "razon": razon,
          "ruc": ruc
        }],
      }).then(function() {
        location.reload();
      });


    },
    action_eliminar_verificacion: function(ev) {
      var lista_id = $(ev.target).data("verificacion_id");
      // for each equipo.trabajadores cuyo trabajador_id es igual a lista_id
      rpc.query({
        model: "equipo.trabajadores",
        method: "search",
        args: [[['trabajador_id', '=', lista_id]]],
      }).then(function(res) {
        for (let elemento in res){
          rpc.query({
            model: "equipo.trabajadores",
            method: "unlink",
            args: [res[elemento]]
          }).then(function(res) {
          });
        }
      }).finally(function(){
          rpc.query({
            model: "equipos.seguridad",
            method: "unlink",
            args: [lista_id]
          }).then(function(res) {
            location.reload();
          });
      })
    },
  })

  publicWidget.registry.SectionConfiguracion = publicWidget.Widget.extend({
    selector: ".registro-configuracion",
    events: {
      'click .nuevo_responsable_configuracion':'nuevo_responsable_configuracion',
      'click .botton-eliminar-trabajador':'action_eliminar_trabajador',
      'click .guardar_trabajador': 'guardar_trabajador',
    },

    guardar_trabajador: function(ev){
      var evento = $(ev.currentTarget)
      var trabajador_id = evento.data("trabajador_id")
      var name = evento.closest(".modal-content").find("input[name='new-responsable-name']").val()
      var dni = evento.closest(".modal-content").find("input[name='new-responsable-dni']").val()
      rpc.query({
        model: 'equipo.trabajadores.trabajadores',
        method: 'write',
        args: [
          [trabajador_id], {
            "name": name,
            "dni": dni
          }
        ],
      }).then(function() {
        location.reload();
      });
    },

    nuevo_responsable_configuracion: function(ev){
      var evento = $(ev.currentTarget)
      var name = evento.closest(".modal-content").find("input[name='new-responsable-name']").val()
      var dni = evento.closest(".modal-content").find("input[name='new-responsable-dni']").val()
      rpc.query({
        model: 'equipo.trabajadores.trabajadores',
        method: 'create',
        args: [{
          "name": name,
          "dni": dni
        }],
      }).then(function() {
        location.reload();
      });
    },

    action_eliminar_trabajador: function(ev) {
      var evento = $(ev.currentTarget)
      var trabajador_id = evento.parents('.eliminar_trabajador_id').data("trabajador_id")
      // for each equipo.trabajadores cuyo trabajador_id es igual a lista_id
      console.log(trabajador_id)
      rpc.query({
        model: "equipo.trabajadores.trabajadores",
        method: 'search_read',
        fields: ['id','trabajador_id'],
        domain: [['id', '=', trabajador_id]],
      }).then(function(res) {
        var array = res[0].trabajador_id
        for (let elemento in array){
          rpc.query({
            model: "equipo.trabajadores",
            method: "unlink",
            args: [array[elemento]]
          }).then(function(res) {
          });
        }
      }).finally(function(){
          rpc.query({
            model: "equipo.trabajadores.trabajadores",
            method: "unlink",
            args: [trabajador_id]
          }).then(function(res) {
            location.reload();
          });
      })
    },

    click_nueva_accidente: function(ev) {
      var razon = $(this.$el).find("input[name='new-accidente-razon']").val()
      var ruc = $(this.$el).find("input[name='new-accidente-ruc']").val()

      rpc.query({
        model: 'enfermedades.ocupacionales',
        method: 'create',
        args: [{
          "razon": razon,
          "ruc": ruc
        }],
      }).then(function() {
        location.reload();
      });


    },
    action_eliminar_verificacion: function(ev) {
      var lista_id = $(ev.target).data("verificacion_id");
      rpc.query({
        model: "lista.verificacion",
        method: "unlink",
        args: [lista_id]
      }).then(function(res) {
        location.reload();
      });
    },
    file_gratis: function(ev) {
      swal({
        title: "Lista de verificacion",
        text: "No puede descargar más archivos excel con el plan Gratis.",
        icon: "info",
      });
    },
  })
})
