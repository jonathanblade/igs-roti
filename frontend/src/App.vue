<template>
  <v-app>
    <v-container class="text-center" fluid>
      <v-row justify="center">
        <v-col cols="12" md="6">
          <Navigation />
          <router-view />
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import Navigation from './components/Navigation.vue';

export default {
  name: 'App',
  components: {
    Navigation
  }
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Ubuntu&display=swap');

#app {
  font-family: 'Ubuntu', sans-serif;
  color: black;
}
</style>
