<template>
  <div>

    <HomeNavbar />

    <div class="home-background">
      <div class="login-container">
        <h1 class="white-text" style="margin: 0 auto;">Welcome to Bookwise</h1>
        <button @click="redirectToUserLoginPage" class="btn btn-primary w-100 m-2">User Login</button>
        <button @click="redirectToLibrarianLoginPage" class="btn btn-primary w-100 m-2">Librarian Login</button>
      </div>
    </div>

  </div>
</template>

<script>
import HomeNavbar from '@/components/HomeNavbar.vue';
import Logo from '../assets/Designer.png';

export default {
  components: {
    HomeNavbar,
  },
  name: 'HomeView',
  data() {
    return {
      logo: Logo
    };
  },
  methods: {
    redirectToUserLoginPage() {
      this.$router.push({ name: 'user-login' });
    },
    redirectToLibrarianLoginPage() {
      this.$router.push({ name: 'librarian-login' });
    }
  }
};
</script>

<style scoped>
@import '../assets/css/style2.css'
</style>