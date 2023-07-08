odoo.define("mapa_riesgo.mapa_riesgo", function(require) {
  'use strict';

  var publicWidget = require("web.public.widget")
  var core = require("web.core")
  var rpc = require("web.rpc")
  var Widget = require("web.Widget")
  var qweb = core.qweb

  publicWidget.registry.CrearRegistroMapaRiesgo = publicWidget.Widget.extend({
    selector: ".list-mapa-riesgo",
    events: {
      'click .botton-mapa-riesgo': 'click_nuevo_registro_vigilancia',
      'click .botton-eliminar-mapeo-riesgo': 'click_eliminar_trabajador',

    },

    click_eliminar_trabajador:function(ev){
      var permiso_id = $(ev.target).data("registro_id");
      rpc.query({
        model: "mapa.riesgo",
        method: "unlink",
        args: [permiso_id]
      }).then(function(res) {
        location.reload();
      });

    },
    click_nuevo_registro_vigilancia: function(ev) {
      var name = $(this.$el).find("input[name='new-registro-name']").val()
      var plan_id = $('#modulo-mapa-riesgo').data("plan_id");
      rpc.query({
        model: 'mapa.riesgo',
        method: 'create',
        args: [{
          "name": name,
        }],
      }).then(function() {
        location.reload();

      });

    },
  })

  publicWidget.registry.AddImageSenal = publicWidget.Widget.extend({
  selector: ".principal-mapa_riesgo",
  events: {
    'click .add_imagen_senal': 'add_imagen_senal',
    'click #download_imagen': 'download_imagen',
    'click #download_pdf': 'download_pdf',
    "change #image_input":"click_image_input",
    'click .botton-guardar-mapa-riesgo': 'guardar_canva',
    'click .botton-undo': 'click_undo',
    'click .botton-redo': 'click_redo',
    'click .botton-minus': 'click_minus',
    'click .botton-plus': 'click_plus',
    'keydown': 'click_redo_undo',
  },
  init:  function() {

  },
  start: async function() {
    this.canvas = new fabric.Canvas('d', { selection: false });
    var canvas = this.canvas
    this.isRedoing = false;
    var isRedoing = this.isRedoing;
    this.h = [];
    var h = this.h;
    var registro_id = $(".principal-mapa_riesgo").data("registro_id");
    fabric.Object.prototype.set({
    transparentCorners: false,
    cornerColor: 'rgba(102,153,255,0.5)',
    cornerSize: 12,
    padding: 5
    });

    await rpc.query({
      model:'mapa.riesgo',
      method:'read',
      args:[[registro_id],["mapa_json"]],
    }).then(function(json){
      var json_replace = json[0]["mapa_json"].replaceAll("'","\"").replaceAll("None","\"\"").replaceAll("False","false").replaceAll("True","true");

      canvas.loadFromJSON( json_replace, canvas.renderAll.bind(canvas), function(o, object) {
        fabric.log(o, object);
      });
    });
  },
  click_redo_undo:function(ev){
    var self = this
      if( ev.which === 89 && ev.ctrlKey ){
        self.click_redo()
      }
      else if( ev.which === 90 && ev.ctrlKey ){
        self.click_undo()

      }
  },
  click_undo:function(){
    var canvas = this.canvas
    var h = this.h;
    if(canvas._objects.length>0){
       h.push(canvas._objects.pop());
       canvas.renderAll();
      }
  },
  click_redo:function(){
    var canvas = this.canvas
    var isRedoing = this.isRedoing
    var h = this.h;
    if(h.length>0){
      isRedoing = true;
     canvas.add(h.pop());
    }
  },
  click_draw:function(scale, translatePos){
      var canvas = this.canvas
      var context = canvas.getContext("2d");
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.save();
      context.translate(translatePos.x, translatePos.y);
      context.scale(scale, scale);
      var grd = context.createLinearGradient(-59, -100, 81, 100);
      context.fillStyle = grd;
      context.fill();

      context.lineWidth = 5;
      context.strokeStyle = "#0000ff";
      context.stroke();
      context.restore();
  },
  click_plus:function(){
    var canvas = this.canvas
    // var self = this
    // var translatePos = {
    //      x: canvas.width / 2,
    //      y: canvas.height / 2
    //  };
    //  var scale = 1.0;
    //  var scaleMultiplier = 0.9;
    //  var startDragOffset = {};
    //  var mouseDown = false;
    //   scale /= scaleMultiplier;
    //  self.click_draw(scale, translatePos);
    canvas.setZoom(canvas.getZoom() * 1.1 ) ;
  },
  click_minus:function(){
    var canvas = this.canvas
    // var self = this
    // var translatePos = {
    //      x: canvas.width / 2,
    //      y: canvas.height / 2
    //  };
    //  var scale = 1.0;
    //  var scaleMultiplier = 0.9;
    //  var startDragOffset = {};
    //  var mouseDown = false;
    //  scale *= scaleMultiplier;
    //  self.click_draw(scale, translatePos);
    canvas.setZoom(canvas.getZoom() / 1.1 ) ;
  },
  download_imagen: function() {
    $("#d").get(0).toBlob(function(blob){
        saveAs(blob, "Mapa .png");
       });
  },
  download_pdf: function() {
    $("#d").get(0).toBlob(function (blob) {
      var url = window.URL || window.webkitURL;
      var imgSrc = url.createObjectURL(blob);
      var img = new Image();
      img.src = imgSrc;
      img.onload = function () {
          var pdf = new jsPDF('p', 'px', [img.height, img.width]);
          pdf.addImage(img, 0, 0, img.width, img.height);
          pdf.save('Mapa de Riesgos.pdf');
      };
  });
  },
  guardar_canva: function() {
    var registro_id = $(".principal-mapa_riesgo").data("registro_id");
    var canvas = this.canvas
    var mapa_json= canvas.toJSON()
    var base64Canvas = canvas.toDataURL("image/jpeg").split(';base64,')[1];
    rpc.query({
      model:'mapa.riesgo',
      method:'write',
      args:[[registro_id],{"mapa_json":mapa_json,"have_map":true,"imagen":base64Canvas}],
    }).then(function(){
      $(".have-map").hide("slow");
    });
  },
  add_imagen_senal: function(ev) {
    var id_imagen = $(ev.target).attr('src');
    var canvas = this.canvas
    var pugImg = new Image();
    pugImg.src = id_imagen;
    var pug = new fabric.Image(pugImg, {
        width: 500,
        height: 500,
        left: 50,
        top: 70,
        scaleX: .25,
        scaleY: .25
    });
    canvas.add(pug);
    canvas.renderAll();
  },
  click_image_input: function(ev){
    var self = this
    var file = ev.target.files[0];
    var canvas = this.canvas
    console.log('canvas')
    console.log(canvas)
    var reader = new FileReader();
    reader.onload = function(f) {
      var data = f.target.result;
      var image = new Image();
      image.src = f.target.result;
      image.onload = function () {
          var height = this.height;
          var width = this.width;
          canvas.setDimensions({width: width, height: height});
        };
      fabric.Image.fromURL(data, function(img) {
        var oImg = img.set({
          left: 70,
          top: 100,
          width: 250,
          height: 200,
          angle: 0
          }).scale(0.9);
        canvas.setBackgroundImage(image.src, canvas.renderAll.bind(canvas), {
            backgroundImageOpacity: 0.5,
            backgroundImageStretch: false
        });
        canvas.renderAll();
        var dataURL = canvas.toDataURL({
          format: 'png',
          quality: 0.8
          });
        });
    };
  reader.readAsDataURL(file);
  self.guardar_canva()
  },



})

publicWidget.registry.PanelMapaRiesgo = publicWidget.Widget.extend({
selector: ".panelmapariesgo",
events: {
  'click .add_imagen_senal': 'add_imagen_senal',
  'click #download_imagen': 'download_imagen',
  'click #download_pdf': 'download_pdf',
  "change #image_input":"click_image_input",
  'click .botton-guardar-mapa-riesgo': 'guardar_canva',
  'click .botton-undo': 'click_undo',
  'click .botton-redo': 'click_redo',
  'click .botton-minus': 'click_minus',
  'click .botton-plus': 'click_plus',
  'keydown': 'click_redo_undo',
},
init:  function() {

},
start: async function() {
  this.canvas = new fabric.Canvas('d', { selection: false });
  var canvas = this.canvas
  this.isRedoing = false;
  var isRedoing = this.isRedoing;
  this.h = [];
  var h = this.h;
  var registro_id = $(".panelmapariesgo").data("registro_id");
  fabric.Object.prototype.set({
  transparentCorners: false,
  cornerColor: 'rgba(102,153,255,0.5)',
  cornerSize: 12,
  padding: 5
  });

  await rpc.query({
    model:'mapa.riesgo',
    method:'read',
    args:[[registro_id],["mapa_json"]],
  }).then(function(json){
    var json_replace = json[0]["mapa_json"].replaceAll("'","\"").replaceAll("None","\"\"").replaceAll("False","false").replaceAll("True","true");

    canvas.loadFromJSON( json_replace, canvas.renderAll.bind(canvas), function(o, object) {
      fabric.log(o, object);
    });
  });
},
click_redo_undo:function(ev){
  var self = this
    if( ev.which === 89 && ev.ctrlKey ){
      self.click_redo()
    }
    else if( ev.which === 90 && ev.ctrlKey ){
      self.click_undo()

    }
},
click_undo:function(){
  var canvas = this.canvas
  var h = this.h;
  if(canvas._objects.length>0){
     h.push(canvas._objects.pop());
     canvas.renderAll();
    }
},
click_redo:function(){
  var canvas = this.canvas
  var isRedoing = this.isRedoing
  var h = this.h;
  if(h.length>0){
    isRedoing = true;
   canvas.add(h.pop());
  }
},
click_draw:function(scale, translatePos){
    var canvas = this.canvas
    var context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.save();
    context.translate(translatePos.x, translatePos.y);
    context.scale(scale, scale);
    var grd = context.createLinearGradient(-59, -100, 81, 100);
    context.fillStyle = grd;
    context.fill();

    context.lineWidth = 5;
    context.strokeStyle = "#0000ff";
    context.stroke();
    context.restore();
},
click_plus:function(){
  var canvas = this.canvas
  // var self = this
  // var translatePos = {
  //      x: canvas.width / 2,
  //      y: canvas.height / 2
  //  };
  //  var scale = 1.0;
  //  var scaleMultiplier = 0.9;
  //  var startDragOffset = {};
  //  var mouseDown = false;
  //   scale /= scaleMultiplier;
  //  self.click_draw(scale, translatePos);
  canvas.setZoom(canvas.getZoom() * 1.1 ) ;
},
click_minus:function(){
  var canvas = this.canvas
  // var self = this
  // var translatePos = {
  //      x: canvas.width / 2,
  //      y: canvas.height / 2
  //  };
  //  var scale = 1.0;
  //  var scaleMultiplier = 0.9;
  //  var startDragOffset = {};
  //  var mouseDown = false;
  //  scale *= scaleMultiplier;
  //  self.click_draw(scale, translatePos);
  canvas.setZoom(canvas.getZoom() / 1.1 ) ;
},
download_imagen: function() {
  $("#d").get(0).toBlob(function(blob){
      saveAs(blob, "Mapa .png");
     });
},
download_pdf: function() {
  $("#d").get(0).toBlob(function (blob) {
    var url = window.URL || window.webkitURL;
    var imgSrc = url.createObjectURL(blob);
    var img = new Image();
    img.src = imgSrc;
    img.onload = function () {
        var pdf = new jsPDF('p', 'px', [img.height, img.width]);
        pdf.addImage(img, 0, 0, img.width, img.height);
        pdf.save('Mapa de Riesgos.pdf');
    };
});
},
guardar_canva: function() {
  var registro_id = $(".principal-mapa_riesgo").data("registro_id");
  var canvas = this.canvas
  var mapa_json= canvas.toJSON()
  var base64Canvas = canvas.toDataURL("image/jpeg").split(';base64,')[1];
  rpc.query({
    model:'mapa.riesgo',
    method:'write',
    args:[[registro_id],{"mapa_json":mapa_json,"have_map":true,"imagen":base64Canvas}],
  }).then(function(){
    $(".have-map").hide("slow");
  });
},
add_imagen_senal: function(ev) {
  var id_imagen = $(ev.target).attr('src');
  var canvas = this.canvas
  var pugImg = new Image();
  pugImg.src = id_imagen;
  var pug = new fabric.Image(pugImg, {
      width: 500,
      height: 500,
      left: 50,
      top: 70,
      scaleX: .25,
      scaleY: .25
  });
  canvas.add(pug);
  canvas.renderAll();
},
click_image_input: function(ev){
  var self = this
  var file = ev.target.files[0];
  var canvas = this.canvas
  console.log('canvas')
  console.log(canvas)
  var reader = new FileReader();
  reader.onload = function(f) {
    var data = f.target.result;
    var image = new Image();
    image.src = f.target.result;
    image.onload = function () {
        var height = this.height;
        var width = this.width;
        canvas.setDimensions({width: width, height: height});
      };
    fabric.Image.fromURL(data, function(img) {
      var oImg = img.set({
        left: 70,
        top: 100,
        width: 250,
        height: 200,
        angle: 0
        }).scale(0.9);
      canvas.setBackgroundImage(image.src, canvas.renderAll.bind(canvas), {
          backgroundImageOpacity: 0.5,
          backgroundImageStretch: false
      });
      canvas.renderAll();
      var dataURL = canvas.toDataURL({
        format: 'png',
        quality: 0.8
        });
      });
  };
reader.readAsDataURL(file);
self.guardar_canva()
},



})



})
