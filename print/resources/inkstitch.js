$(function() {
  
  // If the window is closed, we still want to be sure to shutdown the server
  window.addEventListener('beforeunload', function() {
    $.post('/shutdown', {})
  });

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
  
});

