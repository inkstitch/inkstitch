const axios = require('axios')
const queryString = require('query-string')

var port = queryString.parse(global.location.search).port

module.exports = axios.create({
	baseURL: `http://127.0.0.1:${port}/`
})