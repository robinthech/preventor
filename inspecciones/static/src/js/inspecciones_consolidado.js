odoo.define("inspecciones.inspecciones_consolidado", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb


  publicWidget.registry.ConsolidadoSubestandae = publicWidget.Widget.extend({
    selector: ".consolidado_inspeccion_substandar",
    xmlDependencies:["/inspecciones/static/src/xml/reporte_consolidado.xml"],
    events:{
        'click .wrn-btn-reporte':'click_render_reporte',
        'click .send_email':'click_send_email',
        'click .button-enviar-email':'click_enviar_email',
    },
    jsLibs: [
      '/web/static/lib/Chart/Chart.js',
    ],
    init:function(){
        this._super.apply(this, arguments);
    },
    click_send_email:function(){
        $("#send_email").modal();
    },
    click_enviar_email:function(){

    },

    click_render_reporte:function(ev){
        $( ".loading-learning ").show( "slow" );
        var responsable_id = $(this.$el).find("select[name='responsable_id']").val();
        $(".wrn-btn-reporte").attr("disabled",true);
        rpc.query({
          model:'edit.inspecciones',
          method:'funcion_matriz_reporte',
          args:[1,responsable_id],
        }).then(function(matriz_general){
          console.log(matriz_general);
           var diario = qweb.render("inspecciones.reporte_consolidado_inspeciones",{matriz: matriz_general});
           console.log(diario);
           $("#reporte-consolidado-inspecciones").html(diario);
           $(".wrn-btn-reporte").attr("disabled",false)
           $( ".loading-learning ").hide( "slow" );

        });


    },

  })


})
