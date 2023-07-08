odoo.define("registro_accidente", function(require) {
      'use strict';

      var publicWidget = require("web.public.widget");
      var rpc = require("web.rpc");
      var core = require('web.core');
      var QWeb = core.qweb;
      var _t = core._t;

      publicWidget.registry.CrearRegistro = publicWidget.Widget.extend({
        selector: ".list-registro-accidente",
        events: {
          'click .botton-registro-accidente': 'click_nuevo_registro_accidente',
          'click .file-gratis': 'file_gratis',
    			'click .botton-eliminar-registro-accidente': 'click_eliminar_accidente',
        },
        file_gratis: function(ev) {
          swal({
            title: "REGISTRO DE ACCIDENTE",
            text: "No puede descargar más archivos excel con el plan Gratis.",
            icon: "info",
          });
        },
    		click_eliminar_accidente: function(ev){
    			var evento = $(ev.currentTarget)
    			var registro_id = evento.data("registro_id")
    			rpc.query({
    				model: "registro.accidente",
    				method: "unlink",
    				args: [registro_id],
    			}).then(function(res) {
    				location.reload();
    			});
    		},
        click_nuevo_registro_accidente: function(ev) {
          var fecha = $(this.$el).find("input[name='new-registro-fecha']").val()
          var razon = $(this.$el).find("input[name='new-registro-razon']").val()
          var lugar = $(this.$el).find("input[name='new-registro-lujar']").val()
          var empresa = $(".list-registro-accidente").data("empresa_id");
          var plan_id = $('#modulo-registro-accidente').data("plan_id");

          // rpc.query({
          //   model: 'edit.linea.accidente',
          //   method: 'limites_permisos',
          //   args: [1, plan_id],
          // }).then(function(output) {
            // console.log(output);
            // if (output) {
              rpc.query({
                model: 'registro.accidente',
                method: 'create',
                args: [{
                  "fecha": fecha,
                  "razon_social": razon,
                  "empresa_id": empresa,
                  "lugar": lugar,
                }],
              }).then(function() {
                location.reload();

              });
            // } else {
            //   swal({
            //     title: "Registro De Accidente",
            //     text: "No puede crear más REGISTROS DE ESTADÍSTICAS DE ACCIDENTES.",
            //     icon: "info",
            //   });
            // }

          // });

        },
      })

      publicWidget.registry.EditLineaId = publicWidget.Widget.extend({
        selector: ".change-linea",
        events: {
          'change .linea-accidente': 'click_edit_registro_accidente',
        },
        click_edit_registro_accidente: function(ev) {
          var linea_id = $(ev.target).data("linea_id");
          var registro_id = $(".form-registro-accidente").data("registro_id");
          var field = $(ev.target).attr('name')
          var valor = $(ev.target).val();
          rpc.query({
            model: 'edit.linea.accidente',
            method: 'gruardar_linea',
            args: [1, linea_id, field, valor],
          }).then(function(output) {
            $("input[name='indice_frecuencia'][data-linea_id='" + linea_id + "']").val(output[0]);
            $("input[name='indice_gravedad'][data-linea_id='" + linea_id + "']").val(output[1]);
            $("input[name='indice_accidentabilidad'][data-linea_id='" + linea_id + "']").val(output[2]);
            rpc.query({
              model: 'registro.accidente',
              method: 'open_word_frio',
              args: [registro_id],
            }).then(function() {});
          });

        },
      })



      publicWidget.registry.Graph = publicWidget.Widget.extend({
          selector: ".graph-registro-accidente",
          events: {
            'click .select-dom': 'click_excel',
          },
          jsLibs: [
            '/web/static/lib/Chart/Chart.js',
          ],
          init: function() {
            this._super.apply(this, arguments);
          },
          click_excel: function(ev) {
            var empresa = $(".graph-registro-accidente").data("empresa_id");
            var value = $(".select-dom").val();
            if (value == 1) {
              rpc.query({
                model: 'edit.linea.accidente',
                method: 'get_data',
                args: [1, empresa],
              }).then(function(output) {
                $('#bar-chart').replaceWith($('<canvas id="bar-chart" width="800" height="450"></canvas>'));
                new Chart(document.getElementById("bar-chart"), {
                  type: 'bar',
                  data: {
                    labels: ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"],
                    datasets: [{
                      label: "N°",
                      backgroundColor: ["#F75448", "#7AD61D", "#8A2BE2", "#5F9EA0", "#D2691E", "#006400", "#FF8C00", "#9932CC", "#2F4F4F", "#00BFFF", "#696969", "#228B22"],
                      data: output
                    }]
                  },
                  options: {
                    legend: {
                      display: false
                    },
                    title: {
                      display: true,
                      text: 'N° ACCIDENTES MORTALES'
                    }
                  }
                });
              });
            }
            if (value == 2) {
              rpc.query({
                model: 'edit.linea.accidente',
                method: 'get_data_1',
                args: [1, empresa],
              }).then(function(output) {
                $('#bar-chart').replaceWith($('<canvas id="bar-chart" width="800" height="450"></canvas>'));

                new Chart(document.getElementById("bar-chart"), {
                  type: 'bar',
                  data: {
                    labels: ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"],
                    datasets: [{
                      label: "N°",
                      backgroundColor: ["#F75448", "#7AD61D", "#8A2BE2", "#5F9EA0", "#D2691E", "#006400", "#FF8C00", "#9932CC", "#2F4F4F", "#00BFFF", "#696969", "#228B22"],
                      data: output
                    }]
                  },
                  options: {
                    legend: {
                      display: false
                    },
                    title: {
                      display: true,
                      text: 'N° ACCIDENTE DE TRABAJO LEVE'
                    }
                  }
                });
              });
            }
            if (value == 3) {
              rpc.query({
                model: 'edit.linea.accidente',
                method: 'get_data_2',
                args: [1, empresa],
              }).then(function(output) {
                $('#bar-chart').replaceWith($('<canvas id="bar-chart" width="800" height="450"></canvas>'));

                new Chart(document.getElementById("bar-chart"), {
                  type: 'bar',
                  data: {
                    labels: ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"],
                    datasets: [{
                      label: "N°",
                      backgroundColor: ["#F75448", "#7AD61D", "#8A2BE2", "#5F9EA0", "#D2691E", "#006400", "#FF8C00", "#9932CC", "#2F4F4F", "#00BFFF", "#696969", "#228B22"],
                      data: output
                    }]
                  },
                  options: {
                    legend: {
                      display: false
                    },
                    title: {
                      display: true,
                      text: 'N° ACCIDENTES DE TRABAJO INCAPACITANTES'
                    }
                  }
                });
              });
            }
            if (value == 4) {
              rpc.query({
                model: 'edit.linea.accidente',
                method: 'get_data_3',
                args: [1, empresa],
              }).then(function(output) {
                $('#bar-chart').replaceWith($('<canvas id="bar-chart" width="800" height="450"></canvas>'));

                new Chart(document.getElementById("bar-chart"), {
                  type: 'bar',
                  data: {
                    labels: ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"],
                    datasets: [{
                      label: "N°",
                      backgroundColor: ["#F75448", "#7AD61D", "#8A2BE2", "#5F9EA0", "#D2691E", "#006400", "#FF8C00", "#9932CC", "#2F4F4F", "#00BFFF", "#696969", "#228B22"],
                      data: output
                    }]
                  },
                  options: {
                    legend: {
                      display: false
                    },
                    title: {
                      display: true,
                      text: 'N° ENFERMEDAD OCUPACIONAL'
                    }
                  }
                });
              });
            }
            if (value == 5) {
              rpc.query({
                model: 'edit.linea.accidente',
                method: 'get_data_4',
                args: [1, empresa],
              }).then(function(output) {
                $('#bar-chart').replaceWith($('<canvas id="bar-chart" width="800" height="450"></canvas>'));

                new Chart(document.getElementById("bar-chart"), {
                  type: 'bar',
                  data: {
                    labels: ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"],
                    datasets: [{
                      label: "N°",
                      backgroundColor: ["#F75448", "#7AD61D", "#8A2BE2", "#5F9EA0", "#D2691E", "#006400", "#FF8C00", "#9932CC", "#2F4F4F", "#00BFFF", "#696969", "#228B22"],
                      data: output
                    }]
                  },
                  options: {
                    legend: {
                      display: false
                    },
                    title: {
                      display: true,
                      text: 'N° INCIDENTES PELIGROSOS'
                    }
                  }
                });
              });
            }
            if (value == 6) {
              rpc.query({
                model: 'edit.linea.accidente',
                method: 'get_data_5',
                args: [1, empresa],
              }).then(function(output) {
                $('#bar-chart').replaceWith($('<canvas id="bar-chart" width="800" height="450"></canvas>'));

                new Chart(document.getElementById("bar-chart"), {
                  type: 'bar',
                  data: {
                    labels: ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"],
                    datasets: [{
                      label: "N°",
                      backgroundColor: ["#F75448", "#7AD61D", "#8A2BE2", "#5F9EA0", "#D2691E", "#006400", "#FF8C00", "#9932CC", "#2F4F4F", "#00BFFF", "#696969", "#228B22"],
                      data: output
                    }]
                  },
                  options: {
                    legend: {
                      display: false
                    },
                    title: {
                      display: true,
                      text: 'N° INCIDENTES'
                    }
                  }
                });
              });
            }
          },
        })

      })
