/*
 * Authors: see git history
 *
 * Copyright (c) 2010 Authors
 * Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
 *
 */
export function selectLanguage(translations) {
  // get language from flask server, process in modern electron isn't exposed to renderer
  const request = new XMLHttpRequest();
  request.open('GET', 'http://127.0.0.1:5000/languages', false)
  request.send(null)
  var process = undefined

  if (request.status === 200) {
    process =  JSON.parse(request.responseText)
  }
  // get a list of available translations
  var availableTranslations = ['en_US'];
  for (var k in translations) availableTranslations.push(k);

  var lang = undefined;

  // get system language / Inkscape language
  ['LANG', 'LC_MESSAGES', 'LC_ALL', 'LANGUAGE'].forEach(language => {
    if (process[language]) {
      // split encoding information, we don't need it
      var current_lang = process[language].split('.')[0];
  
      if (current_lang.length == 2) {
        // current language has only two letters (e.g. en),
        // compare with available languages and if present, set to a long locale name (e.g. en_US)
        lang = availableTranslations.find((elem) => elem.startsWith(current_lang));
      } else {
        lang = current_lang;
      }
    }
  })
  // set default language
  if (lang === undefined) {
    lang = "en_US"
  }
  return lang
}
