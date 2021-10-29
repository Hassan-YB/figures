$(document).ready(function(){

    $('.example').DataTable({
        "bPaginate": true,
        "bLengthChange": false,
        "bFilter": true,
        "bSort": true,
        "bInfo": true,
        "bAutoWidth": false,
        "iDisplayLength": 3
    });
    

    $(".cat-btn").on("click", function() {
        var value = $(this).attr('id');
        $('.subcategory span').each(function () {
          if ($(this).hasClass(value)) 
              $(this).show();
          else $(this).hide();
      })
      $('.subcategory input').each(function () {
        if ($(this).hasClass(value)) 
            $(this).show();
        else $(this).hide();
    })
      });
    
    $('tr').click(function() {
        $('tr.active').removeClass('active');
        $(this).addClass('active');
    });
    
    $('.origin').click(
    function(){
        var that = $(this);
        $('#origin').val(that.attr('name'));
        $('#origin').addClass('active');
        
    });

    $('.character').click(
        function(){
            var that = $(this);
            $('#character').val(that.attr('name'));
            $('#character').addClass('active');
        });
    
    $('.classification').click(
        function(){
            var that = $(this);
            $('#classification').val(that.attr('name'));
            $('#classification').addClass('active');
        });
    
    $('.event').click(
        function(){
            var that = $(this);
            $('#event').val(that.attr('name'));
            $('#event').addClass('active');
        });
    
    $('.material').click(
        function(){
            var that = $(this);
            $('#material').val(that.attr('name'));
            $('#material').addClass('active');            
        });

    $('.artist').click(
        function(){
            var that = $(this);
            $('#artist').val(that.attr('name'));
            $('#artist').addClass('active');            
        });  
        
    $('.company').click(
        function(){
            var that = $(this);
            $('#company').val(that.attr('name'));
            $('#company').addClass('active');            
        });
    
    $('#add_pic').click(
        function(){
            var pic = $('<input type="file" name="pic1" accept="image/*">');
            $('.db_pictures').append(pic);
        });

    // $('input[type="checkbox"]').click(
    //     function(){
    //         $(this).val("True");
    //     }); 

    $("#form_id").on('submit', function(event) {
        event.preventDefault(); 
        var pr = $("#price").val();
        var rn = $("#inputGroupSelect01").find(":selected").text();
        var br = $("#barcode").val();
        var ct = $("#catalog").val();
        var inf = $("#info").val();
        var dt = $("#date").val();
        $.ajax({
            type: "POST",
            url: "/releases/",
            data:{
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                  price:pr,
                  run:rn,
                  barcode:br,
                  catalog:ct,
                  info:inf,
                  date:dt,
            },
            success: function(data) {
              if (data['success'])
              var val = data['object'];
              var dt = data['date'];
              var input = $('<input type="text" name="date" id="release" value="'+val+'" placeholder="Release object" hidden>');
              var input1 = $('<button class="btn btn-success mr-4 ml-3 ">'+dt+'</button>');
              $(".releases").append(input,input1);
            }
        }); 
   });


   $("#form_id_1").on('submit', function(event) {
    event.preventDefault();
    var nm = $("#name").val();
    var org = $("#original").val();
    var obj =$("#url").val();
    $.ajax({
        type: "POST",
        url: "/entries/",
        data:{
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
              name:nm,
              original:org,
              object:obj,
        },
        success: function(data) {
          if (data['success']){
            alert(data['msg'])
          }
            
        }
    }); 
});

  });
