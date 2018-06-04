$.postJSON = function(url, data, success=null) {
    return $.ajax(url, {
                        type: 'POST',
                        data: JSON.stringify(data),
                        contentType: 'application/json',
                        success: success
                       });
};

var realistic_rendering = {};
var normal_rendering = {};

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
  }

  transform += " scale(" + scale + ")";
  var label = parseInt(scale*100);

  element.find('svg').css({ transform: transform });
  element.find('.scale').text(label);
}

// set preview svg scale to fit into its box if transform is not set
function scaleAllSvg() {
    $('.page').each(function() {
      if( $(this).find('.inksimulation svg').css('transform') == 'none') {
        scaleSVG($(this).find('.inksimulation'), 'fit');
      }
    });
}

var saveTimerHandles = {};

function setSVGTransform(figure, transform) {
    var field_name = $(figure).data('field-name');
    var scale = transform.match(/-?[\d\.]+/g)[0];
    figure.find('svg').css({ transform: transform });
    figure.find(".scale").text(parseInt(scale*100));

    // avoid spamming updates
    if (saveTimerHandles[field_name] != null)
        clearTimeout(saveTimerHandles[field_name]);

    saveTimerHandles[field_name] = setTimeout(function() {
        $.postJSON('/settings/' + field_name, {value: transform});
    }, 250);
}

$(function() {
  setTimeout(ping, 1000);
  setPageNumbers();

  /* SCALING AND MOVING SVG  */

  /* Mousewheel scaling */
  $('figure.inksimulation').on( 'DOMMouseScroll mousewheel', function (e) {
    if(e.ctrlKey == true) {

      var svg       = $(this).find('svg');
      var transform = svg.css('transform').match(/-?[\d\.]+/g);
      var scale     = parseFloat(transform[0]);

      if (e.originalEvent.detail > 0 || e.originalEvent.wheelDelta < 0) {
        // scroll down = zoom out
        scale *= 0.97;
        if (scale < 0.01)
            scale = 0.01;
      } else {
        //scroll up
        scale *= 1.03;
      }

      // set modified scale
      transform[0] = scale;
      transform[3] = scale;

      setSVGTransform($(this), 'matrix(' + transform + ')');

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
    var p0 = { x: e.pageX, y: e.pageY };
    var start_transform = $(this).find('svg').css('transform').match(/-?[\d\.]+/g);
    var start_offset = { x: parseFloat(start_transform[4]), y: parseFloat(start_transform[5]) };

    $(this).css({cursor: 'move'});
    $(this).on('mousemove', function(e) {
          var p1 = { x: e.pageX, y: e.pageY };
          // set modified translate
          var transform = $(this).find('svg').css('transform').match(/-?[\d\.]+/g);
          transform[4] = start_offset.x + (p1.x - p0.x);
          transform[5] = start_offset.y + (p1.y - p0.y);

          // I'd ike to use setSVGTransform() here but this code runs many
          // times per second and it's just too CPU-intensive.
          $(this).find('svg').css({transform: 'matrix(' + transform + ')'});
      });
  }).on('mouseup', function(e) {
    $(this).css({cursor: 'auto'});
    $(this).data('p0', null);
    $(this).off('mousemove');

    // set it using setSVGTransform() to ensure that it's saved to the server
    setSVGTransform($(this), $(this).find('svg').css('transform'));
  });

  // ignore mouse events on the buttons (Fill, 100%, Apply to All)
  $('figure.inksimulation div').on('mousedown mouseup', function(e) {
    e.stopPropagation();
  });

  /* Apply transforms to All */
  $('button.svg-apply').click(function() {
    var transform = $(this).parent().siblings('svg').css('transform');
    $('.inksimulation').each(function() {
      setSVGTransform($(this), transform);
    })
  });

  /* Contendeditable Fields */

  $('[contenteditable="true"]').on('focusout', function() {
        /* change svg scale */
    var content = $(this).html();
    var field_name = $(this).attr('data-field-name');
    if(field_name == 'svg-scale') {
      var scale     = parseInt(content);
      var svg       = $(this).parent().siblings('svg');
      var transform = svg.css('transform').match(/-?[\d\.]+/g);

      transform[0] = scale / 100;
      transform[3] = scale / 100;
      svg.css({ transform: 'matrix(' + transform + ')' });
    } else {
      /* When we focus out from a contenteditable field, we want to
       * set the same content to all fields with the same classname */
      $('[data-field-name="' + field_name + '"]').html(content);
      $.postJSON('/settings/' + field_name, {value: content});
    }
  });

  // load up initial metadata values
  $.getJSON('/settings', function(settings) {
    $.each(settings, function(field_name, value) {
        $('[data-field-name="' + field_name + '"]').each(function(i, item) {
            var item = $(item);
            if (item.is(':checkbox')) {
                item.prop('checked', value).trigger('initialize');
            } else if (item.is('img')) {
                item.attr('src', value);
            } else if (item.is('select')) {
                item.val(value).trigger('initialize');
            } else if (item.is('figure.inksimulation')) {
                setSVGTransform(item, value);
            } else {
                item.text(value);
            }
        });
    });

    $.getJSON('/realistic', function(realistic_data) {
      // realistic_rendering is global
      realistic_rendering = realistic_data;
    });

    // wait until page size is set (if they've specified one) and then scale SVGs to fit
    setTimeout(function() { scaleAllSvg() }, 500);
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

       /* Chrome and Firefox both have a rule: scripts can only close windows
        * that they opened.  Chrome seems to have an exception for windows that
        * were opened by an outside program, so the above works fine.  Firefox
        * steadfastly refuses to allow us to close the window, so we'll tell
        * the user (in their language) that they can close it.
        */
       setTimeout(function() {
           document.open();
           document.write("<html><body>" + data + "</body></html>");
           document.close();
       }, 1000);
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
  $('select#printing-size').on('change initialize', function(){
    $('.page').toggleClass('a4', $(this).find(':selected').val() == 'a4');
  }).on('change', function() {
    $.postJSON('/settings/paper-size', {value: $(this).find(':selected').val()});
  });

  // Thread Palette
  $('select#thread-palette').change(function(){
    $('.modal').show();
  }).on('update', function() {
    $(this).data('current-value', $(this).find(':selected').val());
  }).trigger('update');

  $('#modal-yes').on('click', function(){
    $("select#thread-palette").trigger("update");
    $('.modal').hide();
    var body = {'name': $('select#thread-palette').find(':selected').val()};
    $.postJSON('/palette', body, function() {
      $.getJSON('/threads', function(threads) {
        console.log("threads: " + JSON.stringify(threads));
        $.each(threads, function(i, thread) {
          console.log("doing: " + JSON.stringify(thread));
          $('[data-field-name="color-' + thread.hex + '"]').text(thread.name);
          var thread_description = thread.manufacturer;
          if (thread.number) {
            thread_description += " #" + thread.number;
          }
          $('[data-field-name="thread-' + thread.hex + '"]').text(thread_description);
        });
      });
    });
  });

  $('#modal-no').on('click', function(){
    var select = $("select#thread-palette");
    select.find('[value="' + select.data('current-value') + '"]').prop('selected', true);
    $('.modal').hide();
  });

  // View selection checkboxes
  $(':checkbox.view').on('change initialize', function() {
    var field_name = $(this).attr('data-field-name');

    $('.' + field_name).toggle($(this).prop('checked'));
    setPageNumbers();
  }).on('change', function() {
    var field_name = $(this).attr('data-field-name');
    $.postJSON('/settings/' + field_name, {value: $(this).prop('checked')});
  });

  // Realistic rendering checkboxes
  $(':checkbox.realistic').on('change', function(e) {
    console.log("realistic rendering checkbox");

    var item = $(this).data('field-name');
    var figure = $(this).closest('figure');
    var svg = figure.find('svg');
    var transform = svg.css('transform');
    var checked = $(this).prop('checked');

    console.log("" + item + " " + transform);

    // do this later to allow this event handler to return now,
    // which will cause the checkbox to be checked or unchecked
    // immediately even if SVG rendering takes awhile
    setTimeout(function() {
      if (checked) {
        if (!(item in normal_rendering)) {
          normal_rendering[item] = svg[0].outerHTML;
        }
        svg[0].outerHTML = realistic_rendering[item];
      } else {
        svg[0].outerHTML = normal_rendering[item];
      }
      // can't use the svg variable here because setting outerHTML created a new tag
      figure.find('svg').css({transform: transform});
    }, 100);

    e.stopPropagation();
    return true;
  });

  $('button.svg-realistic').click(function(e){
    $(this).find('input').click();
  });

  // Logo
  $('#logo-picker').change(function(e) {
      var file = e.originalEvent.currentTarget.files[0];
      var reader = new FileReader();
      reader.onloadend = function() {
          var data = reader.result;
          $('figure.brandlogo img').attr('src', data);
          $.postJSON('/settings/logo', {value: data});
      };
      reader.readAsDataURL(file);
  });

  // "save as defaults" button
  $('#save-settings').click(function(e) {
      var settings = {};
      settings["client-overview"] = $("[data-field-name='client-overview']").is(':checked');
      settings["client-detailedview"] = $("[data-field-name='client-detailedview']").is(':checked');
      settings["operator-overview"] = $("[data-field-name='operator-overview']").is(':checked');
      settings["operator-detailedview"] = $("[data-field-name='operator-detailedview']").is(':checked');
      settings["paper-size"] = $('select#printing-size').find(':selected').val();

      var logo = $("figure.brandlogo img").attr('src');
      if (logo.startsWith("data:")) {
          settings["logo"] = logo;
      }

      $.postJSON('/defaults', {'value': settings});
  });
});
