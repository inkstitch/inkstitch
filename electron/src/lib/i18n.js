module.exports.selectLanguage = function () {
  var lang = "en_US";
  ['LANG', 'LC_MESSAGES', 'LC_ALL', 'LANGUAGE'].forEach(language => {
    if (process.env[language] && process.env[language].split("_").length > 1) {
      lang = process.env[language].split(".")[0];
    }
  })
  return lang
}
