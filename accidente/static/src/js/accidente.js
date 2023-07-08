odoo.define("accidente.lista", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb


  publicWidget.registry.SectionAccidente = publicWidget.Widget.extend({
    selector: ".section_accidente",
    events: {
      'change .linea_datos': 'change_linea_datos',
      'change .linea_accidente': 'change_linea_accidente',
      'change .linea_medida': 'change_linea_medida',
      'change .linea_responsable': 'change_linea_responsable',
      'change .linea_datos_otros': 'change_linea_datos_otros',
      'click .guardar-formulario': 'guardar_formulario',
      'click .actualizar-excel': 'actualiza_excel',
      'click .nuevo-lista-otros': 'nuevo_lista_otros',
      'click .nueva_medida':'nueva_medida',
      'click .nuevo_responsable_configuracion':'nuevo_responsable_configuracion',
      'change input#upload': 'click_guardar_archivo',
			'click .nuevo-supervisor': 'click_nuevo_supervisor',
			'click .botton-eliminar-supervisor': 'action_eliminar_supervisor',

    },
    init:function(){
      this._super.apply(this,arguments)
      this.attachments =[]
    },
		click_nuevo_supervisor: function(ev) {
			var evento = $(ev.currentTarget)
			var responsable = evento.parents(".supervisor").find(".name option:selected").val();
			var fechainicial = evento.parents(".supervisor").find("input[name='new-supervisor-fecha']").val()
			var iperc_id = evento.data("iperc_id")
			rpc.query({
				model: 'accidente.responsable.final',
				method: 'create',
				args: [{
					"responsable": responsable,
					"responsable_id": iperc_id
				}],
			}).then(function() {
				location.reload()
			});
		},
    click_guardar_archivo:function(ev){
        console.log('atachemnt')
        var self = this;
        var files = ev.target.files;
        var accidente_id = $("input#upload").data("accidente_id");
        var icono;

        for (let file of files){
          let reader = new FileReader();
          reader.onload = async function () {
              console.log(reader.result);
              var b64 = reader.result.replace(/^data:.+;base64,/, '');
              var att  = {
                  res_id: accidente_id,
                  res_model: 'registro.accidente.final',
                  name: file.name,
                  datas: b64,
                  mimetype: file.type,
                  type: 'binary',
              }
              self.attachments.push(att)
              let attachment_files  = $("div#attachment_files")
              if(file.type == "application/pdf"){
                icono = "<span><i class='fa fa-file-pdf-o'></i></span>"
              }else if(file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"){
                icono = "<span><i class='fa fa-file-word-o'></i></span>"
              }else if(file.type == "image/jpeg"){
                icono = "<span><i class='fa fa-picture-o'></i></span>"
              }else if(file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"){
                icono = "<span><i class='fa fa-file-excel-o'></i></span>"
              }
              await rpc.query({
                  model: 'ir.attachment',
                  method: 'create',
                  args: [att],
              }).then(function(id){
                attachment_files.append(`${icono}<a href="/web/content/${id}?download=true"> ${file.name} - </a>`)
              });

          };
          reader.readAsDataURL(file)
        }
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
        model: 'registro.accidente.transient',
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
        model: 'accidente.responsable.final.transient',
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
        model: 'medida.correctiva.transient',
        method: 'guardar_linea',
        args: [1, medida_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });
    },
    actualiza_excel: function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.parents('.lista_id').data("lista_id")
      // console.log(lista_id)
      rpc.query({
        model: 'lista.verificacion',
        method: 'file_excel',
        args: [lista_id],
      }).then(function() {
        location.reload();
      });
    },
    nueva_medida: function(ev){
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      rpc.query({
        model: 'medida.correctiva',
        method: 'create',
        args: [{
          "accidente_id": accidente_id,
          "name": "Medida nueva"
        }],
      }).then(function() {
        location.reload();
      });
    },
    nuevo_responsable: function(ev){
      var evento = $(ev.currentTarget)
      var accidente_id = evento.parents('.accidente_id').data("accidente_id")
      rpc.query({
        model: 'accidente.responsable.final',
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
        model: 'accidente.responsable',
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
		action_eliminar_supervisor: function(ev) {
			var evento = $(ev.currentTarget)
			var responsable_id = $(ev.target).data("responsable_id")
			rpc.query({
				model: "accidente.responsable.final",
				method: "unlink",
				args: [responsable_id],
			}).then(function(res) {
				location.reload();
			});
		},
  })

  publicWidget.registry.CrearAccidente = publicWidget.Widget.extend({
    selector: ".registro-accidente",
    jsLibs: [
      '/website_permiso/static/src/lib/notify.js',
    ],
    events: {
      'click .nuevo-registro-accidente': 'click_nueva_accidente',
      'click .actualizar-excel': 'actualiza_excel',
      'click .botton-eliminar-verificacion': 'action_eliminar_verificacion',
      'click .file-gratis': 'file_gratis',
    },
    click_nueva_accidente: function(ev) {
      var razon = $(this.$el).find("input[name='new-accidente-razon']").val()
      var ruc = $(this.$el).find("input[name='new-accidente-ruc']").val()

      rpc.query({
        model: 'registro.accidente.final',
        method: 'create',
        args: [{
          "razon": razon,
          "ruc": ruc
        }],
      }).then(function() {
        location.reload();
      });


    },
    actualiza_excel: function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.closest('.actualizar-excel').data("verificacion_id")
      // console.log(lista_id)
      rpc.query({
        model: 'lista.verificacion',
        method: 'file_excel',
        args: [lista_id],
      }).then(function() {
        location.reload();

      });
    },
    action_eliminar_verificacion: function(ev) {
      var lista_id = $(ev.target).data("verificacion_id");
      rpc.query({
        model: "registro.accidente.final",
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
