/*
 * Authors: see git history
 *
 * Copyright (c) 2010 Authors
 * Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
 *
 */

import axios from 'axios';
import flaskserverport from './flaskserverport.json'

if (flaskserverport.port === undefined) {
    var theflaskport = window.inkstitchAPI.flaskport()
    console.log("Installed mode")
    console.log(theflaskport)
} else {
    var theflaskport = flaskserverport.port
    console.log("Dev mode")
    console.log(theflaskport)
}

export const inkStitch = axios.create({
    baseURL: `http://127.0.0.1:${theflaskport}`
})
