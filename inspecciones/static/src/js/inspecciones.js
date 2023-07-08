odoo.define("inspecciones.inspecciones", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb


  publicWidget.registry.FormularioInspeccionesGeneral = publicWidget.Widget.extend({
    selector: ".principal-inspecciones-general",
    events: {
      'click .button-guardar-inspeccion': 'click_guardar_inspeccion',

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
})
