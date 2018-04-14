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
      label = parseInt(scale*100) + '%';
    } else {
      label = "100%";
    }

    $(this).find('svg').css({ transform: transform });
    $(this).find('figcaption span').text(label);
  });
}

$(function() {
  setTimeout(ping, 1000);
  setPageNumbers();
  scaleInksimulation();

  /* Contendeditable Fields */

  // When we focus out from a contenteditable field, we want to
  // set the same content to all fields with the same classname
  $('[contenteditable="true"]').on('focusout', function() {
    var content = $(this).html();
    var field_name = $(this).attr('data-field-name');
    $('[data-field-name="' + field_name + '"]').text(content);
    $.post('/metadata/' + field_name + '/set', {value: content});
  });

  // load up initial metadata values
  $.getJSON('/metadata', function(metadata) {
      $.each(metadata, function(field_name, value) {
          $('[data-field-name="' + field_name + '"]').text(value);
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

