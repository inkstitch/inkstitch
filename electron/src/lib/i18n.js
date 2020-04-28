module.exports.selectLanguage = function () {
  ['LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'].forEach(language => {
    if (process.env[language]) {
      return process.env[language].split(":")[0]
    }
  })

  return "en_US"
}
