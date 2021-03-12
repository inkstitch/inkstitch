<!--

  Authors: see git history

  Copyright (c) 2010 Authors
  Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.

-->

<template>
  <div id="app">
    <v-app>
      <v-main>
        <router-view></router-view>
      </v-main>
    </v-app>
  </div>
</template>

<script>
export default {
  name: 'my-project'
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Roboto:300,400,500,700|Material+Icons');
</style>
