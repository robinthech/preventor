odoo.define("website_permiso",function(require){
		'use strict';
		var Notification = require('web.Notification');
		var publicWidget = require("web.public.widget");
		var rpc = require("web.rpc");
		var core = require('web.core');
		var QWeb = core.qweb;
		var _t = core._t;
		var session = require('web.session');



		// $(document).ready( function () {
		// });

		publicWidget.registry.RowAlternativas = publicWidget.Widget.extend({
				selector:".permiso-formulario",
				xmlDependencies: ['/web/static/src/xml/notification.xml'],
				jsLibs: [
					'/website_permiso/static/src/lib/notify.js',
				],
				events:{
					'click .nuevo-epp-altura':'click_epp_altura',
					'click .btn-solicitar':'click_solicitar',
					'click .btn-autorizar':'click_autorizar',
					'click .btn-aprobar':'click_aprobar',
					'click .check-altura':'click_altura',
					'click .check-confinado':'click_confinado',
					'click .check-caliente':'click_caliente',
					'click .check-frio':'click_frio',
					'click .check-electrico':'click_electrico',
					'change .area-select':'click_area',
					'change .sub-area-select':'click_sub_area',
					'click .contratista-select':'click_contratista',
					'click .solicitante-select':'click_solicitante',
					'click .autorizador-select':'click_autorizador',
					'click .aprobador-select':'click_aprobador',
					'change .ubicacion':'click_ubicacion',
					'change .fecha-inicio':'click_fecha_inicio',
					'change .hora-inicio':'click_fecha_inicio',
					'change .fecha-fin':'click_fecha_fin',
					'change .hora-fin':'click_fecha_fin',
					'change .decri-trabajo':'click_descripcion',
					'click .anadir-trabajador':'click_anadir_trabajador',
					'click .observacion-aprobar':'click_observacion_aprobar',
					'click .observacion-autorizar':'click_observacion_autorizar',
					'click .cancelar':'click_cancelar',
					'click .nuevo-requisito':'click_nuevo_requisito',
				},
				click_nuevo_requisito:function(ev){
					var permiso_id = $(".permiso-formulario").data("permiso_id");
					var evento = $(ev.currentTarget)
					var name = $(ev.currentTarget).parent().parent().find("input[name='new-name']").val()
					var tipo_requi_id = evento.data("tipo_requi_id")
					var tipo_permiso_id = evento.data("tipo_permiso_id")
					rpc.query({
						model:'permiso.create.line',
						method:'nuevo_requisito',
						args:[1,permiso_id,tipo_requi_id,tipo_permiso_id,name],
					}).then(function(){
						rpc.query({
							model: 'permiso.trabajo',
							method: 'open_word_frio',
							args: [permiso_id],
						}).then(function() {});
						location.reload();

					});
				},

				click_epp_altura:function(ev){
					var permiso_id = $(".permiso-formulario").data("permiso_id");
					rpc.query({
						model:'permiso.create.line',
						method:'cancelar_permiso',
						args:[1,permiso_id],
					}).then(function(){
						rpc.query({
							model: 'permiso.trabajo',
							method: 'open_word_frio',
							args: [permiso_id],
						}).then(function() {});
						location.reload();
					});
				},
				click_cancelar:function(ev){
					var permiso_id = $(".permiso-formulario").data("permiso_id");
					rpc.query({
						model:'permiso.create.line',
						method:'cancelar_permiso',
						args:[1,permiso_id],
					}).then(function(){
						rpc.query({
							model: 'permiso.trabajo',
							method: 'open_word_frio',
							args: [permiso_id],
						}).then(function() {});
						location.reload();
					});
			},
				click_observacion_autorizar:function(ev){
					var permiso_id = $(".permiso-formulario").data("permiso_id");
					var nuevo_trabajador = $(".text-observacion-auto").val();
					rpc.query({
						model:'permiso.create.line',
						method:'funcion_observacion_autorizar',
						args:[1,permiso_id,nuevo_trabajador],
					}).then(function(){
						rpc.query({
							model: 'permiso.trabajo',
							method: 'open_word_frio',
							args: [permiso_id],
						}).then(function() {});
						location.reload();
					});

				},
				click_observacion_aprobar:function(ev){
					var permiso_id = $(".permiso-formulario").data("permiso_id");
					var nuevo_trabajador = $(".text-observacion-apro").val();
					rpc.query({
						model:'permiso.create.line',
						method:'funcion_observacion_aprobar',
						args:[1,permiso_id,nuevo_trabajador],
					}).then(function(){
						rpc.query({
							model: 'permiso.trabajo',
							method: 'open_word_frio',
							args: [permiso_id],
						}).then(function() {});
						location.reload();

					});

				},
				click_anadir_trabajador:function(ev){
					var permiso_id = $(".permiso-formulario").data("permiso_id");
					var nuevo_trabajador = $(".trabajador-add").val();
					rpc.query({
						model:'permiso.create.line',
						method:'nuevo_trabajador',
						args:[1,permiso_id,nuevo_trabajador],
					}).then(function(){
						rpc.query({
							model: 'permiso.trabajo',
							method: 'open_word_frio',
							args: [permiso_id],
						}).then(function() {});
						location.reload();

					});

				},
				click_descripcion:function(ev){
					var permiso_id = $(".permiso-formulario").data("permiso_id");
					var fecha_inicio = $(".decri-trabajo").val();
					rpc.query({
						model:'permiso.trabajo',
						method:'write',
						args:[[permiso_id],{"descripcion":fecha_inicio}],
					}).then(function(){
						rpc.query({
							model: 'permiso.trabajo',
							method: 'open_word_frio',
							args: [permiso_id],
						}).then(function() {});
						location.reload();

					});

				},
				click_fecha_inicio:function(ev){
					var permiso_id = $(".permiso-formulario").data("permiso_id");
					var fecha_inicio = $(".fecha-inicio").val();
					var hora_inicio = $(".hora-inicio").val();
					var fecha_fin = $(".fecha-fin");
					fecha_fin.attr('min',fecha_inicio)
					if (fecha_inicio.length != 0){
						if (hora_inicio.length != 0){
							var fecha_hora_inicio = fecha_inicio + " "+ hora_inicio ;
							rpc.query({
								model:'permiso.trabajo',
								method:'write',
								args:[[permiso_id],{"fecha_inicio":fecha_hora_inicio}],
							}).then();
						};
					};

				},
				click_fecha_fin:function(ev){
					var permiso_id = $(".permiso-formulario").data("permiso_id");
					var fecha_fin = $(".fecha-fin").val();
					var hora_fin = $(".hora-fin").val();
					var fecha_inicio = $(".fecha-inicio");
					fecha_inicio.attr('max',fecha_fin)

					if (fecha_inicio.length != 0){
						if (hora_fin.length != 0){
							var fecha_hora_fin = fecha_fin + " "+ hora_fin ;
							rpc.query({
								model:'permiso.trabajo',
								method:'write',
								args:[[permiso_id],{"fecha_fin":fecha_hora_fin}],
							}).then();
						};
					};
				},
				click_ubicacion:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".ubicacion").val();
						rpc.query({
							model:'permiso.create.line',
							method:'guardar_ubicacion',
							args:[1,permiso_id,value],
						}).then(function(output){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});
						});
				},
				click_sub_area:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".sub-area-select").val();
						rpc.query({
							model:'permiso.create.line',
							method:'guardar_sub_area',
							args:[1,permiso_id,value],
						}).then(function(output){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});
						});
				},
				click_solicitante:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".solicitante-select").val();
						rpc.query({
							model:'permiso.create.line',
							method:'guardar_solicitante',
							args:[1,permiso_id,value],
						}).then(function(output){
							$(".firma-solicitante").attr("src",output);
							// rpc.query({
							// 	model: 'permiso.trabajo',
							// 	method: 'open_word_frio',
							// 	args: [permiso_id],
							// }).then(function() {});
						});
				},
				click_autorizador:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".autorizador-select").val();
						rpc.query({
							model:'permiso.create.line',
							method:'guardar_autorizador',
							args:[1,permiso_id,value],
						}).then(function(output){
							$(".firma-autorizador").attr("src",output);
							// rpc.query({
							// 	model: 'permiso.trabajo',
							// 	method: 'open_word_frio',
							// 	args: [permiso_id],
							// }).then(function() {});
						});
				},
				click_aprobador:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".aprobador-select").val();
						rpc.query({
							model:'permiso.create.line',
							method:'guardar_aprobador',
							args:[1,permiso_id,value],
						}).then(function(output){
							$(".firma-aprobador").attr("src",output);
							// rpc.query({
							// 	model: 'permiso.trabajo',
							// 	method: 'open_word_frio',
							// 	args: [permiso_id],
							// }).then(function() {});
						});
				},
				click_area:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".area-select").val();
						rpc.query({
							model:'permiso.create.line',
							method:'guardar_area',
							args:[1,permiso_id,value],
						}).then(function(output){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});

						});
				},
				click_contratista:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".contratista-select").val();
						rpc.query({
							model:'permiso.create.line',
							method:'guardar_contratista',
							 args:[1,permiso_id,value],
						}).then(function(output){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});

						});
				},
				click_altura:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".check-altura").is(":checked");
						rpc.query({
							model:'permiso.trabajo',
							method:'write',
							args:[[permiso_id],{"altura":value}],
						}).then(function(){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});
						});

				},
				click_confinado:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".check-confinado").is(":checked");
						rpc.query({
							model:'permiso.trabajo',
							method:'write',
							args:[[permiso_id],{"confinado":value}],
						}).then(function(){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});
							location.reload();

						});

				},
				click_caliente:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".check-caliente").is(":checked");
						rpc.query({
							model:'permiso.trabajo',
							method:'write',
							args:[[permiso_id],{"calor":value}],
						}).then(function(){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});
							location.reload();

						});

				},
				click_frio:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".check-frio").is(":checked");
						rpc.query({
							model:'permiso.trabajo',
							method:'write',
							args:[[permiso_id],{"frio":value}],
						}).then(function(){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});
							location.reload();

						});

				},
				click_electrico:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						var value =$(".check-electrico").is(":checked");
						rpc.query({
							model:'permiso.trabajo',
							method:'write',
							args:[[permiso_id],{"electrico":value}],
						}).then(function(){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});
							location.reload();

						});

				},

				click_solicitar:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");

						rpc.query({
							model:'permiso.create.line',
							method:'solicitar_permiso',
							args:[1,permiso_id],
						}).then(function(){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});
							location.reload();

						});

				},
				click_aprobar:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						rpc.query({
							model:'permiso.create.line',
							method:'aprobar_permiso',
							args:[1,permiso_id],
						}).then(function(){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});
							location.reload();

						});

				},
				click_autorizar:function(ev){
						var permiso_id = $(".permiso-formulario").data("permiso_id");
						rpc.query({
							model:'permiso.create.line',
							method:'autorizar_permiso',
							args:[1,permiso_id],
						}).then(function(){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});
							location.reload();

						}
						);

				},
		})


		publicWidget.registry.Requisitos = publicWidget.Widget.extend({
				selector:".requisito-div",
				events:{
					'click .requisito-permiso':'click_permiso_requisito',
				},
				click_permiso_requisito:function(ev){
					var permiso_id = $(".permiso-formulario").data("permiso_id");
						var linea_id = $(ev.target).data("linea_id");
						var value = $(ev.target).is(":checked");
						rpc.query({
							model:'requisito.permiso',
							method:'write',
							args:[[linea_id],{"check":value}],
						}).then(function(){
							rpc.query({
								model: 'permiso.trabajo',
								method: 'open_word_frio',
								args: [permiso_id],
							}).then(function() {});

						});

				},
		})

		publicWidget.registry.CrearTrabajador = publicWidget.Widget.extend({
				selector:".trabajador-form",
				events:{
					'click .nuevo-trabajador': 'click_nuevo_trabajador',
					'click .eliminar-trabajador': 'click_eliminar_trabajador',
				},
				click_nuevo_trabajador:function(ev){
					var nombre = $(this.$el).find("input[name='new-trabajador-name']").val()
					var apellido = $(this.$el).find("input[name='new-trabajador-apellido']").val()
					var dni = $(this.$el).find("input[name='new-trabajador-dni']").val()
					var empresa_id = $(this.$el).find("select[name='new-empresa-trabajador-select']").val()
					var name = nombre + " " + apellido
						rpc.query({
							model:'trabajador.trabajador',
							method:'create',
							args:[{ "name": nombre, "nombre": nombre,
								"apellido": apellido,"empresa_id": empresa_id,
								"dni": dni}],
						}).then(function(){
							location.reload();

						});

				},
				click_eliminar_trabajador:function(ev){
					var permiso_id = $(ev.target).data("trabajador_id");
					rpc.query({
						model: "trabajador.trabajador",
						method: "unlink",
						args: [permiso_id]
					}).then(function(res) {
						location.reload();
					});

				},
		})

		publicWidget.registry.RolesPermisodeTrabajo = publicWidget.Widget.extend({
				selector:".roles-usuario",
				events:{
					'change .change_role': 'change_role_usuario',
				},
				change_role_usuario:function(ev){
		      var evento = $(ev.currentTarget)
		      var usuario_id = evento.parents('.usuario_id').data("usuario_id")
		      var role = evento.data("role")
					rpc.query({
						model:'res.users',
						method:'write',
						args:[[usuario_id],{"perfil_permiso": String(role)}],
					}).then(function(){
						// location.reload();

					});

				},

		})

		publicWidget.registry.Crearempresa = publicWidget.Widget.extend({
				selector:".empresa-form",
				events:{
					'click .nuevo-empresa': 'click_nuevo_trabajador',
					'click .eliminar-empresa': 'click_eliminar_trabajador',
				},
				click_nuevo_trabajador:function(ev){
					var nombre = $(this.$el).find("input[name='new-empresa-name']").val()
					var razon = $(this.$el).find("input[name='new-empresa-razon_social']").val()
					var ruc = $(this.$el).find("input[name='new-empresa-ruc']").val()
						rpc.query({
							model:'empresa.empresa',
							method:'create',
							args:[{  "name": nombre,
								"razon_social": razon,
								"ruc": ruc}],
						}).then(function(){
							location.reload();

						});

				},
				click_eliminar_trabajador:function(ev){
					var permiso_id = $(ev.target).data("empresa_id");
					rpc.query({
						model: "empresa.empresa",
						method: "unlink",
						args: [permiso_id]
					}).then(function(res) {
						location.reload();
					});

				},
		})

		publicWidget.registry.PerfildeUsuario = publicWidget.Widget.extend({
				selector:".usuario-perfil",
				jsLibs:["https://cdn.datatables.net/1.10.24/js/jquery.dataTables.js"],
				init: function(){
					this._super.apply(this,arguments)
					var self = this;
					var session = this.getSession()
					var canvas = document.querySelector("canvas")

					// var signature = this.signaturePad = new SignaturePad(canvas)
					canvas.width = $("#firma").width();
					canvas.height = $("#firma").height();

					self._rpc({
										model: 'res.users',
										method: 'read',
										args: [session.user_id, ['signature_binary']],
								}).then(function(user) {
									// signature.fromDataURL("data:image/png;base64, "+user[0].signature_binary)
								})

					this.spanish = {
							"sProcessing":     "Procesando...",
							"sLengthMenu":     "Mostrar _MENU_ registros",
							"sZeroRecords":    "No se encontraron resultados",
							"sEmptyTable":     "Ningún dato disponible en esta tabla",
							"sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
							"sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
							"sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
							"sSearch":         "Buscar:",
							"sInfoThousands":  ",",
							"sLoadingRecords": "Cargando...",
							"oPaginate": {
									"sFirst":    "Primero",
									"sLast":     "Último",
									"sNext":     "Siguiente",
									"sPrevious": "Anterior"
							},
							"oAria": {
									"sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
									"sSortDescending": ": Activar para ordenar la columna de manera descendente"
							},
							"buttons": {
									"copy": "Copiar",
									"colvis": "Visibilidad"
							}
					}
				},
				start: function(){
						var self = this;
						$('#table_planilla').DataTable({
							"language": self.spanish,
							"columnDefs": [
								{ targets: 'no-sort', orderable: false }
							]
						});
						$('#table_servicios').DataTable({
							"language": self.spanish,
							"columnDefs": [
								{ targets: 'no-sort', orderable: false }
							]
						});
						$('.contratista').DataTable({
							"language": self.spanish
						});
				},
				events:{
					'submit .nuevo_usuario': 'click_nuevo_usuario',
					'click .nueva-sede': 'click_nueva_sede',
					'click .guardar-sede': 'click_guardar_sede',
					'click .botton-eliminar-sede': 'click_eliminar_sede',
					'click .nuevo-trabajador': 'click_nuevo_trabajador',
					'click .guardar-trabajador': 'click_guardar_trabajador',
					'click .botton-eliminar-trabajador': 'click_eliminar_trabajador',
					'click .nuevo-contratista': 'click_nuevo_contratista',
					'click .nuevo-empresa-usuario': 'click_nuevo_empresa',
					'click .nuevo-contratista-trabajador': 'click_nuevo_contratista_trabajador',
					'change #name_empresa': 'change_name_empresa',
					'change #ruc': 'change_ruc',
					'change #correo': 'change_correo',
					'change #telefon': 'change_telefono',
					'change #name_usuario': 'change_name_usuario',
					'change #dni': 'change_dni_usuario',
					'click .search-user': 'click_search_user',
					// action from signature
					'click span[data-action=clear]': '_onClearClick',
					'click span[data-action=undo]': '_onUndoClick',
					'click span[data-action=save-png]': '_onSaveClick',
					'mouseup .linea_firma': 'change_linea_firma',
					'touchend .linea_firma': 'change_linea_firma',
					'change #image_input':'change_image_input',
				},
	      change_image_input:async function(ev){
					var self = this
					this.signaturePad.clear()

			    var file = ev.target.files[0];
					var context = document.querySelector("canvas").getContext('2d')

					var session = this.getSession()
					var reader = new FileReader();
					var img = document.createElement("img");

					reader.onloadend = async function() {
							 img.src = reader.result
							 var signature_binary = reader.result.split(';base64,')[1]
							 rpc.query({
		 						model: 'res.users',
		 						method: 'write',
		 						args: [[session.user_id],{ "signature_binary":signature_binary}],
		 					}).then(function() {
			        	context.drawImage(img, 0, 0,600,157);
		 					});
					}
					reader.readAsDataURL(file);
	      },

				dataURLToBlob: function(dataURL) {

					var parts = dataURL.split(';base64,');
					var contentType = parts[0].split(":")[1];
					var raw = window.atob(parts[1]);
					var rawLength = raw.length;
					var uInt8Array = new Uint8Array(rawLength);

					for (var i = 0; i < rawLength; ++i) {
						uInt8Array[i] = raw.charCodeAt(i);
					}

					return new Blob([uInt8Array], { type: contentType });
				},

				download: function(dataURL, filename) {
					if (navigator.userAgent.indexOf("Safari") > -1 && navigator.userAgent.indexOf("Chrome") === -1) {
						window.open(dataURL);
					} else {
						var blob = this.dataURLToBlob(dataURL);
						var url = window.URL.createObjectURL(blob);

						var a = document.createElement("a");
						a.style = "display: none";
						a.href = url;
						a.download = filename;

						document.body.appendChild(a);
						a.click();

						window.URL.revokeObjectURL(url);
					}
				},
				_onSaveClick: function(){
					if (this.signaturePad.isEmpty()) {
						alert("Primero realice la firma.");
					} else {
						var dataURL = this.signaturePad.toDataURL();
						this.download(dataURL, "signature.png");
					}
				},
				_onUndoClick: function(){
					var data = this.signaturePad.toData();
					if (data) {
					 data.pop(); // remove the last dot or line
					 this.signaturePad.fromData(data);
					}
				},
				_onClearClick: function(){
					this.signaturePad.clear()
				},
				change_linea_firma: function(ev){
					var evento = $(ev.currentTarget)
					var usuario_id = evento.parents('.usuario_id').data("usuario_id")
					var signature = this.signaturePad.toDataURL("image/png")
					var signature_binary = signature.split(';base64,')[1];
					const data = this.signaturePad.toData();
					console.log(data)
					rpc.query({
						model: 'res.users',
						method: 'write',
						args: [[usuario_id],{ "signature_binary":signature_binary}],
					}).then(function() {
						// location.reload();
					});
				},
				click_eliminar_trabajador:function(ev){
					var evento = $(ev.currentTarget)
					var trabajador_id = evento.data("trabajador_id")
					rpc.query({
							model:"trabajador.trabajador",
							method:"unlink",
							args:[[trabajador_id]]
					}).then(function(res){
							location.reload();
					})
				},
				click_guardar_trabajador:function(ev){
						var evento = $(ev.currentTarget)
						var id = evento.data("trabajador_id")
						var nombre = evento.closest(".modal-content").find("input[name='new-trabajador-nombres']").val()
						var dni = evento.closest(".modal-content").find("input[name='new-trabajador-dni']").val()
						var puesto = evento.closest(".modal-content").find("input[name='new-trabajador-puesto']").val()
						var tipo = evento.closest(".modal-content").find("#tipo option:selected").val()
						rpc.query({
							model:'trabajador.trabajador',
							method:'write',
							args:[[id],{"name": nombre,"dni": dni,"puesto": puesto,"tipo": tipo}],
						}).then(function(){
							location.reload();
						})
				},
				click_guardar_sede:function(ev){
						var evento = $(ev.currentTarget)
						var id = evento.data("sede_id")
						var name = evento.closest(".modal-content").find("input[name='new-sede-name']").val()
						var encargado = evento.closest(".modal-content").find(".edit-encargado option:selected").val()
						var dni = evento.closest(".modal-content").find("input[name='new-sede-dni']").val()
						var puesto = evento.closest(".modal-content").find("input[name='new-sede-puesto']").val()
						var trabajadores = evento.closest(".modal-content").find("input[name='new-sede-trabajadores']").val()
						rpc.query({
							model:'sede.sede',
							method:'write',
							args:[[id],{"name": name,"encargado": encargado,"dni": dni,"puesto": puesto,"trabajadores": trabajadores}],
						}).then(function(){
							location.reload();
						})
				},
				click_eliminar_sede:function(ev){
						var evento = $(ev.currentTarget)
						var registro_id = evento.data("sede_id")
						rpc.query({
								model:"sede.sede",
								method:"unlink",
								args:[[registro_id]]
						}).then(function(res){
								location.reload();
						})
				},
				click_nuevo_trabajador:function(ev){
					var evento = $(ev.currentTarget)
					var empresa_id = evento.data("empresa_id")
					var usuario_id = evento.data("usuario_id")
					var nombre = evento.closest(".modal-content").find("input[name='new-trabajador-nombres']").val()
					var dni = evento.closest(".modal-content").find("input[name='new-trabajador-dni']").val()
					var puesto = evento.closest(".modal-content").find("input[name='new-trabajador-puesto']").val()
					var tipo = $("#tipo option:selected").val()
					rpc.query({
						model:'trabajador.trabajador',
						method:'create',
						args:[{"name": nombre,"dni": dni,"puesto": puesto,"empresa_id": empresa_id,"tipo": tipo}],
					}).then(function(){
						location.reload()
					});
				},
				click_nuevo_contratista:function(ev){
					var evento = $(ev.currentTarget)
					var empresa_id = evento.data("empresa_id")
					var usuario_id = evento.data("usuario_id")
					var name = evento.closest(".modal-content").find("input[name='new-contratista-name']").val()
					rpc.query({
						model:'contratista.contratista',
						method:'create',
						args:[{"name": name,"empresa_id": empresa_id}],
					}).then(function(){
						location.reload()
					});
				},
				click_nuevo_contratista_trabajador:function(ev){
					var evento = $(ev.currentTarget)
					var contratista_id = evento.data("contratista_id")
					var usuario_id = evento.data("usuario_id")
					var name = evento.closest(".modal-content").find("input[name='new-contratista-name']").val()
					var dni = evento.closest(".modal-content").find("input[name='new-contratista-dni']").val()
					var correo = evento.closest(".modal-content").find("input[name='new-contratista-correo']").val()
					var telefono = evento.closest(".modal-content").find("input[name='new-contratista-telefono']").val()
					var puesto = evento.closest(".modal-content").find("input[name='new-contratista-puesto']").val()
					rpc.query({
						model:'trabajador.contratista',
						method:'create',
						args:[{"name":name,"dni":dni,"correo":correo,"telefono":telefono,"puesto":puesto,"contratisa_id": contratista_id}],
					}).then(function(){
						location.reload()
					});
				},
				click_nuevo_usuario:function(ev){
					ev.preventDefault()
					var evento = $(ev.currentTarget)
					var empresa_id = evento.data("empresa_id")
					var usuario_id = evento.data("usuario_id")
					var nombre = evento.closest(".modal-content").find("input[name='new-usuario-name']").val()
					var email = evento.closest(".modal-content").find("input[name='new-usuario-email']").val()
					var perfil = evento.closest(".modal-content").find(".perfil-usuario option:selected").val()
					var selected = []
					$('#checkboxes input:checked').each(function() {
							selected.push($(this).attr('id'));
					})
					rpc.query({
						model: 'user.transient',
						method: 'limites_permisos',
						args: [1],
					}).then(function(output) {
						if (output) {
							rpc.query({
								route:"/createuser",
								params:{  "name": nombre,
									"login": email,
									"parent_id":usuario_id,
									"planes": selected,
									"empresa_id":empresa_id,
									"perfil":perfil
								},
							}).then(function(output) {
									console.log(output)
									if(output){
										location.reload()
									}else{
										swal({
												title: "Agregar usuario",
												text: `Un usuario ya esta registrado con este correo.
												Contacta a soporte@softwaresst.com.`,
												icon: "info",
											});
									}
								});
						}else {
							swal({
									title: "Invitado",
									text: "Tu plan gratuito no permite agregar mas invitados.",
									icon: "info",
								});
						}

					});

				},
				click_nuevo_empresa:function(ev){
					var evento = $(ev.currentTarget)
					var nombre = evento.closest(".modal-content").find("input[name='new-empresa-name']").val()
					var ruc = evento.closest(".modal-content").find("input[name='new-empresa-ruc']").val()
					var correo = evento.closest(".modal-content").find("input[name='new-empresa-correo']").val()
					var telefono = evento.closest(".modal-content").find("input[name='new-usuario-telefono']").val()
						rpc.query({
							model:'permiso.create.line',
							method:'crear_empresa_usuario',
							args:[1,nombre, ruc,correo, telefono],
						}).then(function(){
							location.reload();
						});
				},
				click_nueva_sede:function(ev){
					var evento = $(ev.currentTarget)
					var name = evento.closest(".modal-content").find("input[name='new-sede-name']").val()
					var dni = evento.closest(".modal-content").find("input[name='new-sede-dni']").val()
					var puesto = evento.closest(".modal-content").find("input[name='new-sede-puesto']").val()
					var trabajadores = evento.closest(".modal-content").find("input[name='new-sede-trabajadores']").val()
					var encargado = evento.closest(".modal-content").find(".new-sede-encargado option:selected").val()
					var empresa_id = evento.data("empresa_id");
					rpc.query({
						model:'sede.sede',
						method:'create',
						args:[{ "name": name,"encargado": encargado,"dni": dni,"puesto": puesto,"trabajadores": trabajadores,"empresa_id":empresa_id}],
					}).then(function(){
						location.reload();
					});
				},
				change_name_empresa: function(ev) {
					var empresa_id = $(ev.target).data("empresa_id");
					var name = $(this.$el).find("input[name='name_empresa']").val();

					rpc.query({
						model: 'empresa.empresa',
						method: 'write',
						args: [[empresa_id],{"name":name}],
					}).then(function() {
						// location.reload();

					});

				},
				change_name_usuario: function(ev) {
					var usuario_id = $(ev.target).data("usuario_id");
					var name = $(this.$el).find("input[name='name_usuario']").val();

					rpc.query({
						model: 'res.users',
						method: 'write',
						args: [[usuario_id],{"name":name}],
					}).then(function() {
						// location.reload();

					});

				},
				change_correo: function(ev) {
					var empresa_id = $(ev.target).data("empresa_id");
					var correo = $(this.$el).find("input[name='correo']").val();
					rpc.query({
						model: 'empresa.empresa',
						method: 'write',
						args: [[empresa_id],{"correo":correo}],
					}).then(function() {
						// location.reload();
					});
				},
				change_telefono: function(ev) {
					var empresa_id = $(ev.target).data("empresa_id");
					var telefono = $(this.$el).find("input[name='telefono']").val();
					rpc.query({
						model: 'empresa.empresa',
						method: 'write',
						args: [[empresa_id],{"telefono":telefono}],
					}).then(function() {
						// location.reload();
					});
				},
				change_ruc: function(ev) {
					var empresa_id = $(ev.target).data("empresa_id");
					var ruc = $(this.$el).find("input[name='ruc']").val();

					rpc.query({
						model: 'empresa.empresa',
						method: 'write',
						args: [[empresa_id],{"ruc":ruc}],
					}).then(function() {
						// location.reload();

					});

				},
				change_dni_usuario: function(ev) {
					var usuario_id = $(ev.target).data("usuario_id");
					var dni = $(this.$el).find("input[name='dni']").val();

					rpc.query({
						model: 'res.users',
						method: 'write',
						args: [[usuario_id],{"dni":dni}],
					}).then(function() {
						// location.reload();

					});

				},
				click_search_user: function(ev) {
					var evento = $(ev.currentTarget)
					var usuario_id = $(ev.target).data("usuario_id")
					console.log(usuario_id)
					rpc.query({
						route:"/searchuser",
						params:{  "user_id": usuario_id    },
					}).then(function(res) {
						console.log(res)
						res.forEach(element => evento.parents('td').find(`#${element}`).prop( "checked", true ))
					})

				},
		})

		publicWidget.registry.PlantillaPermiso = publicWidget.Widget.extend({
				selector:".plantilla-permiso",
				jsLibs:["https://cdn.datatables.net/1.10.24/js/jquery.dataTables.js"],
				init: function(){
					this._super.apply(this,arguments)
					var self = this;
					var session = this.getSession()

					this.spanish = {
							"sProcessing":     "Procesando...",
							"sLengthMenu":     "Mostrar _MENU_ registros",
							"sZeroRecords":    "No se encontraron resultados",
							"sEmptyTable":     "Ningún dato disponible en esta tabla",
							"sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
							"sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
							"sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
							"sSearch":         "Buscar:",
							"sInfoThousands":  ",",
							"sLoadingRecords": "Cargando...",
							"oPaginate": {
									"sFirst":    "Primero",
									"sLast":     "Último",
									"sNext":     "Siguiente",
									"sPrevious": "Anterior"
							},
							"oAria": {
									"sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
									"sSortDescending": ": Activar para ordenar la columna de manera descendente"
							},
							"buttons": {
									"copy": "Copiar",
									"colvis": "Visibilidad"
							}
					}
				},
				start: function(){
						var self = this;
						$('#plantilla_permiso').DataTable({
							"language": self.spanish,
							 "paging": false,
							"columnDefs": [
								{ targets: 'no-sort', orderable: false }
							]
						});
				},
				events:{
		      'change .tipo-plantilla': 'change_tipo',
				},
		    change_tipo: function(ev) {
		      var evento = $(ev.currentTarget)
		      var requisito_id = evento.data("requisito_id")
		      var opcion = evento.val()
		      var radioname = evento.attr("name")
		      rpc.query({
		        model: 'requisito.requisito.transient',
		        method: 'guardar_linea',
		        args: [1, requisito_id, radioname, opcion]
		      })
		    },
		})



		publicWidget.registry.Crearusuario = publicWidget.Widget.extend({
				selector:".usuario-form",
				jsLibs:["https://cdn.datatables.net/1.10.24/js/jquery.dataTables.js"],
				init: function(){
					this._super.apply(this,arguments)
		      var self = this;
					var session = this.getSession()

					this.spanish = {
							"sProcessing":     "Procesando...",
							"sLengthMenu":     "Mostrar _MENU_ registros",
							"sZeroRecords":    "No se encontraron resultados",
							"sEmptyTable":     "Ningún dato disponible en esta tabla",
							"sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
							"sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
							"sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
							"sSearch":         "Buscar:",
							"sInfoThousands":  ",",
							"sLoadingRecords": "Cargando...",
							"oPaginate": {
									"sFirst":    "Primero",
									"sLast":     "Último",
									"sNext":     "Siguiente",
									"sPrevious": "Anterior"
							},
							"oAria": {
									"sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
									"sSortDescending": ": Activar para ordenar la columna de manera descendente"
							},
							"buttons": {
									"copy": "Copiar",
									"colvis": "Visibilidad"
							}
					}
				},
				start: function(){
						var self = this;
						$('#table_planilla').DataTable({
							"language": self.spanish,
							"columnDefs": [
								{ targets: 'no-sort', orderable: false }
							]
						});
						$('#table_servicios').DataTable({
							"language": self.spanish,
							"columnDefs": [
								{ targets: 'no-sort', orderable: false }
							]
						});
						$('.contratista').DataTable({
							"language": self.spanish
						});
				},
				events:{
					'submit .nuevo_usuario': 'click_nuevo_usuario',
					'click .nueva-sede': 'click_nueva_sede',
					'click .guardar-sede': 'click_guardar_sede',
					'click .botton-eliminar-sede': 'click_eliminar_sede',
					'click .nuevo-trabajador': 'click_nuevo_trabajador',
					'click .guardar-trabajador': 'click_guardar_trabajador',
					'click .botton-eliminar-trabajador': 'click_eliminar_trabajador',
					'click .nuevo-contratista': 'click_nuevo_contratista',
					'click .nuevo-empresa-usuario': 'click_nuevo_empresa',
					'click .nuevo-contratista-trabajador': 'click_nuevo_contratista_trabajador',
					'change #name_empresa': 'change_name_empresa',
					'change #ruc': 'change_ruc',
					'change #correo': 'change_correo',
					'change #telefon': 'change_telefono',
					'change #name_usuario': 'change_name_usuario',
					'change #dni': 'change_dni_usuario',
					'click .search-user': 'click_search_user',
					// action from signature
        	'click span[data-action=clear]': '_onClearClick',
        	'click span[data-action=undo]': '_onUndoClick',
        	'click span[data-action=save-png]': '_onSaveClick',
		      'mouseup .linea_firma': 'change_linea_firma',
		      'touchend .linea_firma': 'change_linea_firma',
				},

				dataURLToBlob: function(dataURL) {

				  var parts = dataURL.split(';base64,');
				  var contentType = parts[0].split(":")[1];
				  var raw = window.atob(parts[1]);
				  var rawLength = raw.length;
				  var uInt8Array = new Uint8Array(rawLength);

				  for (var i = 0; i < rawLength; ++i) {
				    uInt8Array[i] = raw.charCodeAt(i);
				  }

				  return new Blob([uInt8Array], { type: contentType });
				},

				download: function(dataURL, filename) {
				  if (navigator.userAgent.indexOf("Safari") > -1 && navigator.userAgent.indexOf("Chrome") === -1) {
				    window.open(dataURL);
				  } else {
				    var blob = this.dataURLToBlob(dataURL);
				    var url = window.URL.createObjectURL(blob);

				    var a = document.createElement("a");
				    a.style = "display: none";
				    a.href = url;
				    a.download = filename;

				    document.body.appendChild(a);
				    a.click();

				    window.URL.revokeObjectURL(url);
				  }
				},
				_onSaveClick: function(){
					if (this.signaturePad.isEmpty()) {
				    alert("Primero realice la firma.");
				  } else {
				    var dataURL = this.signaturePad.toDataURL();
				    this.download(dataURL, "signature.png");
					}
		  	},
				_onUndoClick: function(){
					var data = this.signaturePad.toData();
				 	if (data) {
					 data.pop(); // remove the last dot or line
					 this.signaturePad.fromData(data);
				 	}
				},
				_onClearClick: function(){
				 	this.signaturePad.clear()
				},
		    change_linea_firma: function(ev){
		      var evento = $(ev.currentTarget)
		      var usuario_id = evento.parents('.usuario_id').data("usuario_id")
		      var signature = this.signaturePad.toDataURL("image/png")
					var signature_binary = signature.split(';base64,')[1];
					const data = this.signaturePad.toData();
					console.log(data)
		      rpc.query({
		        model: 'res.users',
		        method: 'write',
		        args: [[usuario_id],{ "signature_binary":signature_binary}],
		      }).then(function() {
		        // location.reload();
		      });
					var ratio =  Math.max(window.devicePixelRatio || 1, 1);
					console.log(ratio)
		    },
				click_eliminar_trabajador:function(ev){
					var evento = $(ev.currentTarget)
					var trabajador_id = evento.data("trabajador_id")
					rpc.query({
							model:"trabajador.trabajador",
							method:"unlink",
							args:[[trabajador_id]]
					}).then(function(res){
							location.reload();
					})
				},
				click_guardar_trabajador:function(ev){
						var evento = $(ev.currentTarget)
						var id = evento.data("trabajador_id")
						var nombre = evento.closest(".modal-content").find("input[name='new-trabajador-nombres']").val()
						var dni = evento.closest(".modal-content").find("input[name='new-trabajador-dni']").val()
						var puesto = evento.closest(".modal-content").find("input[name='new-trabajador-puesto']").val()
						var tipo = evento.closest(".modal-content").find("#tipo option:selected").val()
						rpc.query({
							model:'trabajador.trabajador',
							method:'write',
							args:[[id],{"name": nombre,"dni": dni,"puesto": puesto,"tipo": tipo}],
						}).then(function(){
							location.reload();
						})
				},
				click_guardar_sede:function(ev){
						var evento = $(ev.currentTarget)
						var id = evento.data("sede_id")
						var name = evento.closest(".modal-content").find("input[name='new-sede-name']").val()
						var encargado = evento.closest(".modal-content").find(".edit-encargado option:selected").val()
						var dni = evento.closest(".modal-content").find("input[name='new-sede-dni']").val()
						var puesto = evento.closest(".modal-content").find("input[name='new-sede-puesto']").val()
						var trabajadores = evento.closest(".modal-content").find("input[name='new-sede-trabajadores']").val()
						rpc.query({
							model:'sede.sede',
							method:'write',
							args:[[id],{"name": name,"encargado": encargado,"dni": dni,"puesto": puesto,"trabajadores": trabajadores}],
						}).then(function(){
							location.reload();
						})
				},
				click_eliminar_sede:function(ev){
						var evento = $(ev.currentTarget)
						var registro_id = evento.data("sede_id")
						rpc.query({
								model:"sede.sede",
								method:"unlink",
								args:[[registro_id]]
						}).then(function(res){
								location.reload();
						})
				},
				click_nuevo_trabajador:function(ev){
					var evento = $(ev.currentTarget)
					var empresa_id = evento.data("empresa_id")
					var usuario_id = evento.data("usuario_id")
					var nombre = evento.closest(".modal-content").find("input[name='new-trabajador-nombres']").val()
					var dni = evento.closest(".modal-content").find("input[name='new-trabajador-dni']").val()
					var puesto = evento.closest(".modal-content").find("input[name='new-trabajador-puesto']").val()
					var tipo = $("#tipo option:selected").val()
					rpc.query({
						model:'trabajador.trabajador',
						method:'create',
						args:[{"name": nombre,"dni": dni,"puesto": puesto,"empresa_id": empresa_id,"tipo": tipo}],
					}).then(function(){
						location.reload()
					});
				},
				click_nuevo_contratista:function(ev){
					var evento = $(ev.currentTarget)
					var empresa_id = evento.data("empresa_id")
					var usuario_id = evento.data("usuario_id")
					var name = evento.closest(".modal-content").find("input[name='new-contratista-name']").val()
					rpc.query({
						model:'contratista.contratista',
						method:'create',
						args:[{"name": name,"empresa_id": empresa_id}],
					}).then(function(){
						location.reload()
					});
				},
				click_nuevo_contratista_trabajador:function(ev){
					var evento = $(ev.currentTarget)
					var contratista_id = evento.data("contratista_id")
					var usuario_id = evento.data("usuario_id")
					var name = evento.closest(".modal-content").find("input[name='new-contratista-name']").val()
					var dni = evento.closest(".modal-content").find("input[name='new-contratista-dni']").val()
					var correo = evento.closest(".modal-content").find("input[name='new-contratista-correo']").val()
					var telefono = evento.closest(".modal-content").find("input[name='new-contratista-telefono']").val()
					var puesto = evento.closest(".modal-content").find("input[name='new-contratista-puesto']").val()
					rpc.query({
						model:'trabajador.contratista',
						method:'create',
						args:[{"name":name,"dni":dni,"correo":correo,"telefono":telefono,"puesto":puesto,"contratisa_id": contratista_id}],
					}).then(function(){
						location.reload()
					});
				},
				click_nuevo_usuario:function(ev){
					ev.preventDefault()
					var evento = $(ev.currentTarget)
					var empresa_id = evento.data("empresa_id")
					var usuario_id = evento.data("usuario_id")
					var nombre = evento.closest(".modal-content").find("input[name='new-usuario-name']").val()
					var email = evento.closest(".modal-content").find("input[name='new-usuario-email']").val()
					var perfil = evento.closest(".modal-content").find(".perfil-usuario option:selected").val()
					var selected = []
					$('#checkboxes input:checked').each(function() {
							selected.push($(this).attr('id'));
					})
					rpc.query({
						model: 'user.transient',
						method: 'limites_permisos',
						args: [1],
					}).then(function(output) {
						if (output) {
							rpc.query({
								route:"/createuser",
								params:{  "name": nombre,
									"login": email,
									"parent_id":usuario_id,
									"planes": selected,
									"empresa_id":empresa_id,
									"perfil":perfil
								},
							}).then(function(output) {
									console.log(output)
									if(output){
										location.reload()
									}else{
										swal({
												title: "Agregar usuario",
												text: `Un usuario ya esta registrado con este correo.
												Contacta a soporte@softwaresst.com.`,
												icon: "info",
											});
									}
								});
						}else {
							swal({
									title: "Invitado",
									text: "Tu plan gratuito no permite agregar mas invitados.",
									icon: "info",
								});
						}

					});

				},
				click_nuevo_empresa:function(ev){
					var evento = $(ev.currentTarget)
					var nombre = evento.closest(".modal-content").find("input[name='new-empresa-name']").val()
					var ruc = evento.closest(".modal-content").find("input[name='new-empresa-ruc']").val()
					var correo = evento.closest(".modal-content").find("input[name='new-empresa-correo']").val()
					var telefono = evento.closest(".modal-content").find("input[name='new-usuario-telefono']").val()
						rpc.query({
							model:'permiso.create.line',
							method:'crear_empresa_usuario',
							args:[1,nombre, ruc,correo, telefono],
						}).then(function(){
							location.reload();
						});
				},
				click_nueva_sede:function(ev){
					var evento = $(ev.currentTarget)
					var name = evento.closest(".modal-content").find("input[name='new-sede-name']").val()
					var dni = evento.closest(".modal-content").find("input[name='new-sede-dni']").val()
					var puesto = evento.closest(".modal-content").find("input[name='new-sede-puesto']").val()
					var trabajadores = evento.closest(".modal-content").find("input[name='new-sede-trabajadores']").val()
					var encargado = evento.closest(".modal-content").find(".new-sede-encargado option:selected").val()
					var empresa_id = evento.data("empresa_id");
					rpc.query({
						model:'sede.sede',
						method:'create',
						args:[{ "name": name,"encargado": encargado,"dni": dni,"puesto": puesto,"trabajadores": trabajadores,"empresa_id":empresa_id}],
					}).then(function(){
						location.reload();
					});
				},
				change_name_empresa: function(ev) {
					var empresa_id = $(ev.target).data("empresa_id");
					var name = $(this.$el).find("input[name='name_empresa']").val();

					rpc.query({
						model: 'empresa.empresa',
						method: 'write',
						args: [[empresa_id],{"name":name}],
					}).then(function() {
						// location.reload();

					});

				},
				change_name_usuario: function(ev) {
					var usuario_id = $(ev.target).data("usuario_id");
					var name = $(this.$el).find("input[name='name_usuario']").val();

					rpc.query({
						model: 'res.users',
						method: 'write',
						args: [[usuario_id],{"name":name}],
					}).then(function() {
						// location.reload();

					});

				},
				change_correo: function(ev) {
					var empresa_id = $(ev.target).data("empresa_id");
					var correo = $(this.$el).find("input[name='correo']").val();
					rpc.query({
						model: 'empresa.empresa',
						method: 'write',
						args: [[empresa_id],{"correo":correo}],
					}).then(function() {
						// location.reload();
					});
				},
				change_telefono: function(ev) {
					var empresa_id = $(ev.target).data("empresa_id");
					var telefono = $(this.$el).find("input[name='telefono']").val();
					rpc.query({
						model: 'empresa.empresa',
						method: 'write',
						args: [[empresa_id],{"telefono":telefono}],
					}).then(function() {
						// location.reload();
					});
				},
				change_ruc: function(ev) {
					var empresa_id = $(ev.target).data("empresa_id");
					var ruc = $(this.$el).find("input[name='ruc']").val();

					rpc.query({
						model: 'empresa.empresa',
						method: 'write',
						args: [[empresa_id],{"ruc":ruc}],
					}).then(function() {
						// location.reload();

					});

				},
				change_dni_usuario: function(ev) {
					var usuario_id = $(ev.target).data("usuario_id");
					var dni = $(this.$el).find("input[name='dni']").val();

					rpc.query({
						model: 'res.users',
						method: 'write',
						args: [[usuario_id],{"dni":dni}],
					}).then(function() {
						// location.reload();

					});

				},
				click_search_user: function(ev) {
					var evento = $(ev.currentTarget)
					var usuario_id = $(ev.target).data("usuario_id")
					console.log(usuario_id)
					rpc.query({
						route:"/searchuser",
						params:{  "user_id": usuario_id    },
					}).then(function(res) {
						console.log(res)
						res.forEach(element => evento.parents('td').find(`#${element}`).prop( "checked", true ))
					})

				},
		})


		publicWidget.registry.EditarPlanes = publicWidget.Widget.extend({
				selector:".editar-planes",
				events:{
					'click .change-plan': 'click_change_plan',
				},
				click_change_plan: function(ev) {
					var evento = $(ev.currentTarget)
					var user_id = $(ev.target).data("user_id")
					evento.closest('.editar-planes').find('.error').html('')
					console.log($(this.$el))
					var planes = []
					$(this.$el).find('input:checkbox').each(function() {
							if($(this).is(':checked')){
								planes.push([0,$(this).attr('id')])
							}else{
								planes.push([1,$(this).attr('id')])
							}
					})
					console.log(planes)
					rpc.query({
						route:"/changeuser",
						params:{  "user_id":user_id,"matriz": planes    },
					}).then(function(res) {
						console.log(res)
						res.forEach(function(tupla){
							console.log(tupla[0])
							if(tupla[2]==1){
								console.log("CORRECTO"+tupla[0])
							}else if(tupla[2]==0){
								console.log("INCORRECTO"+tupla[0])
								var html = '<small>No puede asignar usuarios a:<br/>'+tupla[0]+' - '+tupla[1]+'</small>'
								evento.closest('.editar-planes').find('.error').append(html)
							}
						})
						setTimeout(function(){
							location.reload()
						}, 3000)
					})
				},
		})

		publicWidget.registry.EditarTrabajador = publicWidget.Widget.extend({
				selector:".editar-trabajador",
				events:{
					'click .guardar-trabajador': 'click_guardar_trabajador',
				},
				click_guardar_trabajador:function(ev){
					var nombre = $(this.$el).find("input[name='trabajador-name']").val()
					var apellido = $(this.$el).find("input[name='trabajador-apellido']").val()
					var dni = $(this.$el).find("input[name='trabajador-dni']").val()
					var empresa = $(this.$el).find("select[name='empresa-trabajador-select']").val()
					var id = parseInt($(ev.target).data("trabajador_id"));
					var name = nombre + " " + apellido
						rpc.query({
							model:'trabajador.trabajador',
							method:'write',
							args:[[id],{  "name": name,
							"nombre": nombre,
							"apellido": apellido,
							"dni": dni,
							"empresa_id":empresa}],
						}).then(function(){
							location.reload();

						});

				},
		})

		publicWidget.registry.EditarEmpresa = publicWidget.Widget.extend({
				selector:".editar-empresa",
				events:{
					'click .guardar-empresa': 'click_guardar_trabajador',
				},
				click_guardar_trabajador:function(ev){
					var nombre = $(this.$el).find("input[name='empresa-name']").val()
					var razon = $(this.$el).find("input[name='empresa-razon_social']").val()
					var ruc = $(this.$el).find("input[name='empresa-ruc']").val()
					var id = parseInt($(ev.target).data("empresa_id"));

						rpc.query({
							model:'empresa.empresa',
							method:'write',
							args:[[id],{  "name": nombre,
							"razon_social": razon,
							"ruc": ruc,
						}],
						}).then(function(){
							location.reload();

						});

				},
		})

		publicWidget.registry.Eliminarpermiso = publicWidget.Widget.extend({
				selector: ".eliminar-registro",
				events: {
					'click .botton-eliminar-permiso': 'action_eliminar_permiso',
					'click .file-gratis': 'file_gratis',
				},
				action_eliminar_permiso: function(ev) {
					var permiso_id = $(ev.target).data("permiso_id");
					rpc.query({
						model: "permiso.trabajo",
						method: "unlink",
						args: [permiso_id]
					}).then(function(res) {
						location.reload();
					});
				},
				file_gratis: function(ev) {
					swal({
						title: "Permisos de Trabajo",
						text: "No puede descargar más archivos excel con el plan Gratis.",
						icon: "info",
					});
				},

			})

		publicWidget.registry.HistoryPreventor = publicWidget.Widget.extend({
					selector: ".historial",
        	xmlDependencies:["/website_permiso/static/src/xml/xml.xml"],
					init: function() {
						this._super.apply(this, arguments);
					},
        	start:function(){
	          var desde = $("#fecha_desde").val()
	          var hasta = $("#fecha_hasta").val()
		         rpc.query({
		           model:'permiso.create.line',
		           method:'get_data_table',
		           args:[1,desde,hasta],
		         }).then(function(matriz){
		            var diario = QWeb.render("website_permiso.table_list_permiso", {matriz:  matriz});
		            $("#template-reporte-diario-render").html(diario);
		         });
        },
					events: {
						'change .fecha': 'change_fecha',
					},
					change_fecha: function(ev){
	          var desde = $("#fecha_desde").val()
	          var hasta = $("#fecha_hasta").val()
		         rpc.query({
		           model:'permiso.create.line',
		           method:'get_data_table',
		           args:[1,desde,hasta],
		         }).then(function(matriz){
		            var diario = QWeb.render("website_permiso.table_list_permiso", {matriz:  matriz});
		            $("#template-reporte-diario-render").html(diario);
		         });

					}
			})

		publicWidget.registry.GraphPreventor = publicWidget.Widget.extend({
				selector: ".grafico",
				init: function() {
					this._super.apply(this, arguments);
					var session = this.getSession()
					var fecha_desde = $('#fecha_desde').val()
					var fecha_hasta = $('#fecha_hasta').val()
					rpc.query({
						model: 'permiso.create.line',
						method: 'get_data',
						args: [1, fecha_desde, fecha_hasta],
					}).then(function(output) {
						$('#bar-chart').replaceWith($('<canvas id="bar-chart" width="800" height="450"></canvas>'));
						new Chart(document.getElementById("bar-chart"), {
							type: 'bar',
							data: {
								labels: ["Borrador", "Solicitado", "Autorizado", "Aprobado", "Cerrado", "Observado", "Cancelado"],
								datasets: [{
									label: "N°",
									backgroundColor: ["#F75448", "#7AD61D", "#8A2BE2", "#5F9EA0", "#D2691E", "#006400", "#FF8C00"],
									data: output
								}]
							},
							options: {
								legend: {
									display: false
								},
								title: {
									display: true,
									text: 'N° PERMISOS DE TRABAJO POR ESTADO'
								}
							}
						});
					})


					rpc.query({
						model: 'permiso.create.line',
						method: 'get_data_plantilla',
						args: [1, fecha_desde, fecha_hasta],
					}).then(function(output) {
						console.log(output)
						$('#circle-chart').replaceWith($('<canvas id="circle-chart" width="800" height="450"></canvas>'));
						new Chart(document.getElementById("circle-chart"), {
							type: 'pie',
							data: {
								labels: ["Trabajo en Altura", "Trabajo en Espacios Confinados", "Trabajo en Caliente", "Trabajo en Frío", "Trabajo Eléctricos"],
								datasets: [{
									label: "N°",
									backgroundColor: ["#F75448", "#7AD61D", "#8A2BE2", "#5F9EA0", "#D2691E", "#006400", "#FF8C00"],
									data: output
								}]
							},
							options: {
								legend: {
									display: false
								},
								title: {
									display: true,
									text: 'N° PERMISOS DE TRABAJO POR TIPO'
								}
							}
						});
					})
				},
				events: {
					'change .fecha': 'change_fecha',
				},
				change_fecha: function(ev){
					var fecha_desde = $('#fecha_desde').val()
					var fecha_hasta = $('#fecha_hasta').val()

					rpc.query({
						model: 'permiso.create.line',
						method: 'get_data',
						args: [1, fecha_desde, fecha_hasta],
					}).then(function(output) {
						$('#bar-chart').replaceWith($('<canvas id="bar-chart" width="800" height="450"></canvas>'));
						new Chart(document.getElementById("bar-chart"), {
							type: 'bar',
							data: {
								labels: ["Borrador", "Solicitado", "Autorizado", "Aprobado", "Cerrado", "Observado", "Cancelado"],
								datasets: [{
									label: "N°",
									backgroundColor: ["#F75448", "#7AD61D", "#8A2BE2", "#5F9EA0", "#D2691E", "#006400", "#FF8C00"],
									data: output
								}]
							},
							options: {
								legend: {
									display: false
								},
								title: {
									display: true,
									text: 'N° PERMISOS DE TRABAJO POR ESTADO'
								}
							}
						});
					})

					rpc.query({
						model: 'permiso.create.line',
						method: 'get_data_plantilla',
						args: [1, fecha_desde, fecha_hasta],
					}).then(function(output) {
						console.log(output)
						$('#circle-chart').replaceWith($('<canvas id="circle-chart" width="800" height="450"></canvas>'));
						new Chart(document.getElementById("circle-chart"), {
							type: 'pie',
							data: {
								labels: ["Trabajo en Altura", "Trabajo en Espacios Confinados", "Trabajo en Caliente", "Trabajo en Frío", "Trabajo Eléctricos"],
								datasets: [{
									label: "N°",
									backgroundColor: ["#F75448", "#7AD61D", "#8A2BE2", "#5F9EA0", "#D2691E", "#006400", "#FF8C00"],
									data: output
								}]
							},
							options: {
								legend: {
									display: false
								},
								title: {
									display: true,
									text: 'N° PERMISOS DE TRABAJO POR TIPO'
								}
							}
						});
					})
				}
		})

		publicWidget.registry.Preventor = publicWidget.Widget.extend({
				selector: "#crearpermiso",
				jsLibs: [
					'https://unpkg.com/sweetalert/dist/sweetalert.min.js',
				],
				events: {
					'submit .registro_moni': 'click_excel',
					'change .fecha': 'change_fecha',
				},
				click_excel: function(ev) {
					ev.preventDefault()
					var self = this
					var altura = $(this.$el).find("input[name='trabajo_altura']").is(":checked");
					var confinado = $(this.$el).find("input[name='trabajo_confinado']").is(":checked");
					var caliente = $(this.$el).find("input[name='trabajo_caliente']").is(":checked");
					var frio = $(this.$el).find("input[name='trabajo_frio']").is(":checked");
					var electrico = $(this.$el).find("input[name='trabajo_electrico']").is(":checked");
					var plan_id = $('#modulo-permiso-solicitar').data("plan_id");
					var sede = $(this.$el).find(".sede option:selected").val();
					var plantilla = $(this.$el).find(".plantilla option:selected").val();
					var empresa_id = $(this.$el).find(".registro_moni").data("empresa_id");

					console.log(empresa_id)
					rpc.query({
						model: 'permiso.create.line',
						method: 'limites_permisos',
						args: [1,plan_id],
					}).then(function(output) {
						if (output) {
							rpc.query({
								model: "permiso.trabajo",
								method: "create",
								args: [{
									"frio": frio,
									"electrico": electrico,
									"calor": caliente,
									"confinado": confinado,
									"altura": altura,
									"sede": sede,
									"plantilla":plantilla,
									"empresa_id":empresa_id,
								}]
							}).then(function(res) {
								location.reload();
							});
						}
						else {
							swal({
									title: "Permisos de Trabajo",
									text: "No puede crear más Permisos de Trabajo.",
									icon: "info",
								});
						}

					});

				},
			})

		publicWidget.registry.ExcelPERMISO = publicWidget.Widget.extend({
				selector: ".line-excel",
				events: {
					'click .actualizar-excel': 'click_excel',
				},
				click_excel: function(ev) {
					var permiso_id = $(ev.target).data("permiso_id");
					rpc.query({
						model: 'permiso.trabajo',
						method: 'open_word_frio',
						args: [permiso_id],
					}).then(function() {});

				},
			})

		publicWidget.registry.HideSidebar = publicWidget.Widget.extend({
			selector: ".wrapper",
			events: {
				'click #sidebarCollapse': 'change_sidebar',
			},
			change_sidebar: function(ev) {
				var evento = $(ev.currentTarget)
				var i = evento.find('i')
				var clas = i.attr('class')
				if(clas=='fa fa-arrow-left'){
					i.attr('class', 'fa fa-arrow-right')
					$('#sidebar').addClass('active')
				}else{
					i.attr('class', 'fa fa-arrow-left')
					$('#sidebar').removeClass('active')
				}
			},
		})
		publicWidget.registry.ChangeSidebar = publicWidget.Widget.extend({
			selector: ".accidente",
			events: {
				'click #sidebarCollapse1': 'change_sidebar_1',
			},
			change_sidebar_1: function(ev) {
				console.log('sidebar1')
				var evento = $(ev.currentTarget)
				var i = evento.find('i')
				var clas = i.attr('class')
				if(clas=='fa fa-arrow-left'){
					console.log('left')
					i.attr('class', 'fa fa-arrow-right')
					$('#sidebar').removeClass('active')
				}else{
					i.attr('class', 'fa fa-arrow-left')
					$('#sidebar').addClass('active')
				}
			},
		})

		publicWidget.registry.ToatNotifyPermiso = publicWidget.Widget.extend({
			selector: ".toast-notify-permisos",
			jsLibs: [
				'/website_permiso/static/src/lib/notify.js',
			],
			init: function() {
				this._super.apply(this, arguments);
			},
			start: function() {
					$.notify.addStyle('happyblue', {
						html: '<div class="toast" role="alert" aria-live="assertive" aria-atomic="true"><div class="toast-header"><i class="fa fa-pencil-square-o"></i><strong class="mr-auto">GUÍA</strong><button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close"><span aria-hidden="true"></span></button></div><div class="toast-body"><span data-notify-text/></div></div>',
						classes: {
							base: {
								"white-space": "nowrap",
								"padding": "5px"
							},
							superblue: {
								"background-color": "#54a6dd",
								"background":"lighten(#54a6dd, 30%)",
								"border-color":"lighten(#54a6dd, 20%)",
								"border-left-color":"#54a6dd",
								"color":"darken(#54a6dd, 20%)",
								 "float": "right",
							}
						}
					});
			},
		})


		publicWidget.registry.Sidebar = publicWidget.Widget.extend({
			selector: ".perfil_alumno",
			init: function(){
				console.log('INIT')
			},
			events:{
				'click .sidebar-dropdown':'click_alternativa',
				'click #close-sidebar':'click_close_sidebar',
				'click #show-sidebar':'click_show_sidebar'
			},
			click_alternativa:function(ev){
				var evento = $(ev.currentTarget)
				console.log(evento)
				if (evento.closest("li").hasClass("active")) {
					console.log('active')
					evento.closest("li").removeClass("active")
					evento.children(".sidebar-submenu").css("display", "none");
					// $(".sidebar-dropdown").removeClass("active");
					// $(ev.target).parent().removeClass("active");
				} else {
					console.log('no active')
					// $(".sidebar-dropdown").removeClass("active");
					evento.closest("li").addClass("active")
					evento.children(".sidebar-submenu").css("display", "block");
					// $(ev.target).parent().addClass("active");
				}

			},
			click_close_sidebar:function(ev){
				console.log('click_close_sidebar')
				console.log($(".page-wrapper"))
				$(".page-wrapper").removeClass("toggled");
			},
			click_show_sidebar:function(ev){
				$(".page-wrapper").addClass("toggled");

			},

		})

		publicWidget.registry.Perfilempresa = publicWidget.Widget.extend({
			selector: ".perfil-empresa",
			events: {
				'change #fullName_usuario': 'click_name_usuario',
				'change #dni': 'click_dni_usuario',
				'change #email_usuario': 'click_email_usuario',
				'change #name_empresa': 'click_name_empresa',
				'change #ruc': 'click_ruc',
			},
			click_name_usuario: function(ev) {
				var user_id = $(ev.target).data("user_id");
				var name = $(this.$el).find("input[name='fullName_usuario']").val();

				rpc.query({
					model: 'res.users',
					method: 'write',
					args: [[user_id],{"name":name}],
				}).then(function() {
					location.reload();

				});

			},

			click_email_usuario: function(ev) {
				var user_id = $(ev.target).data("user_id");
				var name = $(this.$el).find("input[name='email_usuario']").val();

				rpc.query({
					model: 'res.users',
					method: 'write',
					args: [[user_id],{"login":name,"email":name}],
				}).then(function() {
					location.reload();

				});

			},

			click_dni_usuario: function(ev) {
				var user_id = $(ev.target).data("user_id");
				var name = $(this.$el).find("input[name='dni']").val();

				rpc.query({
					model: 'res.users',
					method: 'write',
					args: [],
				}).then(function() {
					location.reload();

				});

			},

			click_name_empresa: function(ev) {
				var empresa_id = $(ev.target).data("empresa_id");
				var name = $(this.$el).find("input[name='name_empresa']").val();

				rpc.query({
					model: 'empresa.empresa',
					method: 'write',
					args: [[empresa_id],{"name":name}],
				}).then(function() {
					location.reload();

				});

			},

			click_ruc: function(ev) {
				var empresa_id = $(ev.target).data("empresa_id");
				var ruc = $(this.$el).find("input[name='ruc']").val();

				rpc.query({
					model: 'empresa.empresa',
					method: 'write',
					args: [[empresa_id],{"ruc":ruc}],
				}).then(function() {
					location.reload();

				});

			},


		})



})
