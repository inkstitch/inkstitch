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

$(function() {
  setTimeout(ping, 1000);
  
  setPageNumbers();
  
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
  
  /* When we focus out from a contenteditable field, we want to
     set the same content to all fields with the same classname */
  document.querySelectorAll('[contenteditable="true"]').forEach(function(elem) {
    elem.addEventListener('focusout', function() {
        var content = $(this).html();
        var style = $(this).attr('class');
        $('.' + style).html(content);
    });
  });
  
  // Prevent line breaks in contenteditable fields
  $('[contenteditable="true"]').keypress(function(e){ return e.which != 13; });
  
  // Printing Size
  $('select#printing-size').change(function(){
    $('.page').toggleClass('a4');
  });
  
  //Checkbox
  $(':checkbox').change(function() {
    $('.' + this.id).toggle();
    setPageNumbers();
  });
  
});

