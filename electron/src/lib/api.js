/*
 * Authors: see git history
 *
 * Copyright (c) 2010 Authors
 * Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
 *
 */

import axios from 'axios';

export const inkStitch = axios.create({
    baseURL: 'http://127.0.0.1:5000/'
})
