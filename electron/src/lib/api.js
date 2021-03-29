/*
 * Authors: see git history
 *
 * Copyright (c) 2010 Authors
 * Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
 *
 */

const axios = require('axios')
const queryString = require('query-string')

const port = queryString.parse(global.location.search).port
const url = `http://127.0.0.1:${port}`

module.exports = axios.create({
  baseURL: url
})

module.exports.url = url
