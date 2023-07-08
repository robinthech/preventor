odoo.define("lista_covid.lista_covid", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget");
  var rpc = require("web.rpc");
  var core = require('web.core');
  var QWeb = core.qweb;
  var _t = core._t;

  publicWidget.registry.CrearRegistroListaCovid = publicWidget.Widget.extend({
    selector: ".list-anexo-cuatro",
    events: {
      'click .botton-chequeo-vigilancia': 'click_nuevo_registro_vigilancia',
      'click .file-gratis': 'file_gratis',

    },
    file_gratis: function(ev) {
      swal({
        title: "ANEXO 4",
        text: "No puede descargar más archivos excel con el plan Gratis.",
        icon: "info",
      });
    },
    click_nuevo_registro_vigilancia: function(ev) {
      var fecha = $(this.$el).find("input[name='new-registro-fecha']").val()
      var razon = $(this.$el).find("input[name='new-registro-empresa']").val()
      var ruc = $(this.$el).find("input[name='new-registro-ruc']").val()
      var empresa = $(".list-anexo-cuatro").data("empresa_id");
      var plan_id = $('#modulo-anexo-cuatro').data("plan_id");

      rpc.query({
        model: 'edit.linea.covid',
        method: 'limites_permisos',
        args: [1,plan_id],
      }).then(function(output) {
        console.log(output);
        if (output) {
          rpc.query({
            model: 'covid.anexo',
            method: 'create',
            args: [{
              "fecha": fecha,
              "empresa": razon,
              "empresa_id": empresa,
              "ruc": ruc,
            }],
          }).then(function() {
            location.reload();

          });
        }
        else {
          swal({
              title: "ANEXO 4",
              text: "No puede crear más Chequeo DE vigilancia.",
              icon: "info",
            });
        }

      });

    },
  })


  publicWidget.registry.EditLineaChequeoVigilancia = publicWidget.Widget.extend({
    selector: ".change-linea-anexo",
    events: {
      'change .linea-field-name': 'click_name_registro_accidente',
      'click .linea-field-cumplimiento': 'click_cumplimiento_registro_accidente',
      'change .linea-field-detalles': 'click_detalles_registro_accidente',
    },
    click_name_registro_accidente: function(ev) {
      var registro_id = $(".form-lista-covid").data("registro_id");
      var linea_id = $(ev.target).data("linea_id");
      var valor = $(ev.target).val();
      rpc.query({
        model: 'covid.anexo.lista',
        method: 'write',
        args: [[linea_id],{ "name":valor}],
      }).then(function(output) {
         rpc.query({
          model:'covid.anexo',
          method:'file_excel',
          args:[registro_id],
        }).then(function(){
          // location.reload();
        });
      });

    },
    click_cumplimiento_registro_accidente: function(ev) {
      var registro_id = $(".form-lista-covid").data("registro_id");
      var linea_id = $(ev.target).data("linea_id");
      var valor = $(ev.target).is(":checked");
      console.log(valor)
      console.log(typeof(valor))
      rpc.query({
        model: 'covid.anexo.lista',
        method: 'write',
        args: [[linea_id],{ "cumplimiento":valor}],
      }).then(function(output) {
        rpc.query({
          model: 'covid.anexo',
          method: 'fuction_compute_puntaje',
          args: [registro_id],
        }).then(function(salida) {
            $("input[name='puntaje']").val(salida);

        });
         rpc.query({
          model:'covid.anexo',
          method:'file_excel',
          args:[registro_id],
        }).then(function(){
          // location.reload();
        });
      });

    },
    click_detalles_registro_accidente: function(ev) {
      var registro_id = $(".form-lista-covid").data("registro_id");
      var linea_id = $(ev.target).data("linea_id");
      var valor = $(ev.target).val();
      rpc.query({
        model: 'covid.anexo.lista',
        method: 'write',
        args: [[linea_id],{ "detalles":valor}],
      }).then(function(output) {
      rpc.query({
          model:'covid.anexo',
          method:'file_excel',
          args:[registro_id],
        }).then(function(){
          // location.reload();
        });
      });

    },
  })

  publicWidget.registry.EditSubLineaChequeoVigilancia = publicWidget.Widget.extend({
    selector: ".change-sublista-anexo",
    events: {
      'change .linea-field-name': 'click_name_registro_accidente',
      'click .linea-field-cumplimiento': 'click_cumplimiento_registro_accidente',
      'change .linea-field-detalles': 'click_detalles_registro_accidente',
    },
    click_name_registro_accidente: function(ev) {
      var registro_id = $(".form-lista-covid").data("registro_id");
      var linea_id = $(ev.target).data("linea_id");
      var valor = $(ev.target).val();
      rpc.query({
        model: 'covid.anexo.sublista',
        method: 'write',
        args: [[linea_id],{ "name":valor}],
      }).then(function(output) {
         rpc.query({
          model:'covid.anexo',
          method:'file_excel',
          args:[registro_id],
        }).then(function(){
          // location.reload();
        });
      });

    },
    click_cumplimiento_registro_accidente: function(ev) {
      var registro_id = $(".form-lista-covid").data("registro_id");
      var linea_id = $(ev.target).data("linea_id");
      var valor = $(ev.target).is(":checked");
      console.log(valor)
      console.log(typeof(valor))
      rpc.query({
        model: 'covid.anexo.sublista',
        method: 'write',
        args: [[linea_id],{ "cumplimiento":valor}],
      }).then(function(output) {
        rpc.query({
          model: 'covid.anexo',
          method: 'fuction_compute_puntaje',
          args: [registro_id],
        }).then(function(salida) {
          $("input[name='puntaje']").val(salida);
        });
         rpc.query({
          model:'covid.anexo',
          method:'file_excel',
          args:[registro_id],
        }).then(function(){
          // location.reload();
        });
      });

    },
    click_detalles_registro_accidente: function(ev) {
      var registro_id = $(".form-lista-covid").data("registro_id");
      var linea_id = $(ev.target).data("linea_id");
      var valor = $(ev.target).val();
      rpc.query({
        model: 'covid.anexo.sublista',
        method: 'write',
        args: [[linea_id],{ "detalles":valor}],
      }).then(function(output) {
         rpc.query({
          model:'covid.anexo',
          method:'file_excel',
          args:[registro_id],
        }).then(function(){
          // location.reload();
        });
      });

    },
  })

  publicWidget.registry.NuevoChequeVigilancia = publicWidget.Widget.extend({
    selector: ".form-lista-covid",
    events: {
      'click .botton-elemento-vigilancia': 'click_edit_registro_accidente',
      'change .registro-empresa': 'click_registro_empresa',
      'change .registro-evaluado': 'click_registro_evaluado',
      'change .registro-fecha-evaluacion': 'click_registro_evaluacion',
      'click .nuevo-objetivo-especifico': 'click_nuevo_elemento',
    },
    click_edit_registro_accidente: function(ev) {
      var registro_id = $(".form-lista-covid").data("registro_id");
      var name = $(this.$el).find("input[name='new-registro-name']").val()
      var cumplimiento = $(this.$el).find("input[name='new-registro-cumplimiento']").val()
      var detalles = $(this.$el).find("input[name='new-registro-detalles']").val()
      rpc.query({
        model: 'covid.anexo.lista',
        method: 'create',
        args: [{"name" :name,"cumplimiento":cumplimiento,"detalles":detalles,"covid_id":registro_id}],
      }).then(function(output) {
          location.reload();
      });

    },

    click_registro_empresa: function(ev) {
      var registro_id = $(".form-lista-covid").data("registro_id");
      var valor = $(ev.target).val();
      rpc.query({
        model: 'covid.anexo',
        method: 'write',
        args: [[registro_id],{ "empresa":valor}],
      }).then(function(output) {
         rpc.query({
          model:'covid.anexo',
          method:'file_excel',
          args:[registro_id],
        }).then(function(){
          // location.reload();
        });
      });

    },
    click_registro_evaluado: function(ev) {
      var registro_id = $(".form-lista-covid").data("registro_id");
      var valor = $(ev.target).val();
      rpc.query({
        model: 'covid.anexo',
        method: 'write',
        args: [[registro_id],{ "evaluado":valor}],
      }).then(function(output) {
         rpc.query({
          model:'covid.anexo',
          method:'file_excel',
          args:[registro_id],
        }).then(function(){
          // location.reload();
        });
      });

    },

    click_registro_evaluacion: function(ev) {
      var registro_id = $(".form-lista-covid").data("registro_id");
      var valor = $(ev.target).val();
      rpc.query({
        model: 'covid.anexo',
        method: 'write',
        args: [[registro_id],{ "fecha":valor}],
      }).then(function(output) {
         rpc.query({
          model:'covid.anexo',
          method:'file_excel',
          args:[registro_id],
        }).then(function(){
          // location.reload();
        });
      });

    },

    click_nuevo_elemento:  function(ev){
      var registro_id = $(".form-lista-covid").data("registro_id");
      var evento = $(ev.currentTarget)
      var name = evento.parent().parent().find("input[name='new-objetivo-especifico']").val()
      var lista_id = evento.data("general_id")
      alert(name)
      rpc.query({
          model:'covid.anexo.sublista',
          method:'create',
          args:[{ "name": name, "lista_id": lista_id}],
        }).then(function(){
           rpc.query({
            model:'covid.anexo',
            method:'file_excel',
            args:[registro_id],
          }).then(function(){
            // location.reload();
          });
          location.reload();

        });
      },

  })

})
