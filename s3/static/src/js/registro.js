odoo.define("s3.registro",function(require){
    'use strict';

    var publicWidget = require("web.public.widget");
    var rpc = require("web.rpc");
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;
    publicWidget.registry.Registros = publicWidget.Widget.extend({
        selector:".row_registro",
        events:{
            'click .botton-crear-registro':"action_crear_registro",
            'click .botton-crear-ilu':"action_crear_iluminacion",
            'click .botton-editar-ilu':"action_editar_iluminacion",
            'click .botton-eliminar-ilu':"action_eliminar_iluminacion",
            'click .botton-crear-dosi':"action_crear_dosimetria",
            'click .botton-editar-dosi':"action_editar_dosimetria",
            'click .botton-eliminar-dosi':"action_eliminar_dosimetria",
            'click .botton-crear-sono':"action_crear_sonometria",
            'click .botton-editar-sono':"action_editar_sonometria",
            'click .botton-eliminar-sono':"action_eliminar_sonometria",
            'click .botton-crear-reba':"action_crear_reba",
            'click .botton-crear-rosa':"action_crear_rosa",
            'click .botton-crear-niosh':"action_crear_niosh",
            'click .botton-editar-reba':"action_editar_reba",
            'click .botton-eliminar-reba':"action_eliminar_reba",
            'click .actualizar-excel-registro': 'click_excel',
            'click .actualizar-excel-dosimetria': 'click_excel_dosi',
            'click .actualizar-excel-sono': 'click_excel_sono',
            'click .file-gratis':'file_gratis',
            'click .botton-eliminar-registro': 'action_eliminar_registro',
            'change .fecha_ini':"action_min_date",
            'change .fecha_fin':"action_max_date",
        },
        action_crear_niosh:function(ev){
            var self = this
            var area = $(this.$el).find("input[name='area']").val()
            var puesto_trabajo = $(this.$el).find("input[name='puesto_trabajo']").val()
            var empleado = $(this.$el).find("input[name='empleado']").val()
              var id = parseInt($(this.$el).find("input[name='id']").val())

            rpc.query({
                model:"niosh.niosh",
                method:"create",
                args:[{"registro_id":id,"area":area, "puesto_trabajo":puesto_trabajo, "empleado":empleado}]
            }).then(function(res){
                console.log("CORRECTO")
                location.reload();
            })
        },
        action_crear_registro:function(ev){
            var self = this
            var ruc = $(this.$el).find("input[name='ruc']").val()
            var cliente = $(this.$el).find("input[name='cliente']").val()
            var puntos = $(this.$el).find("input[name='puntos']").val()
            var fecha_ini = $(this.$el).find("input[name='fecha_ini']").val()
            var fecha_fin = $(this.$el).find("input[name='fecha_fin']").val()
            var plan_id = $('#modulo-registro-s3').data("plan_id")

            if(!fecha_ini){
              var fecha_ini = new Date().toISOString().split('T')[0]
            }
            if(!fecha_fin){
              var fecha_fin = new Date().toISOString().split('T')[0]
            }

            rpc.query({
              model: 'monitoreo.transient',
              method: 'limites_permisos',
              args: [1,plan_id],
            }).then(function(output) {
              if (output) {
                rpc.query({
                    model:"registro.monitoreo",
                    method:"create",
                    args:[{"ruc":ruc, "cliente":cliente, "puntos":parseInt(puntos), "fecha_monitoreo":fecha_ini, "fecha_monitoreo_fin":fecha_fin}]
                }).then(function(res){
                    location.reload()
                });
              }
              else {
                swal({
                    title: "Registros de monitoreo",
                    text: "No puede crear más Registros de monitoreo.",
                    icon: "info",
                  });
              }

            });
        },
        action_editar_iluminacion:function(ev){
            var self = this
            var id = parseInt($(this.$el).find("input[name='id']").val())
            var area = $(this.$el).find("input[name='area']").val()
            var puesto_trabajo = $(this.$el).find("input[name='puesto_trabajo']").val()
            var e = document.getElementById("horario_id" + "-" + id)
            var horario = e.options[e.selectedIndex].value
            var d = document.getElementById("tarea_id" + "-" + id)
            var tarea = d.options[d.selectedIndex].value
            var lux = $(this.$el).find("input[name='lux']").val()
            var plan_id = $('.planid').data("plan_id")
            var registro_id = $('.registroid').data("registro_id");

                rpc.query({
                    model:"iluminacion.iluminacion",
                    method:"write",
                    args:[[id],{"area":area, "puesto_trabajo":puesto_trabajo, "horario":horario, "tarea":tarea, "lux":lux}]
                }).then(function(res){
                  rpc.query({
                    model:'registro.monitoreo',
                    method:'datos_ilu',
                    args:[registro_id],
                  }).then(function(){
                    location.reload();
                  });
                })


        },
        action_crear_iluminacion:function(ev){
            var self = this
            var area = $(this.$el).find("input[name='area']").val()
            var puesto_trabajo = $(this.$el).find("input[name='puesto_trabajo']").val()
            var e = document.getElementById("horario_id")
            var horario = e.options[e.selectedIndex].value
            var d = document.getElementById("tarea_id")
            var tarea = d.options[d.selectedIndex].value
            var lux = $(this.$el).find("input[name='lux']").val()
            var id = parseInt($(this.$el).find("input[name='id']").val())
            var counter = parseInt($(this.$el).find("input[name='counter']").val())
            var plan_id = $('.planid').data("plan_id");
            var registro_id = $('.registroid').data("registro_id");
            console.log(plan_id)
            rpc.query({
              model: 'monitoreo.transient',
              method: 'limites_puntos_iluminacion',
              args: [1,plan_id,registro_id],
            }).then(function(output) {
              if (output) {
                $(".botton-crear-ilu").attr("disabled",true)
                rpc.query({
                    model:"iluminacion.iluminacion",
                    method:"create",
                    args:[{"registro_id":id, "area":area, "puesto_trabajo":puesto_trabajo, "horario":horario, "tarea":tarea, "lux":lux}]
                }).then(function(res){
                    rpc.query({
                      model:'registro.monitoreo',
                      method:'datos_ilu',
                      args:[registro_id],
                    }).then(function(){
                      location.reload();
                    });
                })
              }else {
                swal({
                    title: "Registros de monitoreo",
                    text: "No puede crear más puntos de iluminación.",
                    icon: "info",
                  });
              }

            });
        },
        action_eliminar_iluminacion:function(ev){
            var self = this
            var id = parseInt($(this.$el).find("input[name='id']").val())
            var registro_id = $('.registroid').data("registro_id")

            rpc.query({
                model:"iluminacion.iluminacion",
                method:"unlink",
                args:[[id]]
            }).then(function(res){
                rpc.query({
                  model:'registro.monitoreo',
                  method:'datos_ilu',
                  args:[registro_id],
                }).then(function(){
                  location.reload();
                });
            })
        },

        action_editar_dosimetria:function(ev){
            var self = this
            var id = parseInt($(this.$el).find("input[name='id']").val())
            var area = $(this.$el).find("input[name='area']").val()
            var puesto_trabajo = $(this.$el).find("input[name='puesto_trabajo']").val()
            var empleado = $(this.$el).find("input[name='empleado']").val()
            var e = document.getElementById("tarea" + "-" + id)
            var tipo_actividad = e.options[e.selectedIndex].value
            var jornada = $(this.$el).find("input[name='jornada']").val()
            var leq = $(this.$el).find("input[name='leq']").val()
            var plan_id = $('.planid').data("plan_id")
            var registro_id = $('.registroid').data("registro_id")



            rpc.query({
                model:"ruido.dosimetria",
                method:"write",
                args:[[id],{"area":area, "puesto_trabajo":puesto_trabajo, "empleado":empleado, "tipo_actividad":tipo_actividad, "jornada":jornada, "leq":leq}]
            }).then(function(res){
                rpc.query({
                  model:'registro.monitoreo',
                  method:'datos_dosi',
                  args:[registro_id],
                }).then(function(){
                  location.reload();
                });
            })
        },

        action_crear_dosimetria:function(ev){
            var self = this
            var area = $(this.$el).find("input[name='area']").val()
            var puesto_trabajo = $(this.$el).find("input[name='puesto_trabajo']").val()
            var empleado = $(this.$el).find("input[name='empleado']").val()
            var e = document.getElementById("tipo_actividad_id")
            var tipo_actividad = e.options[e.selectedIndex].value
            var jornada = $(this.$el).find("input[name='jornada']").val()
            var leq = $(this.$el).find("input[name='leq']").val()
            var id = parseInt($(this.$el).find("input[name='id']").val())
            var plan_id = $('.planid').data("plan_id")
            var registro_id = $('.registroid').data("registro_id")
            rpc.query({
              model: 'monitoreo.transient',
              method: 'limites_puntos_dosimetria',
              args: [1,plan_id,registro_id],
            }).then(function(output) {
              if (output) {
                rpc.query({
                    model:"ruido.dosimetria",
                    method:"create",
                    args:[{"registro_id":id, "area":area, "puesto_trabajo":puesto_trabajo, "empleado":empleado, "tipo_actividad":tipo_actividad, "jornada":jornada, "leq":leq}]
                }).then(function(res){
                    rpc.query({
                      model:'registro.monitoreo',
                      method:'datos_dosi',
                      args:[registro_id],
                    }).then(function(){
                      location.reload();
                    });
                })
              }else {
                swal({
                    title: "Registros de monitoreo",
                    text: "No puede crear más puntos de dosimetria.",
                    icon: "info",
                  });
              }

              });
        },

        action_eliminar_dosimetria:function(ev){
            var self = this
            var id = parseInt($(this.$el).find("input[name='id']").val())
            var registro_id = $('.registroid').data("registro_id")

            rpc.query({
                model:"ruido.dosimetria",
                method:"unlink",
                args:[[id]]
            }).then(function(res){
                rpc.query({
                  model:'registro.monitoreo',
                  method:'datos_dosi',
                  args:[registro_id],
                }).then(function(){
                  location.reload();
                });
            })
        },

        action_editar_sonometria:function(ev){
            var self = this
            var id = parseInt($(this.$el).find("input[name='id']").val())
            var area = $(this.$el).find("input[name='area']").val()
            var l_min = $(this.$el).find("input[name='l-min']").val()
            var l_max = $(this.$el).find("input[name='l-max']").val()
            var puesto_trabajo = $(this.$el).find("input[name='puesto_trabajo']").val()
            var e = document.getElementById("tarea" + "-" + id)
            var tipo_actividad = e.options[e.selectedIndex].value
            var jornada = $(this.$el).find("input[name='jornada']").val()
            var leq = $(this.$el).find("input[name='leq']").val()

            rpc.query({
                model:"ruido.sonometria",
                method:"write",
                args:[[id],{"area":area, "puesto_trabajo":puesto_trabajo, "tipo_actividad":tipo_actividad, "jornada":jornada, "leq":leq, "l_max":l_max, "l_min":l_min}]
            }).then(function(res){
                console.log("CORRECTO")
                location.reload();
            })
        },

        action_crear_sonometria:function(ev){
            var self = this
            var area = $(this.$el).find("input[name='area']").val()
            var l_min = $(this.$el).find("input[name='l-min']").val()
            var l_max = $(this.$el).find("input[name='l-max']").val()
            var puesto_trabajo = $(this.$el).find("input[name='puesto_trabajo']").val()
            var e = document.getElementById("tipo_actividad_id")
            var tipo_actividad = e.options[e.selectedIndex].value
            var jornada = $(this.$el).find("input[name='jornada']").val()
            var leq = $(this.$el).find("input[name='leq']").val()
            var id = parseInt($(this.$el).find("input[name='id']").val())

            rpc.query({
                model:"ruido.sonometria",
                method:"create",
                args:[{"registro_id":id, "area":area, "puesto_trabajo":puesto_trabajo, "tipo_actividad":tipo_actividad, "jornada":jornada, "leq":leq, "l_max":l_max, "l_min":l_min}]
            }).then(function(res){
                console.log("CORRECTO")
                location.reload();
            })
        },

        action_eliminar_sonometria:function(ev){
            var self = this
            var id = parseInt($(this.$el).find("input[name='id']").val())

            rpc.query({
                model:"ruido.sonometria",
                method:"unlink",
                args:[[id]]
            }).then(function(res){
                console.log("CORRECTO")
                location.reload();
            })
        },
        action_min_date:function(ev){
            var self = this
            var fecha_ini = $(this.$el).find("input[name='fecha_ini']").val()
            var fecha_fin = $(this.$el).find("input[name='fecha_fin']")
            fecha_fin.attr('min',fecha_ini)
        },
        action_max_date:function(ev){
            var self = this
            var fecha_ini = $(this.$el).find("input[name='fecha_ini']")
            var fecha_fin = $(this.$el).find("input[name='fecha_fin']").val()
            fecha_ini.attr('max',fecha_fin)
        },
        click_excel: function(ev) {
          var registro_id = $(ev.target).data("registro_id");
          rpc.query({
            model: 'registro.monitoreo',
            method: 'datos_ilu',
            args: [registro_id],
          }).then(function() {});

        },
        click_excel_dosi: function(ev) {
          var registro_id = $(ev.target).data("registro_id");
          rpc.query({
            model: 'registro.monitoreo',
            method: 'datos_dosi',
            args: [registro_id],
          }).then(function() {});

        },
        click_excel_sono: function(ev) {
          var registro_id = $(ev.target).data("registro_id");
          rpc.query({
            model: 'registro.monitoreo',
            method: 'datos_sono',
            args: [registro_id],
          }).then(function() {});

        },
        file_gratis: function(ev) {
          swal({
            title: "Registro de monitoreo",
            text: "No puede descargar más archivos excel con el plan Gratis.",
            icon: "info",
          });
        },
        action_eliminar_registro: function(ev) {
          var registro_id = $(ev.target).data("registro_id");

          rpc.query({
            model: "registro.monitoreo",
            method: "unlink",
            args: [registro_id]
          }).then(function(res) {
            location.reload();
          });
        },

        action_editar_reba:function(ev){
            var self = this
            var id = parseInt($(this.$el).find("input[name='id']").val())
            var area = $(this.$el).find("input[name='area']").val()
            var puesto_trabajo = $(this.$el).find("input[name='puesto_trabajo']").val()
            var empleado = $(this.$el).find("input[name='empleado']").val()

            rpc.query({
                model:"reba.reba",
                method:"write",
                args:[[id],{"area":area, "puesto_trabajo":puesto_trabajo, "empleado":empleado}]
            }).then(function(res){
                console.log("CORRECTO")
                location.reload();
            })
        },

        action_crear_reba:function(ev){
            var self = this
            var area = $(this.$el).find("input[name='area']").val()
            var puesto_trabajo = $(this.$el).find("input[name='puesto_trabajo']").val()
            var empleado = $(this.$el).find("input[name='empleado']").val()
              var id = parseInt($(this.$el).find("input[name='id']").val())

            rpc.query({
                model:"reba.reba",
                method:"create",
                args:[{"registro_id":id,"area":area, "puesto_trabajo":puesto_trabajo, "empleado":empleado}]
            }).then(function(res){
                console.log("CORRECTO")
                location.reload();
            })
        },

        action_crear_rosa:function(ev){
            var self = this
            var area = $(this.$el).find("input[name='area']").val()
            var puesto_trabajo = $(this.$el).find("input[name='puesto_trabajo']").val()
            var empleado = $(this.$el).find("input[name='empleado']").val()
              var id = parseInt($(this.$el).find("input[name='id']").val())

            rpc.query({
                model:"rosa.rosa",
                method:"create",
                args:[{"registro_id":id,"area":area, "puesto_trabajo":puesto_trabajo, "empleado":empleado}]
            }).then(function(res){
                console.log("CORRECTO")
                location.reload();
            })
        },

        action_eliminar_reba:function(ev){
            var self = this
            var id = parseInt($(this.$el).find("input[name='id']").val())

            rpc.query({
                model:"reba.reba",
                method:"unlink",
                args:[[id]]
            }).then(function(res){
                console.log("CORRECTO")
                location.reload();
            })
        },





    })

    publicWidget.registry.FormEditableSaveReba = publicWidget.Widget.extend({
      selector:"#formulario_editar_field_reba",
      events:{
            'click .botton-guardar-field-data':"action_guardar_field_data",
            "change #image_input":"click_image_input",
            "change .field-odoo":"click_change_field",
      },
      click_change_field: async function(ev){
        var form = $('#formulario_editar_field_reba');
        var puntuacion_a = 0;
        var tronco = 0;
        var cuello = 0;
        var piernas = 0;
        var flexion_tronco = $("input[name='flexion_tronco']").val();
        var flexion_tronco_texto = "";
        var extension_tronco = $("input[name='extension_tronco']").val();
        var extension_tronco_texto = "";
        var flexion_cuello = $("input[name='flexion_cuello']").val();
        var flexion_cuello_texto = "";
        var extension_cuello = $("input[name='extension_cuello']").val();
        var extension_cuello_texto = "";
        var soporte_pie = $("input[name='soporte_pie']").val();
        var soporte_pie_texto = "";
        var flexion_rodilla = $("input[name='flexion_rodilla']").val();
        var flexion_rodilla_texto = "";

        console.log(tronco);

        var puntuacion_b = 0;
        var brazo = 0;
        var antebrazo = 0;
        var muneca = 0;
        var extension_brazo = $("input[name='extension_brazo']").val();
        var extension_brazo_texto = "";
        var correccion_brazo = $("input[name='correccion_brazo']").val();
        var correccion_brazo_texto = "";
        var extension_antebrazo = $("input[name='extension_antebrazo']").val();
        var extension_antebrazo_texto = "";
        var extension_muneca = $("input[name='extension_muneca']").val();
        var extension_muneca_texto = "";
        var torsion_muneca = $("input[name='torsion_muneca']").val();
        var torsion_muneca_texto = "";


        var puntuacion_c = 0;
        var fuerza_carga = 0;
        var cantidad_carga = $("input[name='cantidad_carga']").val();
        var cantidad_carga_texto = "";
        var fuerza_brusca = $("input[name='fuerza_brusca']").val();
        var fuerza_brusca_texto = "";
        var agarre = 0;
        var agarre_tipo = $("input[name='agarre_tipo']").val();
        var agarre_tipo_texto = "";
        var agarre_tipo_texto_1 = "";
        var acti_muscular = 0;
        var tip_muscu = $("input[name='tip_muscu']").is(":checked");
        var tip_muscu_1 = $("input[name='tip_muscu_1']").is(":checked");
        var tip_muscu_2 = $("input[name='tip_muscu_2']").is(":checked");

        var puntuacion = 0;
        var nivel_riesgo = "";
        var nivel_actuacion = 0;
        var cumple = "";


        if (flexion_tronco < 1 || flexion_tronco > 4)
  			   {flexion_tronco = 1;
           }
  			if (extension_tronco < 0 || extension_tronco > 2)
  				{extension_tronco = 0;}
  			if (flexion_cuello < 1 || flexion_cuello > 2)
  			   {	flexion_cuello = 1;}
  			if (extension_cuello < 0 || extension_cuello > 2)
  				{extension_cuello = 0;}
  			if (soporte_pie < 1 || soporte_pie > 2)
  			   {soporte_pie = 1;}
  			if (flexion_rodilla < 0 || flexion_rodilla > 2)
  			   {flexion_rodilla = 0;}

         if (extension_brazo < 1 || extension_brazo > 4)
   				extension_brazo = 1;
   			if (correccion_brazo < -1 || correccion_brazo > 1)
   				correccion_brazo = 0;
   			if (extension_antebrazo < 1 || extension_antebrazo > 2)
   				extension_antebrazo = 1;
   			if (extension_muneca < 0 || extension_muneca > 2)
   				extension_muneca = 0;
   			if (torsion_muneca < 0 || torsion_muneca > 2)
   				torsion_muneca = 0;

          if (cantidad_carga < 0 || cantidad_carga > 2)
    				{cantidad_carga = 0;}
    			if (fuerza_brusca < 0 || fuerza_brusca > 2)
    				{fuerza_brusca = 0;}
    			if (agarre_tipo < 0 || agarre_tipo > 3)
    				{agarre_tipo = 0;}

            if (flexion_tronco == 0)
      				{flexion_tronco_texto = "";}

      			if (flexion_tronco >= 1 && extension_tronco >= 0)
            {
      				if (flexion_tronco == 1){
                  flexion_tronco_texto = "Tronco Erguido";
                }
      				else if (flexion_tronco == 2)
      					{flexion_tronco_texto = "Flexión o Extensión entre 0° y 20°";}
      				else if (flexion_tronco == 3)
      					{flexion_tronco_texto = "Flexión  >20° y ≤60° o Extensión >20°";}
      				else if (flexion_tronco == 4)
      					{flexion_tronco_texto = "Flexión >60°";}

      				if (extension_tronco == 0)
      					{ extension_tronco_texto = "No";}
      				else if (extension_tronco > 0)
      					{extension_tronco_texto = "Sí";}

      				tronco = Number(flexion_tronco)  + Number(extension_tronco);
              }
      			if (flexion_cuello == 0)
      				{flexion_cuello_texto = "";}
      			if (flexion_cuello >= 1 && extension_cuello >= 0)
            {
      				if (flexion_cuello == 1)
      					{flexion_cuello_texto = "Flexión entre 0° y 20°";}
      				else if (flexion_cuello == 2)
      					{flexion_cuello_texto = "Flexión  >20° o Extensión";}

      				if (extension_cuello == 0)
      					{extension_cuello_texto = "No";}
      				else if (extension_cuello > 0)
      					{extension_cuello_texto = "Sí";}

      				cuello =  Number(extension_cuello) + Number(flexion_cuello);
              }
      			if (soporte_pie == 0)
      				{soporte_pie_texto = "Sentado, Andando o de Pie con Soporte Bilateral Simétrico";}

      			if (soporte_pie >= 1 && flexion_rodilla >= 0)
      				{if (soporte_pie == 1)
      					{soporte_pie_texto = "Sentado, Andando o de Pie con Soporte Bilateral Simétrico";}
      				else if (soporte_pie == 2)
      					{soporte_pie_texto = "De Pie con Soporte Unilateral, Soporte Ligero o Postura Inestable";}

      				if (flexion_rodilla == 0)
      					{flexion_rodilla_texto = "No Presenta Flexión de Rodillas";}
      				else if (flexion_rodilla == 1)
      					{flexion_rodilla_texto = "Flexión de una o ambas Rodillas entre 30 y 60°";}
      				else if (flexion_rodilla == 2)
      					{flexion_rodilla_texto = "Flexión de una o ambas rodillas de más de 60° (salvo postura sedente)";}

      				piernas = Number(soporte_pie) + Number(flexion_rodilla);
              }
      			if (cantidad_carga >= 0 && fuerza_brusca >= 0)
      				{
              fuerza_carga = Number(cantidad_carga) + Number(fuerza_brusca);

      				if (cantidad_carga == 0)
      					{cantidad_carga_texto = "Carga o fuerza menor de 5 Kg.";}
      				else if (cantidad_carga == 1)
      					{cantidad_carga_texto = "Carga o fuerza entre 5 y 10 Kg.";}
      				else if (cantidad_carga == 2)
      					{cantidad_carga_texto = "Carga o fuerza mayor de  10 Kg.";}

      				if (fuerza_brusca == 0)
      					{fuerza_brusca_texto = "No";}
      				else if (fuerza_brusca > 0)
      					{fuerza_brusca_texto = "Sí";}
              }
      			// # puntuacion A
      			if (tronco == 1)
      				{if (cuello == 1 || cuello == 2)
      					{if (piernas == 1)
      						{puntuacion_a = 1 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 2 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 3 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 4 + fuerza_carga;}
                }
      				else if (cuello == 3)
      					{if (piernas == 1)
      						{puntuacion_a = 3 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 3 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 5 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 6 + fuerza_carga;}
                }
              }
      			if (tronco == 2)
      				{if (cuello == 1)
      					{if (piernas == 1)
      						{puntuacion_a = 2 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 3 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 4 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 5 + fuerza_carga;}
                }
      				else if (cuello == 2)
      					{if (piernas == 1)
      						{puntuacion_a = 3 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 4 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 5 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 6 + fuerza_carga;}
                }
      				else if (cuello == 3)
      					{if (piernas == 1)
      						{puntuacion_a = 4 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 5 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 6 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 7 + fuerza_carga;}
                }
              }
      			if (tronco == 3)
      				{if (cuello == 1)
      					{if (piernas == 1)
      						{puntuacion_a = 2 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 4 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 5 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 6 + fuerza_carga;}
                }
      				else if (cuello == 2)
      					{if (piernas == 1)
      						{puntuacion_a = 4 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 5 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 6 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 7 + fuerza_carga;}
                }
      				else if (cuello == 3)
      					{if (piernas == 1)
      						{puntuacion_a = 5 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 6 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 7 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 8 + fuerza_carga;}
                }
              }
      			if (tronco == 4)
      				{if (cuello == 1)
      					{if (piernas == 1)
      						{puntuacion_a = 3 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 5 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 6 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 7 + fuerza_carga;}
                }
      				else if (cuello == 2)
      					{if (piernas == 1)
      						{puntuacion_a = 5 + fuerza_carga;}
      					else if (piernas == 2)
      					  {puntuacion_a = 6 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 7 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 8 + fuerza_carga;}
                }
      				else if (cuello == 3)
      					{if (piernas == 1)
      						{puntuacion_a = 6 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 7 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 8 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 9 + fuerza_carga;}
                }
              }
      			if (tronco == 5)
      				{if (cuello == 1)
      					{if (piernas == 1)
      						{puntuacion_a = 4 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 6 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 7 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 8 + fuerza_carga;}
                }
      				else if (cuello == 2)
      					{if (piernas == 1)
      						{puntuacion_a = 6 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 7 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 8 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 9 + fuerza_carga;}
                }
      				else if (cuello == 3)
      					{if (piernas == 1)
      						{puntuacion_a = 7 + fuerza_carga;}
      					else if (piernas == 2)
      						{puntuacion_a = 8 + fuerza_carga;}
      					else if (piernas == 3)
      						{puntuacion_a = 9 + fuerza_carga;}
      					else if (piernas == 4)
      						{puntuacion_a = 9 + fuerza_carga;}
                }
              }

      			if (agarre_tipo >= 0)
      				{agarre = agarre_tipo;
      				if (agarre_tipo == 0)
      					{agarre_tipo_texto = "Bueno";
      					agarre_tipo_texto_1 = "El agarre es bueno y la fuerza de agarre de rango medio";}
      				else if (agarre_tipo == 1)
      				{	agarre_tipo_texto = "Regular";
      					agarre_tipo_texto_1 = "El agarre es aceptable pero no ideal o el agarre es aceptable utilizando otras partes del cuerpo";}
      				else if (agarre_tipo == 2)
      					{agarre_tipo_texto = "Malo";
      					agarre_tipo_texto_1 = "El agarre es posible pero no aceptable";}
      				else if (agarre_tipo == 3)
      				{	agarre_tipo_texto = "Inaceptable";
      					agarre_tipo_texto_1 = "El agarre es torpe e inseguro, no es posible el agarre manual o el agarre es inaceptable utilizando otras partes del cuerpo";}
            }

      			if (extension_brazo == 0)
      				{extension_brazo_texto = "";}
      			if (extension_brazo >= 1 && correccion_brazo >= 0)
      				{brazo = Number(extension_brazo) + Number(correccion_brazo);
      				if (extension_brazo == 1)
      					{extension_brazo_texto = "Desde 20° de Extensión a 20° de Flexión";}
      				else if (extension_brazo == 2)
      					{extension_brazo_texto = "Extensión >20° o Flexión >20° y <45°";}
      				else if (extension_brazo == 3)
      					{extension_brazo_texto = "Flexión >45° y 90°";}
      				else if (extension_brazo == 4)
      					{extension_brazo_texto = "Flexión >90°";}

      				if (correccion_brazo == 0)
      					{correccion_brazo_texto = "No Presenta Correcciones";}
      				else if (correccion_brazo == 1)
      					{correccion_brazo_texto = "Brazo Abducido, Brazo Rotado u Hombro Elevado";}
      				else if (correccion_brazo == -1)
      					{correccion_brazo_texto = "Existe un Punto de Apoyo o la Postura a Favor de la Gravedad";}
              }
      			if (extension_antebrazo == 0)
      				{extension_antebrazo_texto = "";}

      			if (extension_antebrazo >= 1)
      				{antebrazo = extension_antebrazo;
      				if (extension_antebrazo == 1)
      					{extension_antebrazo_texto = "Flexión entre 60° y 100°";}
      				else if (extension_antebrazo == 2)
      					{extension_antebrazo_texto = "Flexión <60° o >100°";}
              }
      			if (extension_muneca == 0)
      				{extension_muneca_texto = "Posición neutra";}
      			if (extension_muneca >= 1 && torsion_muneca >= 0)
      				{muneca = Number(extension_muneca) + Number(torsion_muneca);

      				if (extension_muneca == 1)
      					{extension_muneca_texto = "Flexión o extensión > 0° y <15°";}
      				else if (extension_muneca == 2)
      					{extension_muneca_texto = "Flexión o extensión >15°";}

      				if (torsion_muneca == 0)
      					{torsion_muneca_texto = "No";}
      				else if (torsion_muneca > 0)
      					{torsion_muneca_texto = "Sí";}
            }
      			// # puntuacion B
      			if (brazo == 1)
      				{if (antebrazo == 1)
      					{if (muneca == 1)
      						{puntuacion_b = 1 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 2 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 2 + Number(agarre);}
                }
      				else if (antebrazo == 2)
      					{if (muneca == 1)
      						{puntuacion_b = 1 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 2 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 3 + Number(agarre);}
                }
              }
      			else if (brazo == 2)
      				{if (antebrazo == 1)
      					{if (muneca == 1)
      					  {puntuacion_b = 1 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 2 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 3 + Number(agarre);}
                }
      				else if (antebrazo == 2)
      					{if (muneca == 1)
      						{puntuacion_b = 2 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 3 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 4 + Number(agarre);}
                }
              }
      			if (brazo == 3)
      				{if (antebrazo == 1)
      					{if (muneca == 1)
      						{puntuacion_b = 3 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 4 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 5 + Number(agarre);}
                }
      				else if (antebrazo == 2)
      					{if (muneca == 1)
      						{puntuacion_b = 4 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 5 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 5 + Number(agarre);}
                }
              }
      			if (brazo == 4)
      				{if (antebrazo == 1)
      					{if (muneca == 1)
      						{puntuacion_b = 4 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 5 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 5 + Number(agarre);}
                }
      				else if (antebrazo == 2)
      					{if (muneca == 1)
      						{puntuacion_b = 5 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 6 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 7 + Number(agarre);}
                }
              }
      			if (brazo == 5)
      				{if (antebrazo == 1)
      					{if (muneca == 1)
      						{puntuacion_b = 6 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 7 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 8 + Number(agarre);}
                }
      				else if (antebrazo == 2)
      					{if (muneca == 1)
      						{puntuacion_b = 7 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 8 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 8 + Number(agarre);}
                }
              }
      			if (brazo == 6)
      				{if (antebrazo == 1)
      					{if (muneca == 1)
      						{puntuacion_b = 7 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 8 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 8 + Number(agarre);}
                }
      				else if (antebrazo == 2)
      				{	if (muneca == 1)
      						{puntuacion_b = 8 + Number(agarre);}
      					else if (muneca == 2)
      						{puntuacion_b = 9 + Number(agarre);}
      					else if (muneca == 3)
      						{puntuacion_b = 9 + Number(agarre);}
              }
            }
      			var cont = 0;
      			if (tip_muscu)
      				{cont = cont + 1;}
      			if (tip_muscu_1)
      				{cont = cont + 1;}
      			if (tip_muscu_2)
      				{cont = cont + 1;}

      			acti_muscular = cont;
      			puntuacion = 1;

            puntuacion = 1
      			if (puntuacion_a == 1)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 1;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 1;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 1;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 2;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 3;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 3;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 4;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 5;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 6;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 7;}
              }
      			else if (puntuacion_a == 2)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 1;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 2;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 2;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 3;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 4;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 4;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 5;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 6;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 6;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 8;}
              }
      			if (puntuacion_a == 3)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 2;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 3;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 3;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 3;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 4;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 5;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 6;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 8;}
              }
      			if (puntuacion_a == 4)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 3;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 4;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 4;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 4;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 5;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 6;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 9;}
              }
      			if (puntuacion_a == 5)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 4;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 4;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 4;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 5;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 6;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 9;}
              }
      			if (puntuacion_a == 6)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 6;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 6;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 6;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 10;}}
      			if (puntuacion_a == 7)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 7;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 11;}}
      			if (puntuacion_a == 8)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 8;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 11;}}
      			if (puntuacion_a == 9)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 9;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 12;}}
      			if (puntuacion_a == 10)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 10;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 12;}}
      			if (puntuacion_a == 11)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 11;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 12)
      					{puntuacion_c = 12;}
              }
      			if (puntuacion_a == 12)
      				{if (puntuacion_b == 1)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 2)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 3)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 4)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 5)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 6)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 7)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 8)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 9)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 10)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 11)
      					{puntuacion_c = 12;}
      				else if (puntuacion_b == 12)
      				{	puntuacion_c = 12;}
            }

      			puntuacion = Number(puntuacion_c) + Number(acti_muscular);

      			if (puntuacion == 1)
      				{nivel_riesgo = "INAPRECIABLE";
      				nivel_actuacion = 0;
      				cumple = "SI CUMPLE";}
      			else if (puntuacion == 2)
      				{nivel_riesgo = "BAJO";
      				nivel_actuacion = 1;
      				cumple = "SI CUMPLE";}
      			else if (puntuacion == 3)
      				{nivel_riesgo = "BAJO";
      				nivel_actuacion = 1;
      				cumple = "SI CUMPLE";}
      			else if (puntuacion == 4)
      				{nivel_riesgo = "MEDIO";
      				nivel_actuacion = 2;
      				cumple = "SI CUMPLE";}
      			else if (puntuacion == 5)
      				{nivel_riesgo = "MEDIO";
      				nivel_actuacion = 2;
      				cumple = "SI CUMPLE";}
      			else if (puntuacion == 6)
      				{nivel_riesgo = "MEDIO";
      				nivel_actuacion = 2;
      				cumple = "SI CUMPLE";}
      			else if (puntuacion == 7)
      				{nivel_riesgo = "MEDIO";
      				nivel_actuacion = 2;
      				cumple = "SI CUMPLE";}
      			else if (puntuacion == 8)
      				{nivel_riesgo = "ALTO";
      				nivel_actuacion = 3;
      				cumple = "NO CUMPLE";}
      			else if (puntuacion == 9)
      				{nivel_riesgo = "ALTO";
      				nivel_actuacion = 3;
      				cumple = "NO CUMPLE";}
      			else if (puntuacion == 10)
      				{nivel_riesgo = "ALTO";
      				nivel_actuacion = 3;
      				cumple = "NO CUMPLE";}
      			else if (puntuacion == 11)
      				{nivel_riesgo = "MUY ALTO";
      				nivel_actuacion = 4;
      				cumple = "NO CUMPLE";}
      			else if (puntuacion == 12)
      				{nivel_riesgo = "MUY ALTO";
      				nivel_actuacion = 4;
      				cumple = "NO CUMPLE";}
      			else if (puntuacion == 13)
      				{nivel_riesgo = "MUY ALTO";
      				nivel_actuacion = 4;
      				cumple = "NO CUMPLE";}
      			else if (puntuacion == 14)
      				{nivel_riesgo = "MUY ALTO";
      				nivel_actuacion = 4;
      				cumple = "NO CUMPLE";}
      			else if (puntuacion == 15)
      				{nivel_riesgo = "MUY ALTO";
      				nivel_actuacion = 4;
      				cumple = "NO CUMPLE";}

          $("span[name='puntuacion_a']").text(puntuacion_a);
          $("span[name='tronco']").text(tronco);
          $("span[name='cuello']").text(cuello);
          $("span[name='piernas']").text(piernas);
          $("span[name='flexion_tronco_texto']").text(flexion_tronco_texto);
          $("span[name='extension_tronco_texto']").text(extension_tronco_texto);
          $("span[name='flexion_cuello_texto']").text(flexion_cuello_texto);
          $("span[name='soporte_pie_texto']").text(soporte_pie_texto);
          $("span[name='flexion_rodilla_texto']").text(flexion_rodilla_texto);
          $("span[name='puntuacion_b']").text(puntuacion_b);
          $("span[name='brazo']").text(brazo);
          $("span[name='antebrazo']").text(antebrazo);
          $("span[name='muneca']").text(muneca);
          $("span[name='extension_brazo_texto']").text(extension_brazo_texto);
          $("span[name='correccion_brazo_texto']").text(correccion_brazo_texto);
          $("span[name='extension_antebrazo_texto']").text(extension_antebrazo_texto);
          $("span[name='extension_muneca_texto']").text(extension_muneca_texto);
          $("span[name='torsion_muneca_texto']").text(torsion_muneca_texto);
          $("span[name='puntuacion_c']").text(puntuacion_c);
          $("span[name='fuerza_carga']").text(fuerza_carga);
          $("span[name='cantidad_carga_texto']").text(cantidad_carga_texto);
          $("span[name='fuerza_brusca_texto']").text(fuerza_brusca_texto);
          $("span[name='agarre']").text(agarre);
          $("span[name='agarre_tipo_texto']").text(agarre_tipo_texto);
          $("span[name='agarre_tipo_texto_1']").text(agarre_tipo_texto_1);
          $("span[name='acti_muscular']").text(acti_muscular);
          $("span[name='puntuacion']").text(puntuacion);
          $("span[name='nivel_riesgo']").text(nivel_riesgo);
          $("span[name='nivel_actuacion']").text(nivel_actuacion);
          $("span[name='cumple']").text(cumple);
          $("img[name='flexion_tronco']").attr('src',"/s3/static/description/reba/tronco/tronco_"  + flexion_tronco + ".jpeg");
          $("img[name='flexion_cuello']").attr('src',"/s3/static/description/reba/cuello/cuello_"  + flexion_cuello + ".jpeg");
          $("img[name='soporte_pie']").attr('src',"/s3/static/description/reba/piernas/piernas_"  + soporte_pie + ".jpeg");
          $("img[name='extension_brazo']").attr('src',"/s3/static/description/reba/brazo/brazo_"  + extension_brazo + ".jpeg");
          $("img[name='extension_antebrazo']").attr('src',"/s3/static/description/reba/antebrazo/antebrazo_"  + extension_antebrazo + ".jpeg");
          $("img[name='extension_muneca']").attr('src',"/s3/static/description/reba/muneca/muneca_"  + extension_muneca + ".jpeg");
      },
      action_guardar_field_data: async function(ev){
          var form = $('#formulario_editar_field_reba');
          var model = $('#formulario_editar_field_reba').data("model_id");
          var record_id = $('#formulario_editar_field_reba').data("record_id");
          var dict = []
          $("input[class='field-odoo']", form).each(async function(){
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
            location.reload()

        })

      },
      click_image_input:async function(ev){
        var e =  $(ev.target);
        var record_id = $('#formulario_editar_field_reba').data("record_id");
        for (var i = 0; i < e.length; i++) {
            $( ".image_file_input" ).remove();
           var file = e[0].files[0];
           var img = document.createElement("img");
           var reader = new FileReader();
           var binary = "aaa";
           img.className = "image_file_input";
           reader.onloadend = async function() {
                img.src = reader.result;
                console.log(reader.result)
                var dataType = reader.result.split(';base64,')[1];
                console.log(dataType)
                await rpc.query({
                    model:"reba.reba",
                    method:"write",
                    args:[[record_id],{"imagen":dataType}]
                }).then(function(res){
                });
           }
           reader.readAsDataURL(file);
           $(ev.target).after(img);
          }
          console.log(e);

      },


    })

})
