odoo.define("programa_anual.programa",function(require){
    'use strict';

    var publicWidget = require("web.public.widget")
    var core = require("web.core")
    var rpc = require("web.rpc")
    var Widget = require("web.Widget")
    var qweb = core.qweb

    if (window.screen.width < 1024){
      $('.table-programa-anual .checkesperado').removeClass("checkesperado").addClass("otro");
      $('.table-programa-anual .checkBtn').removeClass("checkBtn").addClass("checkBtnotro");
      $('.table-programa-anual td.p-0').removeClass("p-0").addClass("otro2");
    }else{
      $('.table-programa-anual .otro').removeClass("otro").addClass("checkesperado");
      $('.table-programa-anual td.otro2').removeClass("otro2").addClass("p-0");
      $('.table-programa-anual .checkBtnotro').removeClass("checkBtnotro").addClass("checkBtn");
    }

    window.onresize = function(event) {
    if (window.screen.width < 1024){
      $('.table-programa-anual .checkesperado').removeClass("checkesperado").addClass("otro");
      $('.table-programa-anual .checkBtn').removeClass("checkBtn").addClass("checkBtnotro");
      $('.table-programa-anual td.p-0').removeClass("p-0").addClass("otro2");
    }else{
      $('.table-programa-anual .otro').removeClass("otro").addClass("checkesperado");
      $('.table-programa-anual td.otro2').removeClass("otro2").addClass("p-0");
      $('.table-programa-anual .checkBtnotro').removeClass("checkBtnotro").addClass("checkBtn");
    }

    };

    publicWidget.registry.SectionPrograma = publicWidget.Widget.extend({
        selector:".table_programa",
        events:{
            'change input:checkbox': 'change_checkbox',
            'change .linea_programa': 'change_linea_programa',
            'change .linea_general': 'change_linea_general',
            'change .linea_especifico': 'change_linea_especifico',
            'change .linea_actividad': 'change_linea_actividad',
            'change .linea_actividad_observaciones': 'change_linea_actividad_observaciones',
            'click .nuevo-objetivo-especifico': 'click_nuevo_especifico',
            'click .nuevo-objetivo-general': 'click_nuevo_general',
            'click .nueva-actividad': 'click_nueva_actividad',
            'click .botton-eliminar-general': 'action_eliminar_general',
            'click .botton-eliminar-especifico': 'action_eliminar_especifico',
            // "click a.js_add_cart_json": "_onClickAddCartJSONT",
        },
        change_checkbox: async function(ev){
            var evento = $(ev.currentTarget)
            var programa_id = evento.parents('.programa_id').data("programa_id")
            var registro_id = evento.attr("registro_id")
            var actividad_id = evento.closest('tr').data("actividad_id")
            var name = evento.attr("name")
            var opcion
            var estado
            if(evento.is(':checked')){
              opcion = true
            }else{
              opcion = false
            }

            var avance_p = $("input[tipo='programado'][registro_id='"+ registro_id +"']:checked").length
            var avance_e = $("input[tipo='ejecutado'][registro_id='"+ registro_id +"']:checked").length
            // if(avance_p > 0){
            var resultado = ((avance_e/avance_p)*100).toFixed(2)
            // }else{
            //   var resultado = (0).toFixed(2)
            // }
            // console.log(0.toFixed(2))
            var final = `${resultado}%`
            if (final == "100.00%"){
              estado = "Finalizado"
            }else if(final == "0.00%"){
              estado = "Pendiente"
            }else{
              estado = "En proceso"
            }

            await rpc.query({
              model:'actividad.transient',
              method:'guardar_linea',
              args:[1,actividad_id,name,opcion]
            })

            await rpc.query({
              model:'actividad.transient',
              method:'write_linea',
              args:[1,actividad_id,estado,avance_p,final],
            }).then(function(res){
              $("#pronosticado-" + registro_id + " strong").html(res[1])
              $("#esperado-" + registro_id + " strong").html(res[2])
              $("#estado-" + registro_id + " strong").html(res[0])
            });

            await rpc.query({
              model:'programa.anual',
              method:'datos_sst',
              args:[programa_id],
            }).then(function(){
              // location.reload();
            });
        },
        click_nuevo_especifico: async function(ev){
          var evento = $(ev.currentTarget)
          var programa_id = evento.parents('.programa_id').data("programa_id")
          var name = evento.parents(".general_id").find("input[name='new-objetivo-especifico']").val()
          var objetivo_id = evento.data("general_id")
          await rpc.query({
    					model:'objetivo.especifico',
    					method:'create',
    					args:[{ "name": name, "objetivo_id": objetivo_id}],
    				}).then(function(){

            });

          await rpc.query({
            model:'programa.anual',
            method:'datos_sst',
            args:[programa_id],
          }).then(function(){
            location.reload();
          });
        },
        click_nuevo_general:async function(ev){
          var evento = $(ev.currentTarget)
          var name = $(this.$el).find("input[name='new-objetivo-general']").val()
          var programa_id = evento.parents('.programa_id').data("programa_id")
          var programa_anual_id = evento.data("programa_anual_id")
          $(".nuevo-objetivo-general").attr("disabled",true)
            await rpc.query({
    					model:'objetivo.general',
    					method:'create',
    					args:[{ "name": name, "programa_id": programa_anual_id}],
    				}).then(function(){
            });

            await rpc.query({
              model:'programa.anual',
              method:'datos_sst',
              args:[programa_id],
            }).then(function(){
              location.reload();
            });
        },
        click_nueva_actividad: async function(ev){
          var evento = $(ev.currentTarget)
          var programa_id = evento.parents('.programa_id').data("programa_id")
          var name = evento.parents(".actividad").find("input[name='new-actividad-name']").val()
          var responsable = evento.parents(".actividad").find("input[name='new-actividad-responsable']").val()
          var area = evento.parents(".actividad").find("input[name='new-actividad-area']").val()
          var objetivo_id = evento.data("general_id")
          $(".nueva-actividad").attr("disabled",true)
          await rpc.query({
    				model:'actividad.actividad',
    				method:'create',
    				args:[{ "name": name,"responsable": responsable,"area": area, "objetivo_id": objetivo_id}],
    			}).then(function(){
          });

          await rpc.query({
            model:'programa.anual',
            method:'datos_sst',
            args:[programa_id],
          }).then(function(){
            location.reload();
          });
        },
        change_linea_programa: async function(ev){
          var evento = $(ev.currentTarget)
          var programa_id = evento.parents('.programa_id').data("programa_id")
          var opcion = evento.val()
          var name = evento.attr("name")
          await rpc.query({
            model:'programaanual.transient',
            method:'guardar_linea',
            args:[1,programa_id,name,opcion]
          })

          await rpc.query({
            model:'programa.anual',
            method:'datos_sst',
            args:[programa_id],
          }).then(function(){

          });
        },
        change_linea_general: async function(ev){
          var evento = $(ev.currentTarget)
          var programa_id = evento.parents('.programa_id').data("programa_id")
          var general_id = evento.parents('.general_id').data("general_id")
          var opcion = evento.val()
          var name = evento.attr("name")
          await rpc.query({
            model:'objetivogeneral.transient',
            method:'guardar_linea',
            args:[1,general_id,name,opcion]
          })

          await rpc.query({
            model:'programa.anual',
            method:'datos_sst',
            args:[programa_id],
          }).then(function(){

          });
        },
        change_linea_especifico:async function(ev){
          var evento = $(ev.currentTarget)
          var programa_id = evento.parents('.programa_id').data("programa_id")
          var especifico_id = evento.data("especifico_id")
          var opcion = evento.val()
          var name = evento.attr("name")
          await rpc.query({
            model:'objetivoespecifico.transient',
            method:'guardar_linea',
            args:[1,especifico_id,name,opcion]
          })
          await rpc.query({
            model:'programa.anual',
            method:'datos_sst',
            args:[programa_id],
          }).then(function(){
            location.reload();
          });
        },
        change_linea_actividad:async function(ev){
          var evento = $(ev.currentTarget)
          var actividad_id = evento.parents('.actividad_id').data("actividad_id")
          var programa_id = evento.parents('.programa_id').data("programa_id")
          var opcion = evento.val()
          var name = evento.attr("name")
          await rpc.query({
            model:'actividad.transient',
            method:'guardar_linea',
            args:[1,actividad_id,name,opcion]
          })
          await rpc.query({
            model:'programa.anual',
            method:'datos_sst',
            args:[programa_id],
          }).then(function(){
            location.reload();
          });
        },
        change_linea_actividad_observaciones:async function(ev){
          var evento = $(ev.currentTarget)
          var programa_id = evento.parents('.programa_id').data("programa_id")
          var actividad_id = evento.parents('.actividad_id').data("actividad_id")
          var opcion = evento.find("textarea").val()
          var name = evento.find("textarea").attr("name")
          await rpc.query({
            model:'actividad.transient',
            method:'guardar_linea',
            args:[1,actividad_id,name,opcion]
          })
          await rpc.query({
            model:'programa.anual',
            method:'datos_sst',
            args:[programa_id],
          })
        },
        action_eliminar_general:async function(ev) {
          var evento = $(ev.currentTarget)
          var general_id = $(ev.target).data("general_id");
          var programa_id = evento.parents('.programa_id').data("programa_id")
          var domain = [('objetivo_id', '=', general_id)];
          console.log(domain)
          console.log(general_id)
          await rpc.query({
            model: "objetivo.general",
            method: "unlink",
            args: [general_id],
          }).then(function(res) {
            // location.reload();
          });


          await rpc.query({
            model:'programa.anual',
            method:'datos_sst',
            args:[programa_id],
          }).then(function(){
            location.reload();
          });


        },
        action_eliminar_especifico: async function(ev) {
          var evento = $(ev.currentTarget)
          var especifico_id = $(ev.target).data("especifico_id");
          var programa_id = evento.parents('.programa_id').data("programa_id")

          await rpc.query({
            model: "objetivo.especifico",
            method: "unlink",
            args: [especifico_id]
          }).then(function(res) {
            // location.reload();
          });


          await rpc.query({
            model:'programa.anual',
            method:'datos_sst',
            args:[programa_id],
          }).then(function(){
            location.reload();
          });
        },
    })

    publicWidget.registry.Crearprograma = publicWidget.Widget.extend({
        selector:".programa-anual",
        events:{
          'click .nuevo-programa-anual': 'click_nuevo_programa',
          'click .actualizar-excel': 'actualiza_excel',
          'click .botton-eliminar-verificacion': 'action_eliminar_verificacion',
          'click .botton-eliminar-programa': 'action_eliminar_programa',
          'click .file-gratis': 'file_gratis',
        },
        click_nuevo_programa:function(ev){
          var cliente = $(this.$el).find("input[name='new-lista-cliente']").val()
          var ruc = $(this.$el).find("input[name='new-lista-ruc']").val()
          var domicilio = $(this.$el).find("input[name='new-lista-domicilio']").val()
          var actividad = $(this.$el).find("input[name='new-lista-actividad']").val()
          var plan_id = $('#modulo-programa-anual').data("plan_id");
            rpc.query({
              model: 'actividad.transient',
              method: 'limites_permisos',
              args: [1,plan_id],
            }).then(function(output) {
              if (output) {
          $(".nuevo-programa-anual").attr("disabled",true)
                rpc.query({
          				model:'programa.anual',
          				method:'create',
          				args:[{
                    "cliente": cliente,
                    "ruc": ruc,
                    "domicilio": domicilio,
                    "actividad": actividad
                  }],
            			}).then(function(){
                    location.reload();
                  });
              }
              else {
                swal({
                    title: "Programa Anual",
                    text: "No puede crear más Programa Anual.",
                    icon: "info",
                  });
              }

            });
        },
        actualiza_excel: function(ev){
            var evento = $(ev.currentTarget)
            var lista_id = evento.closest('.actualizar-excel').data("verificacion_id")
            // console.log(lista_id)
            rpc.query({
              model:'programa.anual',
              method:'datos_sst',
              args:[lista_id],
            }).then(function(){
              location.reload();

            });
        },
        action_eliminar_programa: function(ev) {
          console.log('entra')
          var programa_id = $(ev.target).data("programa_id");

          rpc.query({
            model: "programa.anual",
            method: "unlink",
            args: [programa_id]
          }).then(function(res) {
            location.reload();
          });
        },
        file_gratis: function(ev) {
          swal({
            title: "Programa anual",
            text: "No puede descargar más archivos excel con el plan Gratis.",
            icon: "info",
          });
        },
    })

})
