odoo.define("s3.registro_niosh",function(require){
    'use strict';

    var publicWidget = require("web.public.widget");
    var rpc = require("web.rpc");
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;

    publicWidget.registry.FormEditableSaveniosh = publicWidget.Widget.extend({
      selector:"#formulario_editar_field_niosh",
      events:{
            'click .botton-guardar-field-data':"action_guardar_field_data",
            "change #image_input":"click_image_input",
            "change .field-odoo":"click_change_field",
      },
      click_change_field: async function(ev){
        var form = $('#formulario_editar_field_niosh');
      },
      action_guardar_field_data: async function(ev){
          var form = $('#formulario_editar_field_niosh');
          var model = $('#formulario_editar_field_niosh').data("model_id");
          var record_id = $('#formulario_editar_field_niosh').data("record_id");
          var dict = []
          $(".field-odoo", form).each(async function(){
            var nombre = $(this).attr("name");
            var tipo = $(this).attr("type");
            if (tipo == "checkbox") {
               var valor = $(this).is(":checked");
            } else {
               var valor = $(this).val();
              }
            dict.push({
                 type:   tipo,
                 value: valor,
                 name: nombre
             });
        });
        await rpc.query({
            route:"/guardar_field_odoo",
            params:{
              model:model,
              record_id:record_id,
              inputs:dict,
            }
        }).then(function(res){
            location.reload();
        })

      },
      click_image_input:async function(ev){
        var e =  $(ev.target);
        var record_id = $('#formulario_editar_field_niosh').data("record_id");
        for (var i = 0; i < e.length; i++) {
            $( ".image_file_input" ).remove();
           var file = e[0].files[0];
           var img = document.createElement("img");
           var reader = new FileReader();
           var binary = "aaa";
           img.className = "image_file_input";
           reader.onloadend = async function() {
                img.src = reader.result;
                var dataType = reader.result.split(';base64,')[1];
                await rpc.query({
                    model:"niosh.niosh",
                    method:"write",
                    args:[[record_id],{"imagen":dataType}]
                }).then(function(res){
                });
           }
           reader.readAsDataURL(file);
           $(ev.target).after(img);
          }

      },


    })

})
