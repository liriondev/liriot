let noti = 0;

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
    
  $('body').append(`<notifi id='notifi-${noti}'><p id='title'>${title}</p><button onclick='close_notifi(${noti});' id='close'>✘</button>${msg}</notifi>`);
  setTimeout(function(){
    $(`#notifi-${noti}`).css({
      'opacity': '1',
      'margin-top': '0'
    });
    noti++;
  }, 500);
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
        'margin-top': `${parseInt($(this).css('margin-top'))+70}px`,
        'opacity': `${parseFloat($(this).css('opacity'))+0.5}`
      });
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
  $('.content').append('<div style="opacity: 0;" class="loading"><div dot-color="red" class="dot-spin"></div></div>');
  setTimeout(function(){
    $('.loading').css('opacity', '1');
  },500);
  setTimeout(function(){
    location.href=url;
  },1500)
}

function load_panel(data){
  $.get({
    url: '/get',
    data: {'data': data}
  }).then(function(data){
    $(".content").append(data);
    $('.loading').css('opacity', '0');
    setTimeout(function(){$('.loading').remove();},1500);
  });
}

function mod_info(index){
  if($(`.card[id=info-${index}]`).css('height')=='40px'){
    $(`.card[id=info-${index}]`).css('height', 'max-content');
  } else {
    $(`.card[id=info-${index}]`).css('height', '40px');
  }
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
      notifi('Error', data);
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
        notifi('Info', 'Created app succesfull, restart LiteBot and login for phone number.');
      }
    });
  } else {alert("Enter all data");}
  
}