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
});

