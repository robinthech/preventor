odoo.define("lista_verificacion.lista", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb


  publicWidget.registry.SectionLista = publicWidget.Widget.extend({
    selector: ".section_lista",
    events: {
      'change input:radio': 'change_type_radio',
      'change .linea_verificacion': 'change_linea_verificacion',
      'change .linea_datos': 'change_linea_datos',
      'change .linea_datos_otros': 'change_linea_datos_otros',
      'click .guardar-formulario': 'guardar_formulario',
      'click .actualizar-excel': 'actualiza_excel',
      'click .nuevo-lista-otros': 'nuevo_lista_otros'
      // "click a.js_add_cart_json": "_onClickAddCartJSONT",
    },
    guardar_formulario: function(ev) {
      $("#alertsubmit").css("display", "block");
      setTimeout(
        function() {
          location.reload();
          window.scroll(0, 0);
        }, 1000)
    },
    change_linea_datos: async function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.parents('.lista_id').data("lista_id")
      var opcion = evento.val()
      var radioname = evento.attr("name")
      await rpc.query({
        model: 'lista.transient',
        method: 'guardar_linea',
        args: [1, lista_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });

      await rpc.query({
        model: 'lista.verificacion',
        method: 'file_excel',
        args: [lista_id],
      }).then(function() {
        // location.reload();
      });

    },
    change_linea_verificacion: function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.parents('.lista_id').data("lista_id")
      var opcion = evento.find("textarea").val()
      var radioname = evento.find("textarea").attr("name")
      rpc.query({
        model: 'lista.transient',
        method: 'guardar_linea',
        args: [1, lista_id, radioname, opcion]
      })
    },
    change_type_radio: async function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.parents('.lista_id').data("lista_id")
      var opcion = evento.closest('input').attr("value")
      var radioname = evento.closest('input').attr("name")
      var otros_id = evento.parents('tr').data("otros_id")
      var positivo = 0
      var negativo = 0
      var count_si = $("input[value=SI]:radio:checked").length
      var count_no = $("input[value=NO]:radio:checked").length
      var count_otros = $("tr[class=otros]").length
      var resultado = ((count_si / (121 + count_otros)) * 100).toFixed(2)
      console.log(count_si)
      console.log(121 + count_otros)
      $('.point').val(`${resultado}%`)
      if (otros_id) {
        await rpc.query({
          model: 'otros.transient',
          method: 'guardar_linea',
          args: [1, otros_id, 'otros_cumplimiento', opcion]
        })
      } else {
        await rpc.query({
          model: 'lista.transient',
          method: 'guardar_linea',
          args: [1, lista_id, radioname, opcion]
        })
      }

      await rpc.query({
        model: 'lista.verificacion',
        method: 'write',
        args: [
          [lista_id], {
            "count_si": count_si,
            "count_no": count_no,
            "puntaje": `${resultado}%`,
            "count_total": 121 + count_otros
          }
        ],
      }).then(function() {

      });

      await rpc.query({
        model: 'lista.verificacion',
        method: 'file_excel',
        args: [lista_id],
      }).then(function() {

      });
    },
    actualiza_excel: function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.parents('.lista_id').data("lista_id")
      // console.log(lista_id)
      rpc.query({
        model: 'lista.verificacion',
        method: 'file_excel',
        args: [lista_id],
      }).then(function() {
        location.reload();
      });
    },
    nuevo_lista_otros: function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.parents('.lista_id').data("lista_id")
      var indicador = $(this.$el).find("input[name='new-lista-indicador']").val()
      var fuente = $(this.$el).find("input[name='new-lista-fuente']").val()
      var otros_id = evento.data("lista_id")
      rpc.query({
        model: 'lista.otros',
        method: 'create',
        args: [{
          "otros_id": otros_id,
          "otros_indicador": indicador,
          "otros_fuente": fuente
        }],
      }).then(function() {
        location.reload();
      });

      rpc.query({
        model: 'lista.verificacion',
        method: 'file_excel',
        args: [lista_id],
      }).then(function() {
        location.reload();
      });
    },
    change_linea_datos_otros: async function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.parents('.lista_id').data("lista_id")
      var otros_id = evento.parents('tr').data("otros_id")
      var opcion = evento.find('textarea').val()
      var radioname = evento.find('textarea').attr("name")
      // console.log(evento)
      // console.log(radioname)
      // console.log(opcion)
      await rpc.query({
        model: 'otros.transient',
        method: 'guardar_linea',
        args: [1, otros_id, radioname, opcion]
      }).then(function() {
        // location.reload();
      });

      await rpc.query({
        model: 'lista.verificacion',
        method: 'file_excel',
        args: [lista_id],
      }).then(function() {
        // location.reload();
      });

    },
  })

  publicWidget.registry.Crearlista = publicWidget.Widget.extend({
    selector: ".lista-verificacion",
    jsLibs: [
      '/website_permiso/static/src/lib/notify.js',
    ],
    events: {
      'click .nuevo-lista-verificacion': 'click_nueva_lista',
      'click .actualizar-excel': 'actualiza_excel',
      'click .botton-eliminar-verificacion': 'action_eliminar_verificacion',
      'click .file-gratis': 'file_gratis',
    },
    click_nueva_lista: function(ev) {
      var evaluado = $(this.$el).find("input[name='new-lista-evaluado']").val()
      var empresa = $(this.$el).find("input[name='new-lista-empresa']").val()
      var fecha = $(this.$el).find("input[name='new-lista-fecha']").val()
      var plan_id = $('#modulo-lista-verificacion').data("plan_id");
      rpc.query({
        model: 'otros.transient',
        method: 'limites_permisos',
        args: [1, plan_id],
      }).then(function(output) {
        if (output) {
          rpc.query({
            model: 'lista.verificacion',
            method: 'create',
            args: [{
              "evaluado": evaluado,
              "fecha": fecha,
              "empresa": empresa
            }],
          }).then(function() {
            location.reload();
          });
        } else {
          swal({
            title: "Lista de Verificación",
            text: "No puede crear más Lista de Verificación.",
            icon: "info",
          });
        }

      });

    },
    actualiza_excel: function(ev) {
      var evento = $(ev.currentTarget)
      var lista_id = evento.closest('.actualizar-excel').data("verificacion_id")
      // console.log(lista_id)
      rpc.query({
        model: 'lista.verificacion',
        method: 'file_excel',
        args: [lista_id],
      }).then(function() {
        location.reload();

      });
    },
    action_eliminar_verificacion: function(ev) {
      var lista_id = $(ev.target).data("verificacion_id");
      rpc.query({
        model: "lista.verificacion",
        method: "unlink",
        args: [lista_id]
      }).then(function(res) {
        location.reload();
      });
    },
    file_gratis: function(ev) {
      swal({
        title: "Lista de verificacion",
        text: "No puede descargar más archivos excel con el plan Gratis.",
        icon: "info",
      });
    },
  })

  publicWidget.registry.Showguia = publicWidget.Widget.extend({
    selector: "#guia",
    events: {
      'click #next': 'showNextPage',
      'click #previous': 'showPrevPage',
      'click #last': 'showLastPage',
      'click #first': 'showFirstPage',
    },
    init: function() {

      this.pdfDoc = null
      this.pageNumIsPending = null
      this.pageIsRendering = false,
        this.pageNum = 1;

      console.log('showguia')
      var pdf_id = $('#guia').data("pdf_id")
      console.log(pdf_id)
      pdfjsLib.getDocument(`/web/content/${pdf_id}`).promise.then(pdf => {
        this.pdfDoc = pdf
        console.log(pdf.numPages)
        document.querySelector('#page_count').textContent = pdf.numPages;
        this.renderPage(1)
        this.renderPage(2)
      });

    },
    renderPage: function(num) {
      const scale = 1.5,
        canvas = document.querySelector('#my_canvas'),
        ctx = canvas.getContext('2d');
      this.pageIsRendering = true;
      // Get page
      this.pdfDoc.getPage(num).then(page => {
        // Set scale
        const viewport = page.getViewport({
          scale
        });
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        const renderCtx = {
          canvasContext: ctx,
          viewport
        };

        page.render(renderCtx).promise.then(() => {
          this.pageIsRendering = false;

          if (this.pageNumIsPending !== null) {
            renderPage(this.pageNumIsPending);
            this.pageNumIsPending = null;
          }
        });

        // Output current page
        document.querySelector('#page_number').textContent = num;
      })
    },
    queueRenderPage: function(num) {
      if (this.pageIsRendering) {
        this.pageNumIsPending = num;
      } else {
        this.renderPage(num);
      }
    },
    showNextPage: function() {
      if (this.pageNum >= this.pdfDoc.numPages) {
        return;
      }
      this.pageNum++;
      this.queueRenderPage(this.pageNum);
    },
    showPrevPage: function() {
      if (this.pageNum <= 1) {
        return;
      }
      this.pageNum--;
      this.queueRenderPage(this.pageNum);
    },
    showLastPage: function(){
      if (this.pageNum >= this.pdfDoc.numPages) {
        return;
      }
      this.pageNum = this.pdfDoc.numPages;
      this.queueRenderPage(this.pageNum);
    },
    showFirstPage: function(){
        if (this.pageNum <= 1) {
          return;
        }
        this.pageNum = 1;
        this.queueRenderPage(this.pageNum);
    },
  })

  publicWidget.registry.Imprimir = publicWidget.Widget.extend({
    selector:'#content',
    events: {
      'click .imprimir': 'imprimir'
    },
    imprimir:function(){
      var printContents = document.getElementById('sectionimprimir').innerHTML;
      var document_html = window.open("_blank");
      document_html.document.write( "<html><head><title></title>" );
      document_html.document.write( "<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css\" media=\"all\"/>" );
      // document_html.document.write( "<link rel=\"stylesheet\" href=\"https://preventor.tech/web/content/976-8b22757/1/web.assets_common.css\" type=\"text/css\" ");
      document_html.document.write( "<link rel=\"stylesheet\" href=\"https://preventor.tech/web/content/963-1894b32/1/web.assets_frontend.css\" media=\"all\"/>");
      document_html.document.write( "<link rel=\"stylesheet\" href=\"https://cdn.datatables.net/1.10.16/css/dataTables.bootstrap.min.css\" media=\"all\"/>" );
      document_html.document.write( "</head><body>" );
      document_html.document.write( printContents );
      document_html.document.write( "</body></html>" );
      setTimeout(function () {
       document_html.print();
      }, 500)
    }
  })


})
