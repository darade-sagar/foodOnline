
// Add to cart using AJAX requests
$(document).ready(function(){
    // add to cart
    $('.add_to_cart').on('click',function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type:'GET',
            url: url,
            success : function(response){
                console.log(response);
                if(response.status == 'Login_Required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                }
                else if(response.status == 'Failed'){
                    swal(response.message,'','error')
                    
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)

                    // subtotal and grand total.
                    applyCartAmount(
                        response.cart_ammount['subtotal'],
                        response.cart_ammount['tax_dict'],
                        response.cart_ammount['grand_total'],
                    )
                    
                }
            }
        })
    })

    
    // place the cart item quantity on load
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        
        $('#'+the_id).html(qty)
    })

    // decrease cart
    $('.decrease_cart').on('click',function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');

        $.ajax({
            type:'GET',
            url: url,
            success : function(response){
                console.log(response);
                if(response.status == 'Login_Required'){
                    swal(response.message,'','info').then(function(){
                        window.location = '/login';
                    })
                }
                else if(response.status == 'Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty)
                    
                    if(response.qty<=0){
                        document.getElementById("cart-item-"+cart_id).remove()
                        checkEmptyCart()
                        swal('Success', 'Item has been Removed!', 'success')
                    }

                    // subtotal and grand total.
                    applyCartAmount(
                        response.cart_ammount['subtotal'],
                        response.cart_ammount['tax_dict'],
                        response.cart_ammount['grand_total'],
                    )
                }
            }
        })
    })

    // delete cart
    $('.delete_cart').on('click',function(e){
        e.preventDefault();
        
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type:'GET',
            url: url,
            success : function(response){
                console.log(response);
                if(response.status == 'Failed'){
                    swal(response.message,'','error')
                }else{
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    // subtotal and grand total.
                    removeCartItem(0,cart_id)
                    applyCartAmount(
                        response.cart_ammount['subtotal'],
                        response.cart_ammount['tax_dict'],
                        response.cart_ammount['grand_total'],
                        )
                    swal(response.status, response.message, 'success')
                    checkEmptyCart()

                }
            }
        })
    })

    // delete cart element
    function removeCartItem(cartItemQty, cart_id){
        if (cartItemQty <= 0){
            // remove cart item
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }

    // check if cart is empty
    function checkEmptyCart(){
        var cart_counter = document.getElementById('cart_counter').innerHTML
        if (cart_counter==0){
            document.getElementById('empty-cart').style.display = "block";
        }
    }

    // apply cart ammount
    function applyCartAmount(subtotal,tax_dict,grand_total){
        if(window.location.pathname == '/cart/'){
            $('#subtotal').html(subtotal)
            $('#total').html(grand_total)
            
            for(key1 in tax_dict){
                for(key2 in tax_dict[key1]){
                    $('#tax-'+key1).html(tax_dict[key1][key2])
                }
            }
            
        }
    }


    // add opening hours
    $('.add_hour').on('click',function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value 
        var from_hour = document.getElementById('id_from_hour').value 
        var to_hour = document.getElementById('id_to_hour').value 
        var is_closed = document.getElementById('id_is_closed').checked 
        var url = document.getElementById('add_hour_url').value 
        var csrf_token = $('input[name=csrfmiddlewaretoken]').val()
        console.log(day,from_hour,to_hour,is_closed, csrf_token)

        if(is_closed){
            is_closed = 'true'
            condition = day!=''
        }
        else{
            is_closed = 'false'
            condition = day!='' && from_hour != '' && to_hour != ''
        }
        
        if(eval(condition)){
            $.ajax({
                type: "POST",
                url: url,
                data:{
                    'day':day,
                    'from_hour':from_hour,
                    'to_hour':to_hour,
                    'is_closed':is_closed,
                    'csrfmiddlewaretoken':csrf_token,
                },
                success: function(response){
                    
                    if(response.status=='success'){
                        if(response.is_closed == 'Closed'){
                            html = "<tr id='hour-"+response.id+"'><td><b>"+response.day+"</b></td><td> Closed </td><td><a href='#' class='remove-hour' data-url='/vendor/opening-hours/remove/"+response.id+"'>Remove</a></td></tr>"
                        }else{
                            html = "<tr id='hour-"+response.id +"'><td><b>"+response.day+"</b></td><td>"+response.from_hour+"-"+response.to_hour+"</td><td><a href='#' class='remove-hour' data-url='/vendor/opening-hours/remove/"+response.id+"'>Remove</a></td></tr>"
                        }
                        $(".opening_hours").append(html)
                        document.getElementById('opening_hours').reset();
                        
                    }else{
                        console.log(response.status)
                        swal("Current day is already added!",'Please remove it and try again...','error');
                    }

                    console.log(response)
                },
            })
        }
        else{
            swal('Please fill all fields','','info')
        }
        
    })
    
    // remove opening hours
    $(document).on('click','.remove-hour', function(e){
        e.preventDefault();
        url = $(this).attr('data-url');
        console.log(url)

        $.ajax({
            type:"GET",
            url: url,
            success: function(response){
                console.log(response)
                if(response.status=='success'){
                    document.getElementById('hour-'+response.id).remove();
                }
                swal("Day has been removed","","success");
            }
        })

    })

    // newsletter short description field counter
    $('textarea').keyup(function(){
        if(this.value.length > 1000){
            return false;
        }
        $("#short_desc").html("<span class='float-right' style='color:red; text-size:8px'>Character Limit : " + (1000 - this.value.length)+"</span>");
    })
})


