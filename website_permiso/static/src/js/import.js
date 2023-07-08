odoo.define("website_permiso.import", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb


  publicWidget.registry.ImportarTrabajador = publicWidget.Widget.extend({
    selector:"#import_trabajador",
    events: {
      'click .button-importar-trabajador': 'click_import_validar',
      'click .button-importar-trabajador-contratista': 'click_import_validar_contratista',
      'click .button-importar-requisito': 'click_import_requisito',
      'click .button-importar-requisito-estandar': 'click_import_requisito_estandar',
      'change #imput_file_excel': 'change_imput_file',

    },
    start: function(){
    },
    change_imput_file: function(ev){
      var files = $('#imput_file_excel');
			$('.custom-file-label').addClass("selected").html(files[0].files[0].name);
    },
    click_import_requisito:function(ev){
        var e =  $(ev.target);
        var fimput_file_excelile = $('#imput_file_excel')
        for (var i = 0; i < fimput_file_excelile.length; i++) {
           var file = fimput_file_excelile[0].files[0];
           var reader = new FileReader();
           reader.onloadend = async function() {
                var dataType = reader.result.split(';base64,')[1];
                await rpc.query({
                    model:"user.transient",
                    method:"import_requisito",
                    args:[[1],{"file_imput":dataType}]
                }).then(function(res){
                    location.reload();
                });
           }
           reader.readAsDataURL(file);
          }
    },

    click_import_validar:function(ev){
        var e =  $(ev.target);
        var fimput_file_excelile = $('#imput_file_excel')
        for (var i = 0; i < fimput_file_excelile.length; i++) {
           var file = fimput_file_excelile[0].files[0];
           var reader = new FileReader();
           reader.onloadend = async function() {
                var dataType = reader.result.split(';base64,')[1];
                await rpc.query({
                    model:"user.transient",
                    method:"import_user",
                    args:[[1],{"file_imput":dataType}]
                }).then(function(res){
                    location.reload();
                });
           }
           reader.readAsDataURL(file);
          }
    },
    click_import_validar_contratista:function(ev){
      	var evento = $(ev.currentTarget);
        var contratista_id = evento.data("contratista_id");
        var fimput_file_excelile = $('#imput_file_excel');
        for (var i = 0; i < fimput_file_excelile.length; i++) {
           var file = fimput_file_excelile[0].files[0];
           var reader = new FileReader();
           reader.onloadend = async function() {
                var dataType = reader.result.split(';base64,')[1];
                await rpc.query({
                    model:"user.transient",
                    method:"import_user_contratista",
                    args:[[1],{"file_imput":dataType},contratista_id]
                }).then(function(res){
                  location.reload();
                });
           }
           reader.readAsDataURL(file);
          }
    },

  })

  // manejar Requisitos

  publicWidget.registry.RequisitosTrabajador = publicWidget.Widget.extend({
    selector: ".requisito-trabajador-form",
    events: {
      'click .button-nuevo-requisito-estandar': 'click_nuevo_requisito_estandar',
      'click .button-nuevo-requisito': 'click_nuevo_requisito',
      'click .button-guardar-requisito': 'click_guardar_requisito',
      'click .button-guardar-requisito-estandar': 'click_guardar_requisito_estandar',
      'click .botton-eliminar-requisito': 'click_eliminar_requisito',
      'click .botton-eliminar-requisito-estandar': 'click_eliminar_requisito_estandar',
      'click .button-nuevo-requisito-contratista': 'click_nuevo_requisito_contratista',
      'click .button-guardar-requisito-contratista': 'click_guardar_requisito_contratista',
    },
    start: function(){
    },
    click_guardar_requisito_estandar:function(ev){
      console.log("registry");
        var evento = $(ev.currentTarget)
        var id = evento.data("requisito_id")
        var nombre = evento.closest(".modal-content").find("input[name='new-requisito-nombres']").val()
        rpc.query({
          model:'requisito.estandar',
          method:'write',
          args:[[id],{"name": nombre}],
        }).then(function(){
          location.reload();
        })
    },
    click_guardar_requisito:async function(ev){
        var e =  $(ev.target);
        var form = $('#formulario_editar_field_requisito');
        var model = 'requisito.trabajador';
        var record_id = $('#formulario_editar_field_requisito').data("record_id");
        var dict = []
        $("input[class='field-odoo']", form).each(async function(){
          var nombre = $(this).attr("name");
          var tipo = $(this).attr("type");
          var requisito_id = $(this).data("record_id");
          if (tipo == "checkbox") {
             var valor = $(this).is(":checked");
          } else {
             var valor = $(this).val();
            }
          dict.push({
            type:   tipo,
               id:   requisito_id,
               value: valor,
               name: nombre
           });
      });
      await rpc.query({
          route:"/guardar_field_odoo_requisito",
          params:{
            model:model,
            record_id:record_id,
            inputs:dict,
          }
      }).then(function(res){
          location.reload();

      })
    },

    click_nuevo_requisito:function(ev){
      var nombre = $(this.$el).find("input[name='new-requisito-nombre']").val()
      var trabajador_id = $("#formulario_editar_field_requisito").data("record_id");
        rpc.query({
          model:'requisito.trabajador',
          method:'create',
          args:[{ "name": nombre,'trabajador_id':trabajador_id}],
        }).then(function(){
          location.reload();

        });

    },
    click_nuevo_requisito_estandar:function(ev){
      var nombre = $(this.$el).find("input[name='new-requisito-nombre']").val()
      var trabajador_id = $("#formulario_editar_field_requisito").data("record_id");
        rpc.query({
          model:'requisito.estandar',
          method:'create',
          args:[{ "name": nombre}],
        }).then(function(){
          location.reload();

        });

    },
    click_eliminar_requisito:function(ev){
      var requisito_id = $(ev.target).data("requisito_id");
      rpc.query({
        model: "requisito.trabajador",
        method: "unlink",
        args: [requisito_id]
      }).then(function(res) {
        location.reload();
      });

    },
    click_eliminar_requisito_estandar:function(ev){
      console.log("eliminar");
      var requisito_id = $(ev.target).data("requisito_id");
      rpc.query({
        model: "requisito.estandar",
        method: "unlink",
        args: [requisito_id]
      }).then(function(res) {
        location.reload();
      });

    },

    click_guardar_requisito_contratista:async function(ev){
        var e =  $(ev.target);
        var form = $('#formulario_editar_field_requisito');
        var model = 'requisito.trabajador';
        var record_id = $('#formulario_editar_field_requisito').data("record_id");
        var dict = []
        $("input[class='field-odoo']", form).each(async function(){
          var nombre = $(this).attr("name");
          var tipo = $(this).attr("type");
          var requisito_id = $(this).data("record_id");
          if (tipo == "checkbox") {
             var valor = $(this).is(":checked");
          } else {
             var valor = $(this).val();
            }
          dict.push({
            type:   tipo,
               id:   requisito_id,
               value: valor,
               name: nombre
           });
      });
      await rpc.query({
          route:"/guardar_field_odoo_requisito_contratista",
          params:{
            model:model,
            record_id:record_id,
            inputs:dict,
          }
      }).then(function(res){
          location.reload()

      })
    },

    click_nuevo_requisito_contratista:function(ev){
      var nombre = $(this.$el).find("input[name='new-requisito-nombre']").val()
      var trabajador_contratista_id = $("#formulario_editar_field_requisito").data("record_id");
        rpc.query({
          model:'requisito.trabajador',
          method:'create',
          args:[{ "name": nombre,'trabajador_contratista_id':trabajador_contratista_id}],
        }).then(function(){
          location.reload();

        });

    },

  })

  publicWidget.registry.ImportarTrabajador = publicWidget.Widget.extend({
    selector:".formulario_sede_area",
    events: {
      'click .button-nuevo-area': 'click_nueva_area',
      'click .button-guardar-sede': 'click_guardar_sede',
      'click .botton-eliminar-area': 'click_eliminar',

    },
    start: function(){
    },

    click_eliminar:function(ev){
      console.log("eliminar");
      var requisito_id = $(ev.target).data("requisito_id");
      rpc.query({
        model: "area.area",
        method: "unlink",
        args: [requisito_id]
      }).then(function(res) {
        location.reload();
      });

    },
    click_nueva_area:function(ev){
      var nombre = $(this.$el).find("input[name='new-area-nombre']").val();
      var sede_id = $(".formulario_sede_area").data("sede_id");
        rpc.query({
          model:'area.area',
          method:'create',
          args:[{ "name": nombre,'sede_id':sede_id}],
        }).then(function(){
          location.reload();

        });
    },
    click_guardar_sede: function(ev){
        	var evento = $(".formulario_sede_area");
          var id = evento.data("sede_id")
          var name = evento.find("input[name='name']").val();
          var encargado = evento.find("select[name='encargado']").val();
          var dni =evento.find("input[name='dni']").val();
          var puesto = evento.find("input[name='puesto']").val();
          var trabajadores = evento.find("input[name='trabajadores']").val();
          rpc.query({
            model:'sede.sede',
            method:'write',
            args:[[id],{"name": name,"encargado": encargado,"dni": dni,"puesto": puesto,"trabajadores": trabajadores}],
          }).then(function(){
            location.reload();
          })

    },

  })

})
