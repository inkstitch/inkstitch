function ping() {
  $.get("/ping")
   .done(function() { setTimeout(ping, 1000) })
   .fail(function() { $('#errors').attr('class', 'show') });
}

// set pagenumbers
function setPageNumbers() {
  var totalPageNum = $('body').find('.page:visible').length;
  $('span.total-page-num').text(totalPageNum);
  $( '.page:visible span.page-num' ).each(function( index ) {
    $(this).text(index + 1);
  });
}

// set preview svg scale to fit into its box
function scaleInksimulation() {
  $('.inksimulation').each(function() {
    var scale = Math.min(
      $(this).width() / $(this).find('svg').width(),    
      $(this).height() / $(this).find('svg').height()
    );

    // center the SVG
    transform = "translate(-50%, -50%)";

    if(scale <= 1) {
      transform += " scale(" + scale + ")";
      label = parseInt(scale*100);
    } else {
      label = "100";
    }

    $(this).find('svg').css({ transform: transform });
    $(this).find('figcaption span').text(label);
  });
}

$(function() {
  setTimeout(ping, 1000);
  setPageNumbers();
  scaleInksimulation();
  
    /* Mousewheel scaling */
  $('figure.inksimulation').on( 'DOMMouseScroll mousewheel', function ( event ) {
    var transform = $(this).find('svg').css('transform').match(/-?[\d\.]+/g);
    var scale = parseFloat(transform[0]);
    if( scale > 0.01 && (event.originalEvent.detail > 0 || event.originalEvent.wheelDelta < 0)) {
      // scroll down
      scale -= 0.01;
    } else {
      //scroll up
      scale += 0.01;
    }
    // set modified scale
    transform[0] = scale;
    transform[3] = scale;
    $(this).find('svg').css({ transform: 'matrix(' + transform + ')' });
    
    // set scale caption text
    $(this).find("span").text(parseInt(scale*100));

    //prevent page fom scrolling
    return false;
  });
  
  /* Drag SVG */
  $('figure.inksimulation').on('mousedown', function(e) {
      $(this).data('p0', { x: e.pageX, y: e.pageY });
      $(this).css({cursor: 'move'});
  }).on('mouseup', function(e) {
      var p0 = $(this).data('p0'),
        p1 = { x: e.pageX, y: e.pageY },
        d = Math.sqrt(Math.pow(p1.x - p0.x, 2) + Math.pow(p1.y - p0.y, 2));
      if (d > 4) {
        var transform = $(this).find('svg').css('transform').match(/-?[\d\.]+/g);
        transform[4] = parseFloat(transform[4]) + parseFloat(p1.x-p0.x);
        transform[5] = parseFloat(transform[5]) + parseFloat(p1.y-p0.y);
        // set modified translate
        $(this).find('svg').css({ transform: 'matrix(' + transform + ')' });
        $(this).css({cursor: 'auto'});
      }
  })  
  
  /* Contendeditable Fields */
  
  // When we focus out from a contenteditable field, we want to
  // set the same content to all fields with the same classname
  document.querySelectorAll('[contenteditable="true"]').forEach(function(elem) {
    elem.addEventListener('focusout', function() {
        var content = $(this).html();
        var field_name = $(this).attr('data-field-name');
        $('[data-field-name="' + field_name + '"]').html(content);
    });
  });
  
  $('[contenteditable="true"]').keypress(function(e) {
      if (e.which == 13) {
          // pressing enter defocuses the element
          this.blur();

          // also suppress the enter keystroke to avoid adding a new line
          return false;
      } else {
          return true;
      }
    });
  
  
  /* Settings Bar */
  
  $('button.close').click(function() {
    $.post('/shutdown', {})
     .done(function(data) {
       window.close();
    });
  });

  $('button.print').click(function() {
    // printing halts all javascript activity, so we need to tell the backend
    // not to shut down until we're done.
    $.get("/printing/start")
     .done(function() {
        window.print();
        $.get("/printing/end");
     });
  });

  $('button.settings').click(function(){
    $('#settings-ui').show();
  });

  $('#close-settings').click(function(){
      $('#settings-ui').hide();
  });
  
  /* Settings */
  
  // Paper Size
  $('select#printing-size').change(function(){
    $('.page').toggleClass('a4');
  });
  
  //Checkbox
  $(':checkbox').change(function() {
    $('.' + this.id).toggle();
    setPageNumbers();
    scaleInksimulation();
  });
  
});

