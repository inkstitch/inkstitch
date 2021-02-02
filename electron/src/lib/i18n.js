module.exports.selectLanguage = function (translations) {
  // get a list of available translations
  var availableTranslations = [];
  for(var k in translations) availableTranslations.push(k);

  // set default language
  var lang = "en_US";

  // get system language / Inkscape language
  ['LANG', 'LC_MESSAGES', 'LC_ALL', 'LANGUAGE'].forEach(language => {
    if (process.env[language]) {
      // split encoding information, we don't need it
      var current_lang = process.env[language].split(".")[0];
      if (current_lang.length == 2) {
        // current language has only two letters (e.g. en),
        // compare with available languages and if present, set to a long locale name (e.g. en_US)
        lang = availableTranslations.find(elem => elem.startsWith(current_lang));
      } else {
        lang = process.env[language].split(".")[0];
      }
    }
  })
  return lang
}
