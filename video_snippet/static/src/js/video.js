odoo.define("video_snippet.video",function(require){
    'use strict';

    var publicWidget = require("web.public.widget")
    var core = require("web.core")
    var rpc = require("web.rpc")
    var Widget = require("web.Widget")
    var qweb = core.qweb
    var ajax = require("web.ajax")

    var VideoWidget = Widget.extend({
        template:"video_snippet.video_1",
        xmlDependencies:["/video_snippet/static/src/xml/video.xml"],
        events:{
            // 'click .change_video': 'change_video'
        },
        init:function(parent,params){
            this._super()
            this.id = params.id
            this.nombre = params.nombre
            this.description = params.description
            this.url = params.url
            this.modulo = params.modulo
            this.website_url = params.website_url
            this.sale_qty = params.sale_qty
            this.imagen = `/web/image?model=product.product&id=${this.id}&field=image_512`
            this.parent = parent
        },
        add_video_line:function(video_id,qty,tipo){

        },
        // _render:function(){
        //     var product = qweb.render("video_snippet.video_1",
        //                     {   title:this.nombre,
        //                     })
        //     $(this.$el).html(product)
        // }
    })

    publicWidget.registry.SectionProducts = publicWidget.Widget.extend({
        selector:".o_video_section",
        start:function(){
            this._fetch().then(_.bind(this._render,this))
        },
        events:{
            'click .outside': 'outside',
            'click .compra': 'click_compra',
            'keydown': 'evento_esc'
        },
        click_compra: function(ev){
            var objeto = $('li.o_wsale_my_cart ').find('.my_cart_quantity')
            var evento = $(ev.currentTarget)
            var product_id = evento.data("product_id")
            var i = evento.find('i')
            var plan_id
            var plan_id2
            if(product_id == 1){
              plan_id=1
              plan_id2=2
            }else if (product_id == 2) {
              plan_id=3
              plan_id2=4
            }else if (product_id == 3) {
              plan_id=5
              plan_id2=6
            }else if (product_id == 4) {
              plan_id=7
              plan_id2=8
            }else if (product_id == 5) {
              plan_id=9
              plan_id2=10
            }
            console.log(product_id)
            console.log(plan_id)
            if(i.hasClass('fa fa-shopping-cart fa-2x')){
              rpc.query({
                  route:"/shop/cart/update_json_v2",
                  params:{
                    product_id:product_id,
                    set_qty:1,
                    plan_id:plan_id,
                  }
              }).then(function(res){
                i.attr('class', 'fa fa-check-circle fa-2x')
                objeto.html(res.cart_quantity)
              })
            }else{
              rpc.query({
                  route:"/shop/cart/update_json_v2",
                  params:{
                    product_id:product_id,
                    set_qty:0,
                    plan_id:plan_id,
                  }
              }).then(function(res){
                // i.attr('class','fa fa-shopping-cart fa-2x')
                // location.href="/shop/payment"
              })

              rpc.query({
                  route:"/shop/cart/update_json_v2",
                  params:{
                    product_id:product_id,
                    set_qty:0,
                    plan_id:plan_id2,
                  }
              }).then(function(res){
                i.attr('class','fa fa-shopping-cart fa-2x')
                if(res.cart_quantity){
                  objeto.html(res.cart_quantity)
                }else{
                  objeto.html(0)
                }
              })
          }
        },
        outside: async function(ev){
        //   console.log($(event.target))
            if($(ev.target).hasClass('modal')){
              var evento = $(ev.currentTarget)
              var iframe = evento.find("iframe")
              iframe.attr("src", iframe.attr("src").replace("autoplay=1", "autoplay=0"));
            }else if ($(ev.target).hasClass('overlay')){
              var evento = $(ev.currentTarget)
              var iframe = evento.find("iframe")
              iframe.attr("src", iframe.attr("src").replace("autoplay=0", "autoplay=1"));
            }
        },
        evento_esc: function(ev){
            var iframe = $(ev.target).find("iframe")
            if(ev.keyCode == 27){
              iframe.attr("src", iframe.attr("src").replace("autoplay=1", "autoplay=0"));
            }
        },
        _fetch:function(){
            return  this._rpc({
                route:"/get_videos",
                params:{}
            }).then(function(res){
                return res
            }).catch(function(res){
                return []
            })
        },
        _render:function(products){
            var self = this
            $(".o_video_section").empty()
            _.each(products,function(product){
                var p = new VideoWidget(self,product)
                p.appendTo('.o_video_section')
            })
        }
    })

    publicWidget.registry.PaymentCulqi = publicWidget.Widget.extend({
        selector:".o_payment_culqi",
        events:{
        'click .btn_send_payment':'_send_payment',
        'change .selectplan':'_change_select',
        'click .deleteplan':'_delete_plan',

        'focus input':"_focus",
        'blur input':"_blur",

        'keydown input[name="expiration"]':"_valideKeyExpirationdate",
        'keypress input[name="expiration"]':"_press_expiration_date",
        'keydown input[name="cvv"]':"_valideKeycvv",
        'keydown input[name="card_number"]':"_valideKeyCardNumber",

        'keypress input':"_validate",
        'keyup input':"_validate",
        'keydown input':"_validate"
        },
        init:function(){
            var self = this;
            $(".btn_send_payment").attr("disabled",true)
            this._super.apply(this, arguments);
            self.form = {
                email :{validate:false,value:"",pattern:["^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"]},
                cvv :{validate:false,value:"",pattern:["^[0-9]{3,4}$"]},
                expiration :{validate:false,value:"",pattern:["^(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})$", 'g']},
                card_number :{validate:false,value:"",pattern:["^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$"]}
            }
        },
        _focus:function(ev){
            console.log(ev.target.value)
            console.log(this.form[ev.target.id].pattern[0])
            var value = (ev.target.value?ev.target.value:"").match(new RegExp(this.form[ev.target.id].pattern[0]));
            // console.log("_focus",ev.target.value,value)
            $(ev.target).css("border",value?"solid 2px #00dd8d":"solid 2px #572364")
        },
        _blur:function(ev){
            var value = (ev.target.value?ev.target.value:"").match(new RegExp(this.form[ev.target.id].pattern[0]));
            // console.log("_blur",ev.target.value,value)
            $(ev.target).css("border",value?"solid 2px #00dd8d":"solid 2px #FF5C63")
        },
        _press_expiration_date:function(ev){
            if(ev.target.value.length == 2){
                $(ev.target).val(ev.target.value+"/")
            }
        },
        _valideKeyCardNumber:function(event){
            if((event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105) && event.keyCode !==190  && event.keyCode !==110 && event.keyCode !==8 && event.keyCode !==9  ){
                return false;
            }
        },
        _valideKeycvv:function(event){
            if((event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105) && event.keyCode !==190  && event.keyCode !==110 && event.keyCode !==8 && event.keyCode !==9  ){
                return false;
            }
        },
        _valideKeyExpirationdate:function(event){
            if((event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105) && event.keyCode !==190  && event.keyCode !==110 && event.keyCode !==8 && event.keyCode !==9  ){
                return false;
            }
        },
        _change_select:function(ev){
            console.log('CHANGESELECT')
            var evento = $(ev.currentTarget)
            var plan_id = evento.val()
            var product_id = evento.parents('.product_id').data("product_id")
            // var precio = $('.price_sale').html("123")
            console.log(product_id)
            rpc.query({
                route:"/shop/changeplan",
                params:{
                    product_id,
                    plan_id:plan_id,
                }
            }).then(function(output) {
              console.log(output);
              evento.parents('.product_id').find('.oe_currency_value').html(output[0])
              $('#total').find('.oe_currency_value').html(output[1])
            });
        },
        _delete_plan:function(ev){
            console.log('DELETEDSELECT')
            var evento = $(ev.currentTarget)
            // var plan_id = evento.val()
            var product_id = evento.parents('.product_id').data("product_id")
            var plan_id = $( ".selectplan option:selected" ).val();
            // var precio = $('.price_sale').html("123")
            console.log(product_id)
            rpc.query({
                route:"/shop/cart/update_json_v2",
                params:{
                  product_id:product_id,
                  set_qty:0,
                  plan_id:parseInt(plan_id),
                }
            }).then(function(res){
              location.reload()
            })
        },
        _validate:function(ev){
            // console.log(this.email_validate , this.cvv_validate , this.date_validate , this.card_number_validate)
            // this.form[ev.target.id].value = ev.target.value
            this.form[ev.target.id].validate = (ev.target.value?ev.target.value:"").match(new RegExp(this.form[ev.target.id].pattern[0]))?true:false;
            if(this.form.email.validate && this.form.cvv.validate && this.form.expiration.validate && this.form.card_number.validate){
                $(".btn_send_payment").attr("disabled",false)
            }else{
                $(".btn_send_payment").attr("disabled",true)
            }
            return true
        },
        _send_payment:function(ev){
            var self = this
            var culqipk = $(self.$el).find("#culqipk").val();
            var email = $(self.$el).find("#email").val()
            var card_number= $(self.$el).find("#card_number").val()
            var expiration = $(self.$el).find("#expiration").val()
            var expiration_month = expiration.substr(0,2)
            var expiration_year = `20${expiration.substr(3,5)}`
            var cvv = $(self.$el).find("#cvv").val()

            var data = {
                email,
                card_number,
                expiration_month,
                expiration_year,
                cvv
            }
            console.log(data)
            var loading = `<div class="spinner-border" role="status">
                                <span class="sr-only">Loading...</span>
                            </div>`
            $(self.$el).find(".shop_payment_message").html($(loading))
            $(".btn_send_payment").attr("disabled",true)
            $.ajax({
                type:"POST",
                url:"https://secure.culqi.com/v2/tokens",
                dataType: 'json',
                data:JSON.stringify(data),
                headers:{"Content-type": "application/json","authorization": `Bearer ${culqipk}`}
            }).then(function(res){
                console.log(res)
                console.log(res.id)
                var token = res.id
                ajax.post("/sendpayment",{email,token})
                    .then(function(res){
                        $(self.$el).find(".shop_payment_message").html(res)
                        $(".btn_send_payment").attr("disabled",true)
                        location.href="/usuarios"
                    })
            }).catch(function(err){
                if(err.responseJSON["object"] === "error"){
                    $(self.$el).find(".shop_payment_message").html(err.responseJSON["user_message"])
                    $(".btn_send_payment").attr("disabled",true)
                }
            })
        }
    })
})
