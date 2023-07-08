odoo.define("iperc_continuo.continuo", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb


  publicWidget.registry.Crearcontinuo = publicWidget.Widget.extend({
    selector: ".iperc-continuo",
    events: {
      'click .nuevo-continuo': 'click_nuevo_continuo',
      'click .nuevo-trabajador': 'click_nuevo_trabajador',
      'click .nuevo-riesgo': 'click_nuevo_riesgo',
      'click .nueva-secuencia': 'click_nueva_secuencia',
      'click .nuevo-supervisor': 'click_nuevo_supervisor',
      'click .botton-eliminar-continuo': 'eliminar_continuo',
      'change .evaluacion': 'change_evaluacion',
      'change .riesgo': 'change_riesgo',
      'change .evaluacion_riesgo': 'evaluacion_riesgo',
      'change .evaluacion_riesgo': 'evaluacion_riesgo',
      'change .change_secuencia': 'change_secuencia',
      'change .change_trabajadores': 'change_trabajadores',
      'change .change_supervisor': 'change_supervisor',
      'change .select_tipo': 'select_tipo',
      'change .select_descripcion': 'select_descripcion',
      'click .botton-eliminar-supervisor': 'action_eliminar_supervisor',
      'change .tipo_peligro': 'tipo_peligro',
      'keyup input.evaluacion_riesgo': "evaluacion_riesgo_key",
      'click .nuevo-tipo-peligro': "nuevo_tipo_peligro",
      'click .tipo_id': "eliminar_tipo",
      'click .agregar_descripcion': "agregar_descripcion",
      'click .descripcion_id': "eliminar_descripcion",
      'click .print_report': "print_report",
    },
    eliminar_continuo: function(ev){
      var evento = $(ev.currentTarget)
      var continuo_id = evento.data("continuo_id")
      rpc.query({
        model: "iperc.continuo",
        method: "unlink",
        args: [continuo_id],
      }).then(function(res) {
        location.reload();
      });
    },
    click_nuevo_continuo: function(ev) {
      var ruc = $(this.$el).find("input[name='new-continuo-ruc']").val()
      var empresa = $(this.$el).find("input[name='new-continuo-empresa']").val()
      var sede = $(this.$el).find("input[name='new-continuo-sede']").val()
      var plan_id = $('#modulo-iperc-continuo').data("plan_id");
      // rpc.query({
      //   model: 'continuo.transient',
      //   method: 'limites_permisos',
      //   args: [1, plan_id],
      // }).then(function(output) {
      //   if (output) {
      $(".nuevo-continuo").attr("disabled", true)
      rpc.query({
        model: 'iperc.continuo',
        method: 'create',
        args: [{
          "ruc": ruc,
          "cliente": empresa,
          "sede": sede
        }],
      }).then(function() {
        location.reload()
      });
      // } else {
      //   swal({
      //     title: "IPERC CONTINUO",
      //     text: "No puede crear más registros en el módulo de IPERC Continuo.",
      //     icon: "info",
      //   });
      // }

      // });

      // Obteniendo con json http select
      //  Escondiendo
    },
    click_nuevo_trabajador: async function(ev) {
      var evento = $(ev.currentTarget)
      var name = evento.parents(".trabajador").find("input[name='new-trabajador-nombre']").val()
      console.log(name)
      var fecha = evento.parents(".trabajador").find("input[name='new-trabajador-fecha']").val()
      console.log(fecha)
      var area = evento.parents(".trabajador").find("input[name='new-trabajador-area']").val()
      var dni = evento.parents(".trabajador").find("input[name='new-trabajador-dni']").val()
      var iperc_id = evento.data("iperc_id")
      console.log(iperc_id)
      await rpc.query({
        model: 'trabajador.iperc',
        method: 'create',
        args: [{
          "name": name,
          "fecha": fecha,
          "dni": dni,
          "area": area,
          "iperc_id": iperc_id
        }],
      }).then(function() {
        location.reload()
      });
    },
    click_nuevo_riesgo: async function(ev) {
      var evento = $(ev.currentTarget)
      var name = evento.parents(".trabajador").find("input[name='new-riesgo-descripcion']").val()
      var riesgo = evento.parents(".trabajador").find("input[name='new-riesgo-riesgo']").val()
      var evaluacion = evento.parents(".trabajador").find("input[name='new-riesgo-evaluacioniper']").val()
      var medidas = evento.parents(".trabajador").find("input[name='new-riesgo-medidas']").val()
      var riesgo_residual = evento.parents(".trabajador").find("input[name='new-riesgo-evaluacionriesgo']").val()
      var iperc_id = evento.data("iperc_id")
      await rpc.query({
        model: 'evaluacion.iperc',
        method: 'create',
        args: [{
          "name": name,
          "iperc_id": iperc_id
        }],
      }).then(function() {
        location.reload()
      });
    },
    click_nueva_secuencia: function(ev) {
      var evento = $(ev.currentTarget)
      var name = evento.parents(".secuencia").find("input[name='new-secuencia-descripcion']").val()
      var iperc_id = evento.data("iperc_id")
      rpc.query({
        model: 'control.iperc',
        method: 'create',
        args: [{
          "name": name,
          "iperc_id": iperc_id
        }],
      }).then(function() {
        location.reload()
      });
    },
    click_nuevo_supervisor: function(ev) {
      var evento = $(ev.currentTarget)
      var name = evento.parents(".supervisor").find("input[name='new-supervisor-name']").val()
      var fechainicial = evento.parents(".supervisor").find("input[name='new-supervisor-fecha']").val()
      var fecha = fechainicial.substr(0, 10) + ' ' + fechainicial.substr(11, 15)
      var medida = evento.parents(".supervisor").find("input[name='new-supervisor-medida']").val()
      var iperc_id = evento.data("iperc_id")
      rpc.query({
        model: 'supervisor.iperc',
        method: 'create',
        args: [{
          "name": name,
          "fecha": fecha,
          "medida": medida,
          "iperc_id": iperc_id
        }],
      }).then(function() {
        location.reload()
      });
    },
    change_evaluacion: function(ev) {
      var evento = $(ev.currentTarget)
      var val = evento.find("option:selected").val()
      var continuo_id = evento.data("continuo_id")

      if (val == "Alto") {
        $('.evaluacion-alto-' + continuo_id).css('background-color', 'red');
      } else if (val == "Medio") {
        $('.evaluacion-alto-' + continuo_id).css('background-color', 'yellow');
      } else if (val == "Bajo") {
        $('.evaluacion-alto-' + continuo_id).css('background-color', '#00FF00');
      }

      rpc.query({
        model: 'evaluacion.iperc.transient',
        method: 'guardar_linea',
        args: [1, continuo_id, "evaluacion", val]
      })
    },
    change_riesgo: function(ev) {
      var evento = $(ev.currentTarget)
      var val = evento.find("option:selected").val()
      var continuo_id = evento.data("continuo_id")
      if (val == "Alto") {
        $('.riesgo-alto-' + continuo_id).css('background-color', 'red');
      } else if (val == "Medio") {
        $('.riesgo-alto-' + continuo_id).css('background-color', 'yellow');
      } else if (val == "Bajo") {
        $('.riesgo-alto-' + continuo_id).css('background-color', '#00FF00');
      }

      rpc.query({
        model: 'evaluacion.iperc.transient',
        method: 'guardar_linea',
        args: [1, continuo_id, "riesgo_residual", val]
      })
      console.log(val)
    },
    action_eliminar_supervisor: function(ev) {
      var evento = $(ev.currentTarget)
      var continuo_id = evento.parents('.continuo_id').data("continuo_id")
      var supervisor_id = $(ev.target).data("supervisor_id")
      console.log(supervisor_id)
      rpc.query({
        model: "supervisor.iperc",
        method: "unlink",
        args: [supervisor_id],
      }).then(function(res) {
        location.reload();
      });
    },
    evaluacion_riesgo: async function(ev) {
      var evento = $(ev.currentTarget)
      var evaluacion_id = evento.parents('.evaluacion_id').data("evaluacion_id")
      var opcion = evento.val()
      var name = evento.attr("name")
      await rpc.query({
        model: 'evaluacion.iperc.transient',
        method: 'guardar_linea',
        args: [1, evaluacion_id, name, opcion]
      })
    },
    change_secuencia: async function(ev) {
      var evento = $(ev.currentTarget)
      var control_id = evento.parents('.control_id').data("control_id")
      var opcion = evento.val()
      var name = evento.attr("name")
      await rpc.query({
        model: 'control.iperc.transient',
        method: 'guardar_linea',
        args: [1, control_id, name, opcion]
      })
    },
    change_trabajadores: async function(ev) {
      var evento = $(ev.currentTarget)
      var trabajadores_id = evento.parents('.trabajadores_id').data("trabajadores_id")
      var opcion = evento.val()
      var name = evento.attr("name")
      await rpc.query({
        model: 'trabajador.iperc.transient',
        method: 'guardar_linea',
        args: [1, trabajadores_id, name, opcion]
      })
    },
    change_supervisor: async function(ev) {
      var evento = $(ev.currentTarget)
      var supervisor_id = evento.parents('.supervisor_id').data("supervisor_id")
      var opcion = evento.val()
      var name = evento.attr("name")
      if (name == 'fecha' && (opcion.length > 10)){
        opcion = opcion.substr(0,10)+' '+opcion.substr(11,15)
      }
      await rpc.query({
        model: 'supervisor.iperc.transient',
        method: 'guardar_linea',
        args: [1, supervisor_id, name, opcion]
      })
    },
    tipo_peligro: async function(ev) {
      var evento = $(ev.currentTarget)
      var val = evento.find("option:selected").text()
      var id = evento.find("option:selected").val()
      var evaluacion_id = evento.parents(".evaluacion_id").data("evaluacion_id")
      // var continuo_id = evento.data("continuo_id")
      console.log(val)

      if (val == "Alto") {
        $('.riesgo-alto-' + continuo_id).css('background-color', 'red');
      } else if (val == "Medio") {
        $('.riesgo-alto-' + continuo_id).css('background-color', 'yellow');
      } else if (val == "Bajo") {
        $('.riesgo-alto-' + continuo_id).css('background-color', '#00FF00');
      }

      rpc.query({
        route: "/continuo/descripcion",
        params: {
          name: val,
        }
      }).then(function(res) {
        $('#descripcion-' + evaluacion_id).empty()
        console.log(res[0])
        res.forEach(element => {

          $('#descripcion-' + evaluacion_id).append(`<option value=${element.id}>${element.name}</option>`);

        });

        rpc.query({
          model: 'evaluacion.iperc.transient',
          method: 'guardar_linea',
          args: [1, evaluacion_id, "name", res[0].name]
        })

      })

      rpc.query({
        model: 'evaluacion.iperc.transient',
        method: 'guardar_linea',
        args: [1, evaluacion_id, "type_id", id]
      })


    },
    evaluacion_riesgo_key: async function(ev) {
      var evento = $(ev.currentTarget)
      var evaluacion_id = evento.parents(".evaluacion_id").data("evaluacion_id")
      // var continuo_id = evento.data("continuo_id")
      evento.parents(".hint--medium").addClass('hint--bottom')
      evento.parents(".hint--medium").attr("data-hint", evento.val())

    },
    nuevo_tipo_peligro: function(ev) {
      var name = $(this.$el).find("input[name='new-tipo-peligro']").val()
      console.log($(this.$el))
      console.log(name)
      rpc.query({
        model: 'type.iperc',
        method: 'create',
        args: [{
          "name": name,
        }],
      }).then(function() {
        location.reload()
      });
    },
    eliminar_tipo: function(ev) {
      var evento = $(ev.currentTarget)
      var tipo_id = evento.data("tipo_id")
      rpc.query({
        model: "type.iperc",
        method: "unlink",
        args: [tipo_id],
      }).then(function(res) {
        location.reload();
      });
    },
    agregar_descripcion: function(ev) {
      var evento = $(ev.currentTarget)
      var nombre = evento.closest(".modal-content").find("input[name='new-tipo-descripcion']").val()
      var descripcion_id = evento.data("tipo_id")
      rpc.query({
        model: "descripcion.iperc",
        method: "create",
        args: [{
          "name": nombre,
          "descripcion_id": descripcion_id
        }],
      }).then(function(res) {
        location.reload();
      });
    },
    eliminar_descripcion: function(ev) {
      var evento = $(ev.currentTarget)
      var descripcion_id = evento.data("descripcion_id")
      rpc.query({
        model: "descripcion.iperc",
        method: "unlink",
        args: [descripcion_id],
      }).then(function(res) {
        location.reload();
      });
    },
    print_report: function(ev){
      var evento = $(ev.currentTarget)
      var iperc_id = evento.data("iperc_id")
      console.log('print_report')
      rpc.query({
        route: "/pdf/download",
        args: [1]
      }).then(function(res) {
        // location.reload();
      });
    }
  })



})
