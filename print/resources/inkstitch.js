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

// Scale SVG (fit || full size)
function scaleSVG(element, scale = 'fit') {
  
  // always center svg
  transform = "translate(-50%, -50%)";
  
  if(scale == 'fit') {
    var scale = Math.min(
      element.width() / element.find('svg').width(),    
      element.height() / element.find('svg').height()
    );
    // Do not scale to more than 100%
    scale = (scale <= 1) ? scale : 1;
  }
  
  transform += " scale(" + scale + ")";
  var label = parseInt(scale*100);

  element.find('svg').css({ transform: transform });
  element.find('figcaption span').text(label);
}

// set preview svg scale to fit into its box if transform is not set
function scaleAllSvg() {
    $('.page').each(function() {
      if( $(this).css('display') != 'none' ) {
        if( $(this).find('.inksimulation svg').css('transform') == 'none') {
          if( $(this).find('.inksimulation span').text() == '') {
            scaleSVG($(this).find('.inksimulation'));
          } 
          else {
            var transform = $(this).find('.inksimulation span').text();
            var scale = transform.match(/-?[\d\.]+/g)[0];
            $(this).find('.inksimulation svg').css({ transform: transform });
            $(this).find('.inksimulation span').text(parseInt(scale*100));
          }
        }
      }
    });
}

$(function() {
  setTimeout(ping, 1000);
  setPageNumbers();
  scaleAllSvg();
  
  /* SCALING AND MOVING SVG  */
  
  /* Mousewheel scaling */
  $('figure.inksimulation').on( 'DOMMouseScroll mousewheel', function (e) {
    if(event.ctrlKey == true) {
    
      var svg       = $(this).find('svg');
      var transform = svg.css('transform').match(/-?[\d\.]+/g);
      var scale     = parseFloat(transform[0]);
      
      if( scale > 0.01 && (e.originalEvent.detail > 0 || e.originalEvent.wheelDelta < 0)) {
        // scroll down
        scale -= 0.01;
      } else {
        //scroll up
        scale += 0.01;
      }
      
      // set modified scale
      transform[0] = scale;
      transform[3] = scale;
      svg.css({ transform: 'matrix(' + transform + ')' });
      
      // set scale caption text
      $(this).find("span").text(parseInt(scale*100));

      //prevent page fom scrolling
      return false;
    }
  });
  
  /* Fit SVG */
  $('button.svg-fit').click(function() {
    var svgfigure = $(this).closest('figure');
    scaleSVG(svgfigure, 'fit');
  });
  
  /* Full Size SVG */
  $('button.svg-full').click(function() {
    var svgfigure = $(this).closest('figure');
    scaleSVG(svgfigure, '1');
  });
  
  /* Drag SVG */
  $('figure.inksimulation').on('mousedown', function(e) {
      $(this).data('p0', { x: e.pageX, y: e.pageY });
      $(this).css({cursor: 'move'});
  }).on('mouseup', function(e) {
      $(this).css({cursor: 'auto'});
      var p0 = $(this).data('p0'),
        p1 = { x: e.pageX, y: e.pageY },
        d = Math.sqrt(Math.pow(p1.x - p0.x, 2) + Math.pow(p1.y - p0.y, 2));
      if (d > 4) {
        var transform = $(this).find('svg').css('transform').match(/-?[\d\.]+/g);
        transform[4] = parseFloat(transform[4]) + parseFloat(p1.x-p0.x);
        transform[5] = parseFloat(transform[5]) + parseFloat(p1.y-p0.y);
        // set modified translate
        $(this).find('svg').css({ transform: 'matrix(' + transform + ')' });
      }
  })
  
  /* Apply transforms to All */
  $('button.svg-apply').click(function() {
    var transform = $(this).parent().siblings('svg').css('transform');
    var scale = transform.match(/-?[\d\.]+/g)[0];
    $('.inksimulation').each(function() {
      $(this).find('svg').css({ transform: transform });
      $(this).find("span").text(parseInt(scale*100));
      
    })
  });
  
  /* Contendeditable Fields */
  
  document.querySelectorAll('[contenteditable="true"]').forEach(function(elem) {
    elem.addEventListener('focusout', function() {
        /* change svg scale */
        var content    = $(this).html();
        var field_name = $(this).attr('data-field-name');
        if(field_name == 'svg-scale') {
          var scale     = parseInt(content);
          var svg       = $(this).parent().siblings('svg');
          var transform = svg.css('transform').match(/-?[\d\.]+/g);
          
          transform[0] = scale / 100;
          transform[3] = scale / 100;
          svg.css({ transform: 'matrix(' + transform + ')' });
        }
        /* When we focus out from a contenteditable field, we want to
           set the same content to all fields with the same classname */
        else {
          $('[data-field-name="' + field_name + '"]').html(content);
        }
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
    scaleAllSvg();
  });
  
});

