$(function() {
  
  // If the window is closed, we still want to be sure to shutdown the server
  window.addEventListener('beforeunload', setTimeout(function() { 
    $.post('/shutdown', {})
  }), 1000);
  
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

