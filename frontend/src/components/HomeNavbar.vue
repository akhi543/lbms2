<template>
    <header class="navbar navbar-expand-lg">
      <div class="container">
        <router-link class="logo" to="/">
          <img :src="logo" alt="Company Logo" style="height:50px; width:50px;">
        </router-link>
        <router-link class="navbar-brand" style="color: white;" to="/">BookWise</router-link>
        
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div id="navbarNav">
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
import logo from '../assets/Designer.png';

export default {
    name: 'HomeNavbar',
    data() {
        return {
            logo: logo,
            username: ''
        };
    }
};
</script>