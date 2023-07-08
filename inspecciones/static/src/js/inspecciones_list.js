odoo.define("inspecciones.inspecciones_list", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb


  publicWidget.registry.ListaInspecciones = publicWidget.Widget.extend({
    selector: ".list-inspecciones",
    events: {
      'click .botton-inspecciones': 'click_nuevo_registro_inspecciones',
      'click .botton-eliminar-inspecciones': 'click_eliminar_inspecciones',

    },

    click_eliminar_inspecciones:function(ev){
      console.log("asasdasd");
      var permiso_id = $(ev.target).data("registro_id");
      rpc.query({
        model: "inspeccion",
        method: "unlink",
        args: [permiso_id]
      }).then(function(res) {
        location.reload();
      });

    },
    click_nuevo_registro_inspecciones: function(ev) {
      var name = $(this.$el).find("input[name='new-registro-name']").val()
      var formato_id = $(this.$el).find("select[name='new-formato_id']").val()
      var plan_id = $('#modulo-inspecciones').data("plan_id");
      console.log(formato_id);
      console.log(name);
      rpc.query({
        model: 'inspeccion',
        method: 'create',
        args: [{
          "name": name,
          "formato_id": parseInt(formato_id) ,
        }],
      }).then(function() {
        location.reload();

      });

    },

  })

  publicWidget.registry.ListaFormatos = publicWidget.Widget.extend({
    selector: ".list-formatos",
    events: {
      'click .botton-formatos': 'click_nuevo_registro_formatos',
      'click .botton-eliminar-formatos': 'click_eliminar_formatos',

    },

    click_nuevo_registro_formatos:function(ev){
      var permiso_id = $(ev.target).data("registro_id");
      rpc.query({
        model: "formato.inspeccion",
        method: "unlink",
        args: [permiso_id]
      }).then(function(res) {
        location.reload();
      });

    },
    click_nuevo_registro_formatos: function(ev) {
      var name = $(this.$el).find("input[name='new-registro-name']").val();
      var formato_id = $(this.$el).find("select[name='new-formato_id']").val();
      rpc.query({
        model: 'formato.inspeccion',
        method: 'create',
        args: [{
          "name": name,
          "formato_id": parseInt(formato_id) ,
          "origen":'2'
        }],
      }).then(function() {
        location.reload();

      });

    },

  })


})
