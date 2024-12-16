var fontDisplaySize = document.getElementById('font-display-size')
var fontFilterForm = document.getElementById('font-filter');
var sizeFilter = document.getElementById("size-filter");
var categoryFilter = document.getElementById("style-filter");
var glyphFilter = document.getElementById("glyph-filter");

fontFilterForm.addEventListener('submit', function(event) {
    event.preventDefault();
    updateFontList();
    return true;
}, false);

document.getElementById('toggle-font-filter').addEventListener('click', toggleFilterForm);
sizeFilter.addEventListener('change', updateFontList);
categoryFilter.addEventListener('change', updateFontList);
glyphFilter.addEventListener('change', updateFontList);
document.addEventListener("DOMContentLoaded", updateFontList);

function toggleFilterForm() {
if (fontFilterForm.style.display === "none") {
    fontFilterForm.style.display = "block";
  } else {
    fontFilterForm.style.display = "none";
  }
}

function updateFontList(){
  let font_data = document.querySelectorAll('[data-max_size]');
  for (var font of font_data) {
    let max_size = parseFloat(font.getAttribute('data-max_size'));
    let min_size = parseFloat(font.getAttribute('data-min_size'));

    let keywords = font.getAttribute('data-keywords').split(",");
    let selectedCategories = categoryFilter.selectedOptions;
    selectedCategories = Array.from(selectedCategories).map(({ value }) => value);
    selectedCategories = selectedCategories.filter(n => n);
    let activeKeys = keywords.filter(key => selectedCategories.includes(key));

    let glyphs = font.getAttribute('data-glyphs').split(" ");
    let selectedGlyphs = Array.from(new Set(glyphFilter.value.replace(/\s/g, "").split("")));

    if ((sizeFilter.value && (max_size < sizeFilter.value || min_size > sizeFilter.value)) ||
        (selectedCategories.length > 0 && activeKeys.length == 0) ||
        (selectedGlyphs.length > 0 && !selectedGlyphs.every(glyph => glyphs.includes(glyph)))
       ) {
      font.style.display = 'none';
    } else {
      font.style.display = 'block';
    }
  }
  let countVisible = document.querySelectorAll(".font-separator:not([style='display: none;'])").length;
  document.getElementById('font-counter').innerHTML = countVisible
}

fontDisplaySize.addEventListener('change', updateFontDisplaySize);
function updateFontDisplaySize() {
  let font_images = document.querySelectorAll('div.font-separator img');
  for (var image of font_images) {
      if (fontDisplaySize.checked) {
        image.style.height = image.getAttribute('data-image_height');
      } else {
        image.style.height = '5em';
      }
  }
}

sortbySelect = document.getElementById('sort-by-min-size')
sortbySelect.addEventListener('change', sortFontList);
sortDirect = document.getElementById('sort-asc-desc')
sortDirect.addEventListener('change', sortFontList);

function sortFontList(){
    let font_data = document.querySelectorAll("[data-max_size]");
    let fontSizeArray = Array.from(font_data);

    let sortby = sortbySelect.value;
    var sorted = fontSizeArray
    if (sortby == "title") {
        sorted = fontSizeArray.sort((a, b) => a.dataset.title.localeCompare(b.dataset.title));
    } else if (sortby == "min_size") {
        sorted = fontSizeArray.sort((a, b) => parseFloat(a.dataset.min_size) - parseFloat(b.dataset.min_size));
    } else {
        sorted = fontSizeArray.sort((a, b) => parseFloat(a.dataset.max_size) - parseFloat(b.dataset.max_size));
    }
    if (sortDirect.value == 'desc') {
        sorted = sorted.reverse()
    }
    sorted.forEach(e => document.querySelector("#font-list").appendChild(e))
}

displayIcons = document.getElementById('font-display-icons')
displayIcons.addEventListener('change', showHidePreviewImages)

function showHidePreviewImages() {
    let images = document.querySelectorAll('.font-library-preview-image')
    images.forEach(function(image) {
        if (displayIcons.checked) {
            image.style.display = 'inline';
            fontDisplaySize.disabled = false;
        } else {
            image.style.display = 'none';
            fontDisplaySize.disabled = true;
        }
    });
}
