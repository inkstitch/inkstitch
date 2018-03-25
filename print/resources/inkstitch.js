function ping() {
  console.info("pinging");
  $.get("/ping")
   .done(function() { console.info("ping successful"); setTimeout(ping, 1000) })
   .fail(function() { console.info("ping error"); $('#errors').attr('class', 'show') });
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
    window.print();
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

