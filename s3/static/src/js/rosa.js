odoo.define("s3.registro_rosa",function(require){
    'use strict';

    var publicWidget = require("web.public.widget");
    var rpc = require("web.rpc");
    var core = require('web.core');
    var QWeb = core.qweb;
    var _t = core._t;

    publicWidget.registry.FormEditableSaveRosa = publicWidget.Widget.extend({
      selector:"#formulario_editar_field_rosa",
      events:{
            'click .botton-guardar-field-data':"action_guardar_field_data",
            "change #image_input":"click_image_input",
            "change .field-odoo":"click_change_field",
      },
      click_change_field: async function(ev){
        var form = $('#formulario_editar_field_rosa');
        var tabla_1 = [[2,	2,	3,	4,	5,	6,	7,	8],
                   [2,	2,	3,	4,	5,	6,	7,	8],
                   [3,	3,	3,	4,	5,	6,	7,	8],
                   [4,	4,	4,	4,	5,	6,	7,	8],
                   [5,	5,	5,	5,	5,	7,	8,	9],
                   [6,	6,	6,	7,	7,	8,	8,	9],
                   [7,	7,	7,	8,	8,	9,	9,	9]];
        var tabla_2 = [[1,	1,	1,	2,	3,	4,	5,	6],
                   [1,	1,	2,	2,	3,	4,	5,	6],
                   [1,	2,	2,	3,	3,	4,	6,	7],
                   [2,	2,	3,	3,	4,	5,	6,	8],
                   [3,	3,	4,	4,	5,	6,	7,	8],
                   [4,	4,	5,	5,	6,	7,	8,	9],
                   [5,	5,	6,	7,	8,	8,	9,	9]];
        var tabla_3 = [[1,	1,	1,	2,	3,	4,	5,	6],
                   [1,	1,	2,	3,	4,	5,	6,	7],
                   [1,	2,	2,	3,	4,	5,	6,	7],
                   [2,	3,	3,	3,	5,	6,	7,	8],
                   [3,	4,	4,	5,	5,	6,	7,	8],
                   [4,	5,	5,	6,	6,	7,	8,	9],
                   [5,	6,	6,	7,	7,	8,	8,	9],
                   [6,	7,	7,	8,	8,	9,	9,	9]];
        var tabla_4 = [[1,	2,	3,	4,	5,	6,	7,	8,	9],
                   [2,	2,	3,	4,	5,	6,	7,	8,	9],
                   [3,	3,	3,	4,	5,	6,	7,	8,	9],
                   [4,	4,	4,	4,	5,	6,	7,	8,	9],
                   [5,	5,	5,	5,	5,	6,	7,	8,	9],
                   [6,	6,	6,	6,	6,	6,	7,	8,	9],
                   [7,	7,	7,	7,	7,	7,	7,	8,	9],
                   [8,	8,	8,	8,	8,	8,	8,	8,	9],
                   [9,	9,	9,	9,	9,	9,	9,	9,	9]];
        var tabla_final = [[1,	2,	3,	4,	5,	6,	7,	8,	9,	10],
                       [2,	2,	3,	4,	5,	6,	7,	8,	9,	10],
                       [3,	3,	3,	4,	5,	6,	7,	8,	9,	10],
                       [4,	4,	4,	4,	5,	6,	7,	8,	9,	10],
                       [5,	5,	5,	5,	5,	6,	7,	8,	9,	10],
                       [6,	6,	6,	6,	6,	6,	7,	8,	9,	10],
                       [7,	7,	7,	7,	7,	7,	7,	8,	9,	10],
                       [8,	8,	8,	8,	8,	8,	8,	8,	9,	10],
                       [9,	9,	9,	9,	9,	9,	9,	9,	9,	10],
                       [10, 10,	10,	10,	10,	10,	10,	10,	10,	10]];
        var silla_puntuacion = 0;
        var altura_longitud_puntuacion = 0;
        var respaldo_reposabrazos_puntuacion = 0;
        //altura
        var silla_altura_puntuacion = 0;
        var silla_altura_igual = $("input[name='silla_altura_igual']").is(":checked");
        var silla_altura_menor = $("input[name='silla_altura_menor']").is(":checked");
        var silla_altura_mayor = $("input[name='silla_altura_mayor']").is(":checked");

        var silla_altura_sin_contacto = $("input[name='silla_altura_sin_contacto']").is(":checked");
        var silla_altura_no_ajustable = $("input[name='silla_altura_no_ajustable']").is(":checked");
        var silla_altura_sin_espacio = $("input[name='silla_altura_sin_espacio']").is(":checked");
        // if ((ev.target.name == 'silla_altura_igual') || (ev.target.name == 'silla_altura_menor') || (ev.target.name == 'silla_altura_mayor') ){
        //   if (silla_altura_igual && (ev.target.name == 'silla_altura_igual')){
        //     silla_altura_menor = false;
        //     silla_altura_mayor =false;
        //     $("input[name='silla_altura_menor']").prop('checked',false);
        //     $("input[name='silla_altura_mayor']").prop('checked',false);
        //
        //   }else if (silla_altura_menor && (ev.target.name == 'silla_altura_menor')){
        //     silla_altura_igual = false;
        //     silla_altura_mayor =false;
        //     $("input[name='silla_altura_igual']").prop('checked',false);
        //     $("input[name='silla_altura_mayor']").prop('checked',false);
        //
        //   }else if (silla_altura_mayor && (ev.target.name == 'silla_altura_mayor')){
        //     silla_altura_igual = false;
        //     silla_altura_menor =false;
        //     $("input[name='silla_altura_igual']").prop('checked',false);
        //     $("input[name='silla_altura_menor']").prop('checked',false);
        //   }else {
        //     silla_altura_igual = true;
        //     silla_altura_menor =false;
        //     silla_altura_mayor =false;
        //     $("input[name='silla_altura_igual']").prop('checked',true);
        //     $("input[name='silla_altura_menor']").prop('checked',false);
        //     $("input[name='silla_altura_mayor']").prop('checked',false);
        //   }
        //
        // }




        //longitud
        var silla_longitud_puntuacion = 0;

        var silla_longitud_igual = $("input[name='silla_longitud_igual']").is(":checked");
        var silla_longitud_menor = $("input[name='silla_longitud_menor']").is(":checked");
        var silla_longitud_mayor = $("input[name='silla_longitud_mayor']").is(":checked");
        var silla_longitud_no_ajustable = $("input[name='silla_longitud_no_ajustable']").is(":checked");

        // if ((ev.target.name = 'silla_longitud_igual') || (ev.target.name == 'silla_longitud_menor') || (ev.target.name == 'silla_longitud_mayor')){
        //   if (silla_longitud_igual && (ev.target.name = 'silla_longitud_igual')){
        //     silla_longitud_menor = false;
        //     silla_longitud_mayor =false;
        //     $("input[name='silla_longitud_menor']").prop('checked',false);
        //     $("input[name='silla_longitud_mayor']").prop('checked',false);
        //
        //   }else if (silla_longitud_menor && (ev.target.name == 'silla_longitud_menor')){
        //     silla_longitud_igual = false;
        //     silla_longitud_mayor =false;
        //     $("input[name='silla_longitud_igual']").prop('checked',false);
        //     $("input[name='silla_longitud_mayor']").prop('checked',false);
        //
        //   }else if (silla_longitud_mayor && (ev.target.name == 'silla_longitud_mayor')){
        //     silla_longitud_igual = false;
        //     silla_longitud_menor =false;
        //     $("input[name='silla_longitud_igual']").prop('checked',false);
        //     $("input[name='silla_longitud_menor']").prop('checked',false);
        //   }else{
        //     silla_longitud_igual = true;
        //     silla_longitud_menor =false;
        //     silla_longitud_mayor =false;
        //     $("input[name='silla_longitud_igual']").prop('checked',true);
        //     $("input[name='silla_longitud_menor']").prop('checked',false);
        //     $("input[name='silla_longitud_mayor']").prop('checked',false);
        //   }
        // }


        //respaldo
        var silla_respaldo_puntuacion = 0;

        var silla_respaldo_recto = $("input[name='silla_respaldo_recto']").is(":checked");
        var silla_respaldo_plano = $("input[name='silla_respaldo_plano']").is(":checked");
        var silla_respaldo_obtuso = $("input[name='silla_respaldo_obtuso']").is(":checked");
        var silla_respaldo_agudo = $("input[name='silla_respaldo_agudo']").is(":checked");
        var silla_respaldo_ajustable = $("input[name='silla_respaldo_ajustable']").is(":checked");
        var silla_respaldo_mesa = $("input[name='silla_respaldo_mesa']").is(":checked");
        //
        // if ((ev.target.name == 'silla_respaldo_recto') || (ev.target.name == 'silla_respaldo_plano') || (ev.target.name == 'silla_respaldo_obtuso')){
        //   if (silla_respaldo_recto && (ev.target.name == 'silla_respaldo_recto')){
        //     silla_respaldo_plano = false;
        //     silla_respaldo_obtuso =false;
        //     silla_respaldo_agudo =false;
        //     $("input[name='silla_respaldo_plano']").prop('checked',false);
        //     $("input[name='silla_respaldo_obtuso']").prop('checked',false);
        //     $("input[name='silla_respaldo_agudo']").prop('checked',false);
        //
        //   }else if (silla_respaldo_plano && (ev.target.name == 'silla_respaldo_plano')){
        //     silla_respaldo_recto = false;
        //     silla_respaldo_obtuso =false;
        //     silla_respaldo_agudo =false;
        //     $("input[name='silla_respaldo_recto']").prop('checked',false);
        //     $("input[name='silla_respaldo_obtuso']").prop('checked',false);
        //     $("input[name='silla_respaldo_agudo']").prop('checked',false);
        //
        //   }else if (silla_respaldo_obtuso && (ev.target.name == 'silla_respaldo_obtuso')){
        //     silla_respaldo_plano = false;
        //     silla_respaldo_recto = false;
        //     silla_respaldo_agudo =false;
        //     $("input[name='silla_respaldo_plano']").prop('checked',false);
        //     $("input[name='silla_respaldo_recto']").prop('checked',false);
        //     $("input[name='silla_respaldo_agudo']").prop('checked',false);
        //   }
        //   else if (silla_respaldo_agudo && (ev.target.name == 'silla_respaldo_agudo')){
        //     silla_respaldo_plano = false;
        //     silla_respaldo_recto = false;
        //     silla_respaldo_obtuso =false;
        //     $("input[name='silla_respaldo_plano']").prop('checked',false);
        //     $("input[name='silla_respaldo_recto']").prop('checked',false);
        //     $("input[name='silla_respaldo_obtuso']").prop('checked',false);
        //   }else{
        //     silla_respaldo_agudo =false;
        //     silla_respaldo_plano = false;
        //     silla_respaldo_recto = true;
        //     silla_respaldo_obtuso =false;
        //     $("input[name='silla_respaldo_plano']").prop('checked',false);
        //     $("input[name='silla_respaldo_recto']").prop('checked',true);
        //     $("input[name='silla_respaldo_obtuso']").prop('checked',false);
        //     $("input[name='silla_respaldo_agudo']").prop('checked',false);
        //   }
        //
        // }


        //reposabrazos
        var silla_reposabrazos_puntuacion = 0;

        var silla_reposabrazos_linea = $("input[name='silla_reposabrazos_linea']").is(":checked");
        var silla_reposabrazos_alto = $("input[name='silla_reposabrazos_alto']").is(":checked");
        var silla_reposabrazos_dura = $("input[name='silla_reposabrazos_dura']").is(":checked");
        var silla_reposabrazos_separados = $("input[name='silla_reposabrazos_separados']").is(":checked");
        var silla_reposabrazos_ajustable = $("input[name='silla_reposabrazos_ajustable']").is(":checked");
        var silla_reposabrazos_duracion = $("select[name='silla_reposabrazos_duracion']").val();
        // if ((ev.target.name == 'silla_reposabrazos_linea') || (ev.target.name == 'silla_reposabrazos_alto')){
        //   if (silla_reposabrazos_linea && (ev.target.name == 'silla_reposabrazos_linea')){
        //     silla_reposabrazos_alto =false;
        //     $("input[name='silla_reposabrazos_alto']").prop('checked',false);
        //
        //   }else if (silla_reposabrazos_alto && (ev.target.name == 'silla_reposabrazos_alto')){
        //     silla_reposabrazos_linea =false;
        //     $("input[name='silla_reposabrazos_linea']").prop('checked',false);
        //
        //   }else{
        //     silla_reposabrazos_linea =true;
        //     silla_reposabrazos_alto =false;
        //     $("input[name='silla_reposabrazos_alto']").prop('checked',false);
        //     $("input[name='silla_reposabrazos_linea']").prop('checked',true);
        //
        //   }
        //
        // }


        var monitor_telefono_puntuacion = 0;

        //monitor
        var monitor_puntuacion = 0;
        var monitor_ideal = $("input[name='monitor_ideal']").is(":checked");
        var monitor_bajo = $("input[name='monitor_bajo']").is(":checked");
        var monitor_alto = $("input[name='monitor_alto']").is(":checked");
        var monitor_centrada = $("input[name='monitor_centrada']").is(":checked");
        var monitor_reflejos = $("input[name='monitor_reflejos']").is(":checked");
        var monitor_documentos = $("input[name='monitor_documentos']").is(":checked");
        var monitor_alejado = $("input[name='monitor_alejado']").is(":checked");
        var monitor_duracion = $("select[name='monitor_duracion']").val();

        // if ((ev.target.name == 'monitor_ideal') || (ev.target.name == 'monitor_bajo') || (ev.target.name == 'monitor_alto')){
        //   if (monitor_ideal && (ev.target.name == 'monitor_ideal')){
        //     monitor_bajo =false;
        //     monitor_alto =false;
        //     $("input[name='monitor_bajo']").prop('checked',false);
        //     $("input[name='monitor_alto']").prop('checked',false);
        //   }else if (monitor_bajo && (ev.target.name == 'monitor_bajo')){
        //     monitor_ideal =false;
        //     monitor_alto =false;
        //     $("input[name='monitor_ideal']").prop('checked',false);
        //     $("input[name='monitor_alto']").prop('checked',false);
        //   }else if (monitor_alto && (ev.target.name == 'monitor_alto')){
        //     monitor_ideal =false;
        //     monitor_bajo =false;
        //     $("input[name='monitor_ideal']").prop('checked',false);
        //     $("input[name='monitor_bajo']").prop('checked',false);
        //   }else{
        //     monitor_ideal =true;
        //     monitor_alto =false;
        //     monitor_bajo =false;
        //     $("input[name='monitor_ideal']").prop('checked',true);
        //     $("input[name='monitor_alto']").prop('checked',false);
        //     $("input[name='monitor_bajo']").prop('checked',false);
        //   }
        // }


        //telefono
        var telefono_puntuacion = 0;
        var telefono_manos = $("input[name='telefono_manos']").is(":checked");
        var telefono_alejado = $("input[name='telefono_alejado']").is(":checked");
        var telefono_cuello = $("input[name='telefono_cuello']").is(":checked");
        var telefono_mano_libre = $("input[name='telefono_mano_libre']").is(":checked");
        var telefono_duracion = $("select[name='telefono_duracion']").val();
        // if ( (ev.target.name == 'telefono_manos') || (ev.target.name == 'telefono_alejado')){
        //   if (telefono_manos && (ev.target.name == 'telefono_manos')){
        //     telefono_alejado =false;
        //     $("input[name='telefono_alejado']").prop('checked',false);
        //   }else if (telefono_alejado && (ev.target.name == 'telefono_alejado')){
        //     telefono_manos =false;
        //     $("input[name='telefono_manos']").prop('checked',false);
        //   }else{
        //     telefono_manos =true;
        //     telefono_alejado =false;
        //     $("input[name='telefono_alejado']").prop('checked',false);
        //     $("input[name='telefono_manos']").prop('checked',true);
        //   }
        //
        // }



        var teclado_raton_puntuacion = 0;
        //teclado
        var teclado_puntuacion = 0;

        var teclado_munecas_rectas = $("input[name='teclado_munecas_rectas']").is(":checked");
        var teclado_munecas_extendidas = $("input[name='teclado_munecas_extendidas']").is(":checked");
        var teclado_munecas_desviadas = $("input[name='teclado_munecas_desviadas']").is(":checked");
        var teclado_alto = $("input[name='teclado_alto']").is(":checked");
        var teclado_alcanza = $("input[name='teclado_alcanza']").is(":checked");
        var teclado_ajustable = $("input[name='teclado_ajustable']").is(":checked");
        var teclado_duracion = $("select[name='teclado_duracion']").val();
        // if ((ev.target.name == 'teclado_munecas_rectas') || (ev.target.name == 'teclado_munecas_extendidas')){
        //   if (teclado_munecas_rectas && (ev.target.name == 'teclado_munecas_rectas')){
        //     teclado_munecas_extendidas =false;
        //     $("input[name='teclado_munecas_extendidas']").prop('checked',false);
        //   }else if (teclado_munecas_extendidas && (ev.target.name == 'teclado_munecas_extendidas')){
        //     teclado_munecas_rectas =false;
        //     $("input[name='teclado_munecas_rectas']").prop('checked',false);
        //   }else{
        //     teclado_munecas_rectas =true;
        //     teclado_munecas_extendidas =false;
        //     $("input[name='teclado_munecas_extendidas']").prop('checked',false);
        //     $("input[name='teclado_munecas_rectas']").prop('checked',true);
        //   }
        // }


        //raton
        var raton_puntuacion = 0;

        var raton_linea = $("input[name='raton_linea']").is(":checked");
        var raton_lejos = $("input[name='raton_lejos']").is(":checked");
        var raton_diferentes = $("input[name='raton_diferentes']").is(":checked");
        var raton_estirar = $("input[name='raton_estirar']").is(":checked");
        var raton_reposamos = $("input[name='raton_reposamos']").is(":checked");
        var raton_duracion = $("select[name='raton_duracion']").val();

        // if ( (ev.target.name == 'raton_linea') || (ev.target.name == 'raton_lejos')){
        //   if (raton_linea && (ev.target.name == 'raton_linea')){
        //     raton_lejos =false;
        //     $("input[name='raton_lejos']").prop('checked',false);
        //
        //   }else if (raton_lejos && (ev.target.name == 'raton_lejos')){
        //     raton_linea =false;
        //     $("input[name='raton_linea']").prop('checked',false);
        //
        //   }else{
        //     raton_linea =true;
        //     raton_lejos =false;
        //     $("input[name='raton_lejos']").prop('checked',true);
        //     $("input[name='raton_linea']").prop('checked',true);
        //
        //   }
        // }





        var resultado_grupo_a = 0;
        var resultado_grupo_b = 0;
        var resultado_final = 0;
        var nivel_riesgo = "";
        var situacion_trabajo = "";
        var cumple = "";

        var cont_si = 0;
        var cont_no = 0;
        var cont = 0;

        // _compute_puntuacion_silla_altura
        cont = 0;
        if (silla_altura_igual){
          cont = 1;
        }
        if (silla_altura_menor){
          cont = 2;
        }
        if (silla_altura_mayor){
          cont = 2;
        }
        if (silla_altura_sin_contacto){
          cont = 3;
        }
        if (silla_altura_no_ajustable){
          cont = cont + 1;
        }
        if (silla_altura_sin_espacio){
          cont = cont + 1;
        }
        silla_altura_puntuacion = cont;

        // _compute_puntuacion_silla_longitud
        cont = 0;
        if (silla_longitud_igual)
            {cont = 1;}
        if (silla_longitud_menor)
          {  cont = 2;}
        if (silla_longitud_mayor)
            {cont = 2;}
        if (silla_longitud_no_ajustable)
          {  cont = cont + 1;}

        silla_longitud_puntuacion = cont;

        // _compute_puntuacion_silla_respaldo
        cont = 0;
        if (silla_respaldo_recto)
            {cont = 1;}
        if (silla_respaldo_plano)
          {  cont = 2;}
        if (silla_respaldo_obtuso)
          {  cont = 2;}
        if (silla_respaldo_agudo)
            {cont = 2;}
        if (silla_respaldo_ajustable)
          {  cont = cont + 1;}
        if (silla_respaldo_mesa)
            {cont = cont + 1;}
        silla_respaldo_puntuacion = cont;

        // _compute_puntuacion_silla_reposabrazos

        cont = 0;
        if (silla_reposabrazos_linea){
          cont = 1;
        }
        if (silla_reposabrazos_alto){
          cont = 2;
        }
        if (silla_reposabrazos_dura){
          cont = 2;
        }
        if (silla_reposabrazos_separados){
          cont = cont + 1;
        }
        if (silla_reposabrazos_ajustable){
          cont = cont + 1;
        }

        silla_reposabrazos_puntuacion = cont;

        // _compute_silla
        altura_longitud_puntuacion = silla_altura_puntuacion + silla_longitud_puntuacion;
        respaldo_reposabrazos_puntuacion = silla_respaldo_puntuacion + silla_reposabrazos_puntuacion;

        // _compute_puntuacion_monitor
        cont = 0;
        if (monitor_ideal)
            {cont = 1;}
        if (monitor_bajo)
            {cont = 2;}
        if (monitor_alto)
            {cont = 2;}
        if (monitor_centrada)
            {cont = cont + 1;}
        if (monitor_reflejos)
            {cont = cont + 1;}
        if (monitor_documentos)
            {cont = cont + 1;}
        if (monitor_alejado)
            {cont = cont + 1;}

        monitor_puntuacion = cont;

        if (monitor_duracion == 'menor')
            {monitor_puntuacion = cont - 1;}
        if (monitor_duracion == 'entre')
            {monitor_puntuacion = cont;}
        if (monitor_duracion == 'mayor')
            {monitor_puntuacion = cont + 1;}

        //_compute_puntuacion_telefono
        cont = 0;
        if (telefono_manos)
            {cont = 1;}
        if (telefono_alejado)
            {cont = 2;}
        if (telefono_cuello)
            {cont = cont + 2;}
        if (telefono_mano_libre)
            {cont = cont + 1;}
        telefono_puntuacion = cont;

        if (telefono_duracion == 'menor')
          { telefono_puntuacion = cont - 1;}
        if (telefono_duracion == 'entre')
          { telefono_puntuacion = cont;}
        if (telefono_duracion == 'mayor')
            {telefono_puntuacion = cont + 1;}

        // _compute_puntuacion_teclado

        cont = 0;
        if (teclado_munecas_rectas)
            {cont = 1;}
        if (teclado_munecas_extendidas)
            {cont = 2;}
        if (teclado_munecas_desviadas)
            {cont = cont + 1;}
        if (teclado_alto)
           {cont = cont + 1;}
        if (teclado_alcanza)
           {cont = cont + 1;}
        if (teclado_ajustable)
            {cont = cont + 1;}

        teclado_puntuacion = cont;
        if (teclado_duracion == 'menor')
            {teclado_puntuacion = cont - 1;}
        if (teclado_duracion == 'entre')
          {  teclado_puntuacion = cont;}
        if (teclado_duracion == 'mayor')
          {  teclado_puntuacion = cont + 1;}

        // _compute_puntuacion_raton

        cont = 0;

        if (raton_linea)
            {cont = 1;}
        if (raton_lejos)
            {cont = 2;}
        if (raton_diferentes)
            {cont = cont + 2;}
        if (raton_estirar)
            {cont = cont + 1;}
        if (raton_reposamos)
            {cont = cont + 1;}

        raton_puntuacion = cont

        if (raton_duracion == 'menor')
            {raton_puntuacion = cont - 1;}
        if (raton_duracion == 'entre')
            {raton_puntuacion = cont;}
        if (raton_duracion == 'mayor')
          {  raton_puntuacion = cont + 1;}

        // _compute_silla_tabla
        if (altura_longitud_puntuacion >= 2 && respaldo_reposabrazos_puntuacion >= 2){
          silla_puntuacion = tabla_1[altura_longitud_puntuacion - 2][respaldo_reposabrazos_puntuacion - 2];
        }
        if (silla_reposabrazos_duracion == 'menor')
            {silla_puntuacion = silla_puntuacion - 1;}
        if (silla_reposabrazos_duracion == 'entre')
            {silla_puntuacion = silla_puntuacion;}
        if (silla_reposabrazos_duracion == 'mayor')
            {silla_puntuacion = silla_puntuacion + 1;}

        resultado_grupo_a = silla_puntuacion;

        // _compute_monitor_telefono_tabla
        if (telefono_puntuacion >= 0 && monitor_puntuacion >= 0){
          monitor_telefono_puntuacion = tabla_2[telefono_puntuacion][monitor_puntuacion];
        }

        // _compute_teclado_raton_tabla
        if (raton_puntuacion >= 0 && teclado_puntuacion >= 0){
          teclado_raton_puntuacion = tabla_3[raton_puntuacion][teclado_puntuacion];
        }
        // _compute_resultado_b
        if (teclado_raton_puntuacion >= 1 && monitor_telefono_puntuacion >= 1){
          resultado_grupo_b = tabla_4[teclado_raton_puntuacion-1][monitor_telefono_puntuacion-1];
        }
        // _compute_resultado_final
        if (resultado_grupo_b >= 1 && resultado_grupo_a >= 1){
          resultado_final = tabla_final[resultado_grupo_b - 1][resultado_grupo_a - 1];
        }
        // _compute_resultado_rosa
        if (resultado_final == 1)
            {nivel_riesgo = 'INAPRECIABLE';
            cumple = "SÍ CUMPLE";
            situacion_trabajo = 'Situaciones de trabajo aceptables';}
        else if (resultado_final == 2)
            {nivel_riesgo = 'INAPRECIABLE';
            cumple = "SÍ CUMPLE";
            situacion_trabajo = 'Situaciones de trabajo aceptables';}
        else if (resultado_final == 3)
            {nivel_riesgo = 'BAJO';
            cumple = "SÍ CUMPLE";
            situacion_trabajo = 'Situaciones de trabajo aceptables';}
        else if (resultado_final == 4)
            {nivel_riesgo = 'BAJO';
            cumple = "SÍ CUMPLE";
            situacion_trabajo = 'Situaciones de trabajo aceptables';}
        else if (resultado_final == 5)
            {nivel_riesgo = 'MEDIO';
            cumple = "SÍ CUMPLE";
            situacion_trabajo = 'Situacion de tarea de prioridad  Medio de intervención ergonómica';}
        else if (resultado_final == 6)
            {nivel_riesgo = 'MEDIO';
            cumple = "SÍ CUMPLE";
            situacion_trabajo = 'Situacion de tarea de prioridad  Medio de intervención ergonómica';}
        else if (resultado_final == 7)
            {nivel_riesgo = 'ALTO';
            cumple = "NO CUMPLE";
            situacion_trabajo = 'Situacion de tarea de prioridad  Alto de intervención ergonómica';}
        else if (resultado_final == 8)
            {nivel_riesgo = 'ALTO';
            cumple = "NO CUMPLE";
            situacion_trabajo = 'Situacion de tarea de prioridad  Alto de intervención ergonómica';}
        else if( resultado_final == 9)
            {nivel_riesgo = 'MUY ALTO';
            cumple = "NO CUMPLE";
            situacion_trabajo = 'Situacion de tarea de prioridad  Muy alto de intervención ergonómica';}
        else if (resultado_final == 10)
            {nivel_riesgo = 'MUY ALTO';
            cumple = "NO CUMPLE";
            situacion_trabajo = 'Situacion de tarea de prioridad  Muy alto de intervención ergonómica';}
        if (cumple == "SÍ CUMPLE")
            {cont_si = 1;}
        else
            {cont_no = 1;}
        cont = 1;
        $("span[name='silla_altura_puntuacion']").text(silla_altura_puntuacion);
        $("span[name='silla_longitud_puntuacion']").text(silla_longitud_puntuacion);
        $("span[name='silla_respaldo_puntuacion']").text(silla_respaldo_puntuacion);
        $("span[name='silla_reposabrazos_puntuacion']").text(silla_reposabrazos_puntuacion);
        $("span[name='altura_longitud_puntuacion']").text(altura_longitud_puntuacion);
        $("span[name='respaldo_reposabrazos_puntuacion']").text(respaldo_reposabrazos_puntuacion);
        $("span[name='silla_puntuacion']").text(silla_puntuacion);
        $("span[name='monitor_telefono_puntuacion']").text(monitor_telefono_puntuacion);
        $("span[name='monitor_puntuacion']").text(monitor_puntuacion);
        $("span[name='telefono_puntuacion']").text(telefono_puntuacion);
        $("span[name='teclado_raton_puntuacion']").text(teclado_raton_puntuacion);
        $("span[name='teclado_puntuacion']").text(teclado_puntuacion);
        $("span[name='raton_puntuacion']").text(raton_puntuacion);
        $("span[name='resultado_grupo_a']").text(resultado_grupo_a);
        $("span[name='resultado_grupo_b']").text(resultado_grupo_b);
        $("span[name='resultado_final']").text(resultado_final);
        $("span[name='nivel_riesgo']").text(nivel_riesgo);
        $("span[name='situacion_trabajo']").text(situacion_trabajo);





      },
      action_guardar_field_data: async function(ev){
          var form = $('#formulario_editar_field_rosa');
          var model = $('#formulario_editar_field_rosa').data("model_id");
          var record_id = $('#formulario_editar_field_rosa').data("record_id");
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
        var record_id = $('#formulario_editar_field_rosa').data("record_id");
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
                    model:"rosa.rosa",
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
