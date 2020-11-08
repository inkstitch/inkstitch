var electron = require('electron');

$.postJSON = function(url, data, success=null) {
    return $.ajax(url, {
                        type: 'POST',
                        data: JSON.stringify(data),
                        contentType: 'application/json',
                        success: success
                       });
};

var realistic_rendering = {};
var realistic_cache = {};
var normal_rendering = {};

//function to chunk opd view into pieces 
  // source: https://stackoverflow.com/questions/3366529/wrap-every-3-divs-in-a-div
$.fn.chunk = function(size) {
  var arr = [];
  for (var i = 0; i < this.length; i += size) {
    arr.push(this.slice(i, i + size));
  }
  return this.pushStack(arr, "chunk", size);
}

// build operator detailed view (opd)
function buildOpd(thumbnail_size = $('#operator-detailedview-thumbnail-size').val() ) {

  var thumbnail_size    = parseInt(thumbnail_size);
  var thumbnail_size_mm = thumbnail_size  + 'mm';
  
  var thumbnail_layout  = (thumbnail_size >= 60) ? 'medium' : 'small';
  
  // remove old settings
  $('div.page.operator-detailedview header').remove();
  $('div.page.operator-detailedview footer').remove();
  $('div.page.operator-detailedview .job-headline').remove();
  $('div.page.operator-detailedview .opd-color-block').parentsUntil('div.page.operator-detailedview').addBack().unwrap();
  $('.opd-color-block').removeClass('medium large');
  $('.opd-color-block').removeAttr('style');
  
  // set thumbnail size
  $('.operator-svg.operator-preview').css({
      'width': thumbnail_size_mm, 
      'height': thumbnail_size_mm,
      'max-width': thumbnail_size_mm
  });
  
  // calculate number of blocks per page
  var num_blocks_per_page = 1;
  if(thumbnail_layout == 'medium') {
    $('.opd-color-block').addClass('medium');
    // set width to be able to calculate the height
    $('.opd-color-block').css({ 'width': thumbnail_size_mm });
    // calculate max height -> source: https://stackoverflow.com/questions/6060992/element-with-the-max-height-from-a-set-of-elements
    var color_box_height = Math.max.apply(null, $('.opd-color-block').map(function () { return $(this).height(); }).get());
    var container_height = $('#opd-info').height();
    var num_rows = Math.floor(container_height / color_box_height);
    var num_columns = Math.floor(175 / thumbnail_size);
    // if only two blocks fit into one row, use 50% of the space for each of them
    if(num_columns == 2) { $('.opd-color-block').css({ 'width': 'calc(50% - 2mm)' }); }
    // set equal height for all color blocks
    $('.opd-color-block').css({ 'height': color_box_height });
    // set number of color blocks per page for medium thumbnails
    num_blocks_per_page = num_columns * num_rows;
    // use layout for large thumbnails if only 2 or less color blocks fit on one page
    if(num_blocks_per_page <= 2) { 
      $('.opd-color-block').removeClass('medium').removeAttr('style').addClass('large');
      thumbnail_layout = 'large';
      // set number of color blocks per page for large thumbnails
      num_blocks_per_page = 2;
    }
  } else {
    // set number of color blocks per page for small thumbnails
    num_blocks_per_page = Math.floor(220 / thumbnail_size);
  }
  // set number of color blocks per page to 1 if it defaults to zero
    // this should never happen, but we want to avoid the browser to crash 
  num_blocks_per_page = (num_blocks_per_page <= 0) ? '1' : num_blocks_per_page;
  
  // adjust to new settings
  var header = $('#opd-info header').prop('outerHTML');
  var footer = $('#opd-info footer').prop('outerHTML');
  var job_headline = $('#opd-info .job-headline').prop('outerHTML');
  var opd_visibility = ($('#operator-detailedview').is(':checked')) ? 'block' :'none';
  var paper_size = $('#printing-size').val();
  $('.opd-color-block').chunk(num_blocks_per_page).wrap('<div class="page operator-detailedview ' + paper_size + ' ' + thumbnail_layout +'" style="display:'+ opd_visibility +'"><main class="operator-detailedview"><div class="operator-job-info"></div></main></div>');
  $('div.operator-detailedview').prepend(header);
  $('.operator-job-info').prepend(job_headline);
  $('div.operator-detailedview').append(footer);
  // update page numbers
  setPageNumbers();
}

// set pagenumbers
function setPageNumbers() {
  var totalPageNum = $('body').find('.page:visible').length;
  $('span.total-page-num').text(totalPageNum);
  $('.page:visible span.page-num').each(function( index ) {
    $(this).text(index + 1);
  });
}

// Calculate estimated time
function setEstimatedTime() {
  var speed = Math.floor($('#machine-speed').val() / 60); // convert to seconds
  speed = (speed <= 0) ? 1 : speed;
  var timeTrim = ($('#time-trims').val() == '') ? 0 : parseInt($('#time-trims').val());
  var addToTotal = ($('#time-additional').val() == '') ? 0 : parseInt($('#time-additional').val());
  var timeColorChange = ($('#time-color-change').val() == '') ? 0 : parseInt($('#time-color-change').val());

  // operator detailed view
  $('.estimated-time').each(function(index, item) {
      var selector = $(this);
      var stitchCount = parseInt($(selector).closest('p').find('.num-stitches').text().match(/\d+/));
      var numTrims = parseInt($( selector ).closest('div').find('p span.num-trims').text().match(/\d+/));
      var estimatedTime = stitchCount/speed + (timeTrim * numTrims);
      writeEstimatedTime( selector, estimatedTime );
  });
  
  // client detailed view
  $('.cld-estimated-time').each(function(index, item) {
      var selector = $(this);
      var stitchCount = parseInt($(selector).closest('div.page').find('main .detailed .color-info span.num-stitches').text().match(/\d+/));
      var numTrims = parseInt($( selector ).closest('div.page').find('main .detailed .color-info span.num-trims').text().match(/\d+/));
      var estimatedTime = stitchCount/speed + (timeTrim * numTrims);
      writeEstimatedTime( selector, estimatedTime );
  });

  var stitchCount = parseInt($('.total-num-stitches').first().text().match(/\d+/));
  var numTrims = parseInt($('.total-trims').first().text().match(/\d+/));
  var numColorBlocks = parseInt($('.num-color-blocks').first().text().match(/\d+/))-1; // the last color-block is not a color change
  var selector = '.total-estimated-time';
  var estimatedTime = stitchCount/speed + (timeTrim * numTrims) + (timeColorChange * numColorBlocks) + addToTotal;
  writeEstimatedTime( selector, estimatedTime );
}

function attachLeadingZero(n) {
    return (n < 10) ? ("0" + n) : n;
}

function writeEstimatedTime( selector, estimatedTime ) {
  var hours = attachLeadingZero(Math.floor(estimatedTime / 3600));
  var minutes = attachLeadingZero(Math.floor((estimatedTime - (hours*3600)) / 60));
  var seconds = attachLeadingZero(Math.floor(estimatedTime % 60));
  $(selector).text( hours + ':' + minutes + ':' + seconds );
}

// Scale SVG (fit || full size)
function scaleSVG(element, scale = 'fit') {

  // always center svg
  var transform = "translate(-50%, -50%)";

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

// set preview svg scale to fit into its box if display block and transform is not set
function scaleAllSvg() {
  $('.page').each(function() {
    if( $(this).css('display') == 'block' ) {
      if( $(this).find('.inksimulation svg').css('transform') == 'none') {
        scaleSVG($(this).find('.inksimulation'), 'fit');
      }
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

  /* Contenteditable Fields */

  $('body').on('focusout', '[contenteditable="true"]:not(.info-text)', function() {
    /* change svg scale */
    var content = $(this).text();
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
      $('[data-field-name="' + field_name + '"]').text(content);
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
        } else if (item.is('input[type=range]')) {
            item.val(value).trigger('initialize');
            $('#display-thumbnail-size').text(value + 'mm');
        } else if (item.is('input[type=number]')) {
            item.val(value).trigger('initialize');
        } else if (item.is('figure.inksimulation')) {
            setSVGTransform(item, value);
        } else if (item.is('div.footer-info')) {
            $('#footer-info-text').html($.parseHTML(value));
            item.html($.parseHTML(value));
        } else if (item.is('#custom-page-content')) {
            $('#custom-page-content').html($.parseHTML(value));
        } else {
            item.text(value);
        }
      });
    });

    // wait until page size is set (if they've specified one) and then scale SVGs to fit and build operator detailed view
    setTimeout(function() { 
      scaleAllSvg();
      buildOpd();
    }, 500);
  });

  $('body').on('keypress', '[contenteditable="true"]:not(.info-text)', function(e) {
    if (e.which == 13) {
      // pressing enter defocuses the element
      this.blur();
      // also suppress the enter keystroke to avoid adding a new line
      return false;
    } else {
      return true;
    }
  });

  $('#footer-info-text[contenteditable="true"]').keypress(function(e) {
    if (e.which == 13) {
      if($(this).find('div').length > 2) {
        return false;
      } else {
        return true;
      }
    }
  });

  $('.info-text[contenteditable="true"]').focusout(function() {
    updateEditableText($(this));
  });

  /* Settings Bar */

  $('button.close').click(function() {
     window.close();
  });

  $('button.print').click(function() {
	  var pageSize = $('select#printing-size').find(':selected').text();
	  electron.ipcRenderer.send('open-pdf', pageSize)
  });

  $('button.save-pdf').click(function() {
	  var pageSize = $('select#printing-size').find(':selected').text();
	  electron.ipcRenderer.send('save-pdf', pageSize)
  });  
  
  $('button.settings').click(function(){
    $('#settings-ui').show();
  });

  $('#close-settings').click(function(){
      $('#settings-ui').hide();
  });

  /* Settings */

  // Settings Tabs
  $('#tabs button').click(function() {
    var active_fieldset_position = $(this).index() +1;
    $('#settings-ui #fieldsets-ui > fieldset').css({'display': 'none'});
    $('#settings-ui #fieldsets-ui > fieldset:nth-child('+active_fieldset_position+')').css({'display': 'block'});
    $('#tabs .tab.active').removeClass("active");
    $(this).addClass("active");
  });

  // Footer
  function getEditMode(element){
	    return element.closest('fieldset').find('.switch-mode').prop('checked');
  }

  $('.switch-mode').change(function() {
		var element = $(this);
		var info_text = element.closest('fieldset').find('.info-text');
    var editMode = getEditMode(element);
    if (editMode) {
      info_text.text( info_text.html() );
			element.closest('.tool-bar').find('.tb-button.edit-only').prop("disabled", true);
    } else {
      info_text.css('display', 'block');
      var sourceText = info_text.text();
      info_text.html( $.parseHTML(sourceText) );
      element.closest('.tool-bar').find('.tb-button.edit-only').prop('disabled', false);
    }
  });

  function updateEditableText(element) {
    var editMode = getEditMode(element);
    var info_text = element.closest('fieldset').find('.info-text');
    var editableText = '';

    if (editMode) {
      editableText = info_text.text();
    } else {
      editableText = info_text.html();
    }

    if(info_text.is('#footer-info-text')) {
      $('div.footer-info').html($.parseHTML(editableText));
      $.postJSON('/settings/footer-info', {value: editableText});
    } else {
      $.postJSON('/settings/custom-page-content', {value: editableText});
    }
  }

  function formatText(selection, value) {
      if(window.getSelection().toString()){
        document.execCommand(selection, false, value);
      }
  }

  $('.tb-bold').click(function() {
    if(!getEditMode($(this))) {
      formatText('bold');
      updateEditableText($(this));
    }
  });

  $('.tb-italic').click(function() {
    if(!getEditMode($(this))) {
      formatText('italic');
      updateEditableText($(this));
    }
  });

  $('.tb-underline').click(function() {
    if(!getEditMode($(this))) {
      formatText('underline');
      updateEditableText($(this));
    }
  });

  $('.tb-remove').click(function() {
    if(!getEditMode($(this))) {
      formatText('removeFormat');
      updateEditableText($(this));
    }
  });

  $('.tb-hyperlink').click(function() {
    if(!getEditMode($(this))) {
      formatText('createlink', 'tempurl');
      updateEditableText($(this));
      $(this).closest('.tool-bar').children('.url-window').css('display', 'block');
    }
  });

  $('.url-ok').click(function() {
    var link = $(this).closest('.tool-bar').find('.user-url').val();
    $(this).closest('fieldset').find('.info-text').find('a[href="tempurl"]').attr('href', link);
    $('.user-url').val('https://');
    $('.url-window').css('display', 'none');
    updateEditableText($(this));
  });

  $('.url-cancel').click(function() {
    $(this).closest('fieldset').find('.info-text').find('a[href="tempurl"]').contents().unwrap();
    $('.user-url').val('https://');
    $('.url-window').css('display', 'none');
    updateEditableText($(this));
  });

  $('.tb-mail').click(function() {
    if(!getEditMode($(this))) {
      formatText('createlink', 'tempurl');
      updateEditableText($(this));
      $(this).closest('.tool-bar').find('.mail-window').css('display', 'block');
    }
  });

  $('.mail-ok').click(function() {
    var link = 'mailto:' + $(this).closest('.tool-bar').find('.user-mail').val();
    $(this).closest('fieldset').find('.info-text').find('a[href="tempurl"]').attr('href', link);
    $('.user-mail').val('@');
    $('.mail-window').css('display', 'none');
    updateEditableText($(this));
  });

  $('.mail-cancel').click(function() {
    $(this).closest('fieldset').find('.info-text').find('a[href="tempurl"]').contents().unwrap();
    $('.user-mail').val('@');
    $('.mail-window').css('display', 'none');
    updateEditableText($(this));
  });

  $('.tb-reset').click(function() {
    $(this).closest('.tool-bar').find('.reset-window').css('display', 'block');
  });

  $('.reset-ok').click(function() {
    var htmlMode = getEditMode($(this));
    if(!htmlMode) {
      $(this).closest('fieldset').find('.info-text').html($(this).closest('.tool-bar').find('.original-info').html());
    } else {
      $(this).closest('fieldset').find('.info-text').text($(this).closest('.tool-bar').find('.original-info').html());
    }
    $('.reset-window').css('display', 'none');
    updateEditableText($(this));
  });

  $('.reset-cancel').click(function() {
    $('.reset-window').css('display', 'none');
  });

  $('body').on("click", ".edit-footer-link", function() {
    $("button.settings").trigger("click");
    $("#branding-tab").trigger("click");
  });


  // Paper Size
  $('select#printing-size').on('change initialize', function(){
    $('.page').toggleClass('a4', $(this).find(':selected').val() == 'a4');
  }).on('change', function() {
    $.postJSON('/settings/paper-size', {value: $(this).find(':selected').val()});
  });
  
  // Operator detailed view: thumbnail size setting
  $(document).on('input', '#operator-detailedview-thumbnail-size', function() {
    var thumbnail_size_mm = $(this).val()  + 'mm';
    $('#display-thumbnail-size').text( thumbnail_size_mm );
  });

  // Operator detailed view: thumbnail size setting action
  $('#operator-detailedview-thumbnail-size').change(function() {
    // set thumbnail size
    var thumbnail_size = $(this).val();
    // set page break positions
    buildOpd(thumbnail_size);
    
    $.postJSON('/settings/operator-detailedview-thumbnail-size', {value: thumbnail_size});
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
    scaleAllSvg();
    setPageNumbers();
  }).on('change', function() {
    var field_name = $(this).attr('data-field-name');
    $.postJSON('/settings/' + field_name, {value: $(this).prop('checked')});
  });

  // Estimated Time
  $('#machine-speed, #time-additional, #time-color-change, #time-trims').on('input initialize', function() {
    setEstimatedTime();
  }).on('change', function() {
    var field_name = $(this).attr('data-field-name');
    $.postJSON('/settings/' + field_name, {value: $(this).val()});
  });

  // Display Estimated Time checkboxes
  $(':checkbox.time-display').on('input initialize', function() {
    var field_name = $(this).attr('data-field-name');
    $('.' + field_name).toggle($(this).prop('checked'));
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

    function finalize(svg_content) {
      svg[0].outerHTML = svg_content;
      // can't use the svg variable here because setting outerHTML created a new tag
      figure.find('svg').css({transform: transform});
    }

    // do this later to allow this event handler to return now,
    // which will cause the checkbox to be checked or unchecked
    // immediately even if SVG rendering takes awhile
    setTimeout(function() {
      if (checked) {
        if (!(item in normal_rendering)) {
          normal_rendering[item] = svg[0].outerHTML;
        }

        if (!(item in realistic_cache)) {
          // pre-render the realistic SVG to a raster image to spare the poor browser
          var image = document.createElement('img');
          image.onload = function() {
            console.log("rendering!");
            var canvas = document.createElement('canvas');

            // maybe make DPI configurable?  for now, use 600
            canvas.width = image.width / 96 * 600;
            canvas.height = image.height / 96 * 600;

            var ctx = canvas.getContext('2d');
            ctx.drawImage(image, 0, 0, image.width, image.height, 0, 0, canvas.width, canvas.height);
            realistic_cache[item] = '<svg width=' + image.width + ' height=' + image.height + ' xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">' +
                                    '<image x=0 y=0 width=' + image.width + ' height=' + image.height + ' xlink:href="' + canvas.toDataURL() + '" />' +
                                    '</svg>';
            finalize(realistic_cache[item]);
          };
          image.src = '/realistic/' + item;
        } else {
          finalize(realistic_cache[item]);
        }
      } else {
        finalize(normal_rendering[item]);
      }
    }, 100);

    e.stopPropagation();
    return true;
  });

  setTimeout(function() {
    setEstimatedTime();
  }, 100);

  $('button.svg-realistic').click(function(e){
    $(this).find('input').click();
  });

  // Logo
  $(document).on("change", ".logo-picker", function(e) {
    var file = e.currentTarget.files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
      var data = reader.result;
      $('figure.brandlogo img').attr('src', data);
      $.postJSON('/settings/logo', {value: data});
    };
    reader.readAsDataURL(file);
  });

  // "save as defaults" button
  $('button.save-settings').click(function(e) {
    var settings = {};
    settings["client-overview"] = $("[data-field-name='client-overview']").is(':checked');
    settings["client-detailedview"] = $("[data-field-name='client-detailedview']").is(':checked');
    settings["operator-overview"] = $("[data-field-name='operator-overview']").is(':checked');
    settings["operator-detailedview"] = $("[data-field-name='operator-detailedview']").is(':checked');
    settings["operator-detailedview-thumbnail-size"] = $("[data-field-name='operator-detailedview-thumbnail-size']").val();
    settings["custom-page"] = $("[data-field-name='custom-page']").is(':checked');
    settings["paper-size"] = $('select#printing-size').find(':selected').val();

    var logo = $("figure.brandlogo img").attr('src');
    if (logo.startsWith("data:")) {
        settings["logo"] = logo;
    }
    settings["footer-info"] = $("[data-field-name='footer-info']").html();

    settings["machine-speed"] = $("[data-field-name='machine-speed']").val();
    settings["time-additional"] = $("[data-field-name='time-additional']").val();
    settings["time-color-change"] = $("[data-field-name='time-color-change']").val(); 
    settings["time-trims"] = $("[data-field-name='time-trims']").val();

    settings["time-clo"] = $("[data-field-name='time-clo']").val();
    settings["time-cld"] = $("[data-field-name='time-cld']").val();
    settings["time-opo"] = $("[data-field-name='time-opo']").val();
    settings["time-opd"] = $("[data-field-name='time-opd']").val();

    $.postJSON('/defaults', {'value': settings});
  });
});
