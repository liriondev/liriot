let noti = 0;
let tmp = 1;

function hashCode (str){
  let hash = 0;
  if (str.length == 0) return hash;
  for (i = 0; i < str.length; i++) {
      char = str.charCodeAt(i);
      hash = ((hash<<5)-hash)+char;
      hash = hash & hash;
  }
  return hash;
}

$(document).ready(
  function() {
    let y = 0;
    function loads(){
      if (y<=4){
        $("#load-"+y).css({
          'opacity': '1',
        });
        y++;
        setTimeout(loads, 500);
      }
    }
    loads();
  }
);

function notifi(title,msg){
  
  $('notifi').each(function(i){
    $(this).css({
      'margin-top': `${parseInt($(this).css('margin-top'))-70}px`,
      'opacity': `${parseFloat($(this).css('opacity'))-0.5}`
    });
    if(parseInt($(this).css('opacity'))==0){
      $(this).css('displanotifiy', 'none')
    }
  });
  $('body').append(`<notifi id='notifi-${noti}' class='bgc-${title}'><p onclick='close_notifi(${noti});' id='close'>x</p>${msg}</notifi>`);
  setTimeout(function(){
    $(`#notifi-${noti}`).css({
      'opacity': '1',
      'margin-top': '0'
    });
    noti++;
  }, 100); 
}

function close_notifi(index){

  $(`#notifi-${index}`).css({
    'opacity': '0',
    'margin-top': '100px'
  });
  setTimeout(function(){
    $(`#notifi-${index}`).remove()
  }, 500);

  $('notifi').each(function(i){
    if(parseInt(this.id.replace('notifi-',''))<index){
      $(this).css({
          'margin-top': `${parseInt($(this).css('margin-top'))+70}px`
      });
       if(parseFloat($(`#notifi-${parseInt(this.id.replace('notifi-',''))+1}`).css('opacity'))>=0.5) {
        $(this).css({
          'opacity': `${parseFloat($(this).css('opacity'))+0.5}`
        });
      }
      if(parseFloat($(this).css('opacity'))>=0){
        $(this).css('displanotifiy', 'block')
      }
    }
  });
}

function exec(cmd){
	$.get({
      url: '/exec',
      data: {"command": cmd},
      cache: false
    }).then(function(data){
      return data;
    });
}

function loading(url){
  $('.content').append('<div style="opacity: 0;" class="loading"><img src="static/img/grid.svg"></div>');
  setTimeout(function(){
    $('.loading').css('opacity', '1');
  },100);
  setTimeout(function(){
    location.href=url;
  	setTimeout(function(){$('.loading').remove();},500);
  },1000)
}

function load_panel(data){
 $.get({
	  url: '/get',
	  data: {'data': data}
	}).then(function(data){
	  $(".content").append(data);
	  $('.loading').css('opacity', '0');
    setTimeout(function(){$('.loading').remove();},1000);
	});
}

function reload(mod){
  exec(`loader.reload("${mod}")`);
}
function deleted(mod){
  exec(`loader.unload("${mod}");os.system("rm -rf modules/${mod}")`);
}

function login(){
  $.get({
    url: '/login',
    data: {'password': $.md5($("input[name=password]").val())}
  }).then(function(data){
    if(data=='Succesfull'){
      loading('/home');
    } else {
      notifi('danger', data);
    }
  })
}

function create(){

  let values = {
      "api_id": $("input[name=api_id]").val(),
      "api_hash": $("input[name=api_hash]").val(),
      "password": $.md5($("input[name=password]").val()),
      "language": $("select").val()
  }

  if(values['api_hash'].length && values['api_id'] && values['language'] && values['password']!="d41d8cd98f00b204e9800998ecf8427e"){
    $.get({
      url: '/create',
      data: values,
      cache: false
    }).then(function(data){
      if(data=='Succesfull'){
        notifi('succesfull', 'Created app succesfull, restart LiteBot and login for phone number.');
      }
    });
  } else {alert("Enter all data");}
  
}