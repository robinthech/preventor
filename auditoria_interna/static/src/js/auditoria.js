odoo.define("auditoria_interna.auditoria",function(require){
    'use strict';

    var publicWidget = require("web.public.widget")
    var core = require("web.core")
    var rpc = require("web.rpc")
    var Widget = require("web.Widget")
    var qweb = core.qweb

    publicWidget.registry.Crearauditoria = publicWidget.Widget.extend({
        selector:".auditoria-interna",
        events:{
          'click .nueva-auditoria-interna': 'click_nueva_auditoria',
        //   'click .actualizar-excel': 'actualiza_excel',
        //   'click .botton-eliminar-verificacion': 'action_eliminar_verificacion',
        //   'click .botton-eliminar-programa': 'action_eliminar_programa',
        },
        click_nueva_auditoria:function(ev){
          var cliente = $(this.$el).find("input[name='new-auditoria-razon']").val()
          var ruc = $(this.$el).find("input[name='new-auditoria-ruc']").val()
          var domicilio = $(this.$el).find("input[name='new-auditoria-domicilio']").val()
          var actividad = $(this.$el).find("input[name='new-auditoria-actividad']").val()
          rpc.query({
    				model:'auditoria.interna',
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
        },
        click_guardar_archivo:function(ev){
            console.log('atachemnt')

            var files = ev.target.files;
            console.log(files)
            var reader = new FileReader();
            reader.readAsDataURL(documentos);
            reader.onload = function () {
                console.log(reader.result);
            };
            var output = [];
            for (var i = 0, f; f = files[i]; i++) {
              output.push(escape(f.name), ', ');
            }
            document.getElementById('list').innerHTML = output.join('');

            // rpc.query({
            //           model:'auditoria.interna',
            //           method:'guardar_documento',
            //           args:[[1],{"attachment": resultado}],
            //         }).then(function(){
            //       location.reload();
            //   });
          },
        // actualiza_excel: function(ev){
        //     var evento = $(ev.currentTarget)
        //     var lista_id = evento.closest('.actualizar-excel').data("verificacion_id")
        //     // console.log(lista_id)
        //     rpc.query({
        //       model:'lista.verificacion',
        //       method:'file_excel',
        //       args:[lista_id],
        //     }).then(function(){
        //       location.reload();

        //     });
        // },
        // action_eliminar_verificacion: function(ev) {
        //     var lista_id = $(ev.target).data("verificacion_id");
        //     rpc.query({
        //       model: "lista.verificacion",
        //       method: "unlink",
        //       args: [lista_id]
        //     }).then(function(res) {
        //       location.reload();
        //     });
        // },
        // action_eliminar_programa: function(ev) {
        //   console.log('entra')
        //   var programa_id = $(ev.target).data("programa_id");

        //   rpc.query({
        //     model: "programa.anual",
        //     method: "unlink",
        //     args: [programa_id]
        //   }).then(function(res) {
        //     location.reload();
        //   });
        // },
    })

    publicWidget.registry.Formularioauditoria = publicWidget.Widget.extend({
      selector: '.table-auditoria',
      events:{
        'change .linea_auditoria': 'change_linea_auditoria',
        'change .linea_auditor': 'change_linea_auditor',
        'change .linea_medida': 'change_linea_medidas',
        'change .linea_registro': 'change_linea_registro',
        'click .nuevo-auditor': 'click_nuevo_auditor',
        'click .nuevo-registro': 'click_nuevo_registro',
        'click .nueva-medida': 'click_nueva_medida',
      },
      change_linea_auditoria:function(ev){
        var evento = $(ev.currentTarget)
        var auditoria_id = evento.parents('.auditoria_id').data("auditoria_id")
        var opcion = evento.val()
        var name = evento.attr("name")
        rpc.query({
          model:'auditoriainterna.transient',
          method:'guardar_linea',
          args:[1,auditoria_id,name,opcion]
        })
      },
      click_nuevo_auditor:function(ev){
        var evento = $(ev.currentTarget)
        var auditoria_id = evento.data("auditoria_id")
        var nombre = $(this.$el).find("input[name='new-auditor-nombre']").val()
        var registro = $(this.$el).find("input[name='new-auditor-registro']").val()
        rpc.query({
          model:'auditor.auditor',
          method:'create',
          args:[{ "name": nombre,"registro": registro,"auditoria_id": auditoria_id}],
          }).then(function(){
            location.reload();
          });
      },
      click_nueva_medida:function(ev){
        var evento = $(ev.currentTarget)
        var auditoria_id = evento.data("auditoria_id")
        var medida_correctiva = $(this.$el).find("input[name='new-medida-descripcion']").val()
        var responsable = $(this.$el).find("input[name='new-medida-responsable']").val()
        rpc.query({
          model:'no.conformidad',
          method:'create',
          args:[{ "medida_correctiva": medida_correctiva,"responsable": responsable,"auditoria_id": auditoria_id}],
          }).then(function(){
            location.reload();
          });
      },
      click_nuevo_registro:function(ev){
        var evento = $(ev.currentTarget)
        var auditoria_id = evento.data("auditoria_id")
        var fechainicial = $(this.$el).find("input[name='new-registro-fecha']").val()
        var fecha = fechainicial.substr(0,10)+' '+fechainicial.substr(11,15)
        var procesos = $(this.$el).find("input[name='new-registro-procesos']").val()
        var responsables = $(this.$el).find("input[name='new-registro-responsables']").val()
        rpc.query({
          model:'registro.auditoria',
          method:'create',
          args:[{ "name": procesos,"responsables": responsables,"fecha": fecha,"auditoria_id": auditoria_id}],
          }).then(function(){
            location.reload();
          });
      },
      change_linea_auditor:function(ev){
        var evento = $(ev.currentTarget)
        var auditoria_id = evento.parents('.auditor_id').data("auditor_id")
        var opcion = evento.val()
        var name = evento.attr("name")
        rpc.query({
          model:'auditor.transient',
          method:'guardar_linea',
          args:[1,auditoria_id,name,opcion]
        })
      },
      change_linea_registro:function(ev){
        var evento = $(ev.currentTarget)
        var registro_id = evento.parents('.registro_id').data("registro_id")
        var opcion = evento.val()
        var name = evento.attr("name")
        if(name=="fecha"){
          var opcion = opcion.substr(0,10)+' '+opcion.substr(11,15)
          console.log(opcion)
        }
        rpc.query({
          model:'registro.transient',
          method:'guardar_linea',
          args:[1,registro_id,name,opcion]
        })
      },
      change_linea_medidas:function(ev){
        var evento = $(ev.currentTarget)
        var medidas_id = evento.parents('.medidas_id').data("medidas_id")
        console.log(medidas_id)
        var opcion = evento.val()
        console.log(typeof(opcion))
        var name = evento.attr("name")
        console.log(opcion)
        console.log(name)
        rpc.query({
          model:'noconfomidad.transient',
          method:'guardar_linea',
          args:[1,medidas_id,name,opcion]
        })
      },
    })
})
