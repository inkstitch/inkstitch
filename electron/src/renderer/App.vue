<template>
  <div id="app">
    <v-app>
      <v-main>
        <!-- the v-container, v-row, and v-col give us vertical centering -->
        <v-container fill-height fluid>
          <v-row align="center" justify="center">
            <v-col>
              <router-view></router-view>
            </v-col>
          </v-row>
        </v-container>
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
