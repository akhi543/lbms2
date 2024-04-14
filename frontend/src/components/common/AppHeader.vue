<template>
  <header class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
      <router-link class="logo" to="/">
        <img :src="logo" alt="Company Logo" style="height:50px; width:50px;">
      </router-link>
      <router-link class="navbar-brand" to="/">BookWise</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/">About</router-link>
          </li>
        </ul>
      </div>
    </div>
  </header>
</template>

<script>
import Logo from '../../assets/Designer.png';
export default {
  name: 'AppHeader',
  data() {
    return {
      logo: Logo
    };
  }
};
</script>

<style scoped>
/* Add scoped styles for the header component here */
</style>