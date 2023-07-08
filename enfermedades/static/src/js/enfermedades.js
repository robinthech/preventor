odoo.define("enfermedades.enfermedades", function(require) {
  'use strict';
  console.log('enfermedades')
  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb


  publicWidget.registry.SectionEnfermedades = publicWidget.Widget.extend({
    selector: ".section_enfermedades",
    events: {
      'change .linea_datos': 'change_linea_datos',
      'change .linea_accidente': 'change_linea_accidente',
      'change .linea_medida': 'change_linea_medida',
      'change .linea_relacion': 'change_linea_relacion',
      'change .linea_enfermedad': 'change_linea_enfermedad',
      'change .linea_responsable': 'change_linea_responsable',
      'change .linea_datos_otros': 'change_linea_datos_otros',
      'click .guardar-formulario': 'guardar_formulario',
      'click .nuevo-lista-otros': 'nuevo_lista_otros',
      'click .nueva_medida':'nueva_medida',
      'click .nueva_relacion':'nueva_relacion',
      'click .agregar_datos':'agregar_datos',
      'click .nuevo_responsable':'nuevo_responsable',
      'click .nuevo_responsable_configuracion':'nuevo_responsable_configuracion',
      'change .tipo_peligro': 'tipo_peligro',

    },
    tipo_peligro: async function(ev) {
      var evento = $(ev.currentTarget)
      var id = evento.find("option:selected").val()
      var evaluacion_id = evento.parents(".enfermedad_id").data("enfermedad_id")
      console.log('tipo_peligro')
      rpc.query({
        route: "/enfermedades/configuracion",
        params: {
          name: id,
        }
      }).then(function(res) {
        $('#descripcion-' + evaluacion_id).empty()
        res.forEach(element => {
          $('#descripcion-' + evaluacion_id).append(`<option value=${element.id}>${element.name}</option>`);
        });

        rpc.query({
          model: 'datos.enfermedad.transient',
          method: 'guardar_linea',
          args: [1, evaluacion_id, "agente", res[0].id]
        })

      })
      // var id_f = parseInt(id)
      // console.log(id_f)
      // rpc.query({
      //   model: 'evaluacion.iper.transient',
      //   method: 'guardar_linea',
      //   args: [1, evaluacion_id, "type_id", id_f]
      // })


    },

    change_linea_accidente: async function(ev) {
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      var opcion = evento.val()
      var radioname = evento.attr("name")
      if (radioname == "sexo" || radioname == "turno"){
        opcion = evento.find("option:selected").val()
      }
      if(radioname == "fecha_accidente"){
        opcion = opcion.substr(0,10)+' '+opcion.substr(11,15)
      }
      console.log(opcion)
      await rpc.query({
        model: 'registro.enfermedades.transient',
        method: 'guardar_linea',
        args: [1, accidente_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });

    },
    change_linea_enfermedad: async function(ev) {
      var evento = $(ev.currentTarget)
      var enfermedad_id = evento.parents('.enfermedad_id').data("enfermedad_id")
      var opcion = evento.val()
      var radioname = evento.attr("name")
      if (["enero_p","febrero_p","marzo_p","abril_p","mayo_p","junio_p","julio_p","agosto_p","septiembre_p","octubre_p","noviembre_p","diciembre_p"].includes(radioname)){
        if(evento.is(':checked')){
          opcion = true
        }else{
          opcion = false
        }
      }
      await rpc.query({
        model: 'datos.enfermedad.transient',
        method: 'guardar_linea',
        args: [1, enfermedad_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });
    },
    change_linea_relacion: async function(ev) {
      console.log('linea_relacion')
      var evento = $(ev.currentTarget)
      var relacion_id = evento.parents('.relacion_id').data("relacion_id")
      var opcion = evento.val()
      var radioname = evento.attr("name")
      if (radioname == "monitoreo"){
        if(evento.is(':checked')){
          opcion = true
        }else{
          opcion = false
        }
      }
      console.log(radioname)
      console.log(opcion)
      console.log(relacion_id)
      await rpc.query({
        model: 'relacion.sustancias.transient',
        method: 'guardar_linea',
        args: [1, relacion_id, radioname, opcion]
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
        model: 'enfermedades.responsable.final.transient',
        method: 'guardar_linea',
        args: [1, accidente_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });

    },
    change_linea_medida: async function(ev) {
      var evento = $(ev.currentTarget)
      var medida_id = evento.parents('.medida_id').data("medida_id")
      var opcion = evento.val()
      var radioname = evento.attr("name")
      if (radioname == "estado"){
        opcion = evento.find("option:selected").val()
        if (opcion == "P"){
          evento.removeClass("bg-success bg-warning").addClass("bg-danger")
        }else if(opcion == "R"){
          evento.removeClass("bg-danger bg-warning").addClass("bg-success")
        }else if(opcion == "E"){
          evento.removeClass("bg-danger bg-success").addClass("bg-warning")
        }
      }
      await rpc.query({
        model: 'medida.enfermedades.transient',
        method: 'guardar_linea',
        args: [1, medida_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });
    },
    nueva_medida: function(ev){
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      rpc.query({
        model: 'medida.enfermedades',
        method: 'create',
        args: [{
          "accidente_id": accidente_id,
          "name": "Medida nueva"
        }],
      }).then(function() {
        location.reload();
      });
    },
    nueva_relacion: function(ev){
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      rpc.query({
        model: 'relacion.sustancias',
        method: 'create',
        args: [{
          "relacion_id": accidente_id,
          "name": "Relacion de sustancias"
        }],
      }).then(function() {
        location.reload();
      });
    },
    agregar_datos: function(ev){
      var evento = $(ev.currentTarget)
      var enfermedad_id = evento.data("enfermedad_id")
      console.log('agregar_datos')
      console.log(enfermedad_id)
      rpc.query({
        model: 'datos.enfermedad',
        method: 'create',
        args: [{
          "enfermedad_id": enfermedad_id,
          "name":"Nueva enfermedad"
        }],
      }).then(function() {
        location.reload();
      });
    },
    nuevo_responsable: function(ev){
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      rpc.query({
        model: 'enfermedades.responsable',
        method: 'create',
        args: [{
          "responsable_id": accidente_id,
          "name": "Nuevo responsable"
        }],
      }).then(function() {
        location.reload();
      });
    },
    nuevo_responsable_configuracion: function(ev){
      var evento = $(ev.currentTarget)
      var name = $(this.$el).find("input[name='new-responsable-name']").val()
      console.log(name)
      rpc.query({
        model: 'enfermedades.responsable',
        method: 'create',
        args: [{
          "name": name
        }],
      }).then(function() {
        location.reload();
      });
    },
    nuevo_lista_otros: function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.parents('.lista_id').data("lista_id")
      var indicador = $(this.$el).find("input[name='new-lista-indicador']").val()
      var fuente = $(this.$el).find("input[name='new-lista-fuente']").val()
      var otros_id = evento.data("lista_id")
      rpc.query({
        model: 'lista.otros',
        method: 'create',
        args: [{
          "otros_id": otros_id,
          "otros_indicador": indicador,
          "otros_fuente": fuente
        }],
      }).then(function() {
        location.reload();
      });

      rpc.query({
        model: 'lista.verificacion',
        method: 'file_excel',
        args: [lista_id],
      }).then(function() {
        location.reload();
      });
    },
    change_linea_datos_otros: async function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.parents('.lista_id').data("lista_id")
      var otros_id = evento.parents('tr').data("otros_id")
      var opcion = evento.find('textarea').val()
      var radioname = evento.find('textarea').attr("name")
      // console.log(evento)
      // console.log(radioname)
      // console.log(opcion)
      await rpc.query({
        model: 'otros.transient',
        method: 'guardar_linea',
        args: [1, otros_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });

      await rpc.query({
        model: 'lista.verificacion',
        method: 'file_excel',
        args: [lista_id],
      }).then(function() {
        // location.reload();
      });

    },
  })

  publicWidget.registry.CrearEnfermedades = publicWidget.Widget.extend({
    selector: ".registro-incidente",
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
        model: "enfermedades.ocupacionales",
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
