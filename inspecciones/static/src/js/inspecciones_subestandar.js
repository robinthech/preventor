odoo.define("inspecciones.inspecciones_subestandar", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb


  publicWidget.registry.FormularioInspeccionesSubestandar = publicWidget.Widget.extend({
    selector: ".principal-inspecciones-subestandar",
    events: {
      'click .button-guardar-inspeccion': 'click_guardar_inspeccion',
      'click .botton-nueva-condicion-subestandar': 'click_nueva_inspeccion_subestandar',

    },
    click_nueva_inspeccion_subestandar: function(ev) {
      var name = $(ev.target).parent().parent().find("input[name='new-registro-name']").val();
      var condicion_id = parseInt($(ev.target).data("condicion_id"));
      rpc.query({
        model: 'sub.condicion',
        method: 'create',
        args: [{
          "name": name,
          "condicion_id": parseInt(condicion_id) ,
        }],
      }).then(function() {
        location.reload();

      });

    },

    click_guardar_inspeccion:async function(ev){
      var form = $('#formulario_editar_inspecciones');
      var model = 'sub.condicion';
      var record_line_id = $('#formulario_editar_inspecciones').data("record_id");
      var dict = []
      $(".field-odoo", form).each(async function(){
        var nombre = $(this).attr("name");
        var tipo = $(this).attr("type");
        var requisito_id = $(this).data("record_id");
        var model_id = $(this).data("model_id");
        if (tipo == "checkbox") {
           var valor = $(this).is(":checked");
        } else {
           var valor = $(this).val();
          }
        dict.push({
             type:   tipo,
             id:   requisito_id,
             value: valor,
             name: nombre,
             model_id:model_id

         });
       });
        console.log(dict);
        await rpc.query({
            route:"/guardar_field_odoo_inspeccion",
            params:{
              model:model,
              record_id:record_line_id,
              inputs:dict
            }
        }).then(function(res){
            location.reload()

        })


    },

  })

  publicWidget.registry.FormatoFormularioInspeccionesSubestandar = publicWidget.Widget.extend({
    selector: ".formato-principal-inspecciones-subestandar",
    events: {
      'click .botton-nueva-condicion-subestandar': 'click_nueva_inspeccion_subestandar',

    },
    click_nueva_inspeccion_subestandar: function(ev) {
      var name = $(ev.target).parent().parent().find("input[name='new-registro-name']").val();
      var condicion_id = parseInt($(ev.target).data("condicion_id"));
      rpc.query({
        model: 'formato.sub.condicion',
        method: 'create',
        args: [{
          "name": name,
          "condicion_id": parseInt(condicion_id) ,
        }],
      }).then(function() {
        location.reload();

      });

    },

  })

})
