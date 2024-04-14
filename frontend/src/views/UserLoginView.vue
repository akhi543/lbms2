<template>
  <div>

    <HomeNavbar />

    <div class="home-background">
      <div class="login-container">
        <h1>User Login</h1>
        <form class="mb-3" @submit.prevent="login" method="post">
          <div class="mb-3">
            <label for="inputEmail" class="form-label text-light">Username</label>
            <input type="text" class="form-control" v-model="username" placeholder="Username">
          </div>
          <div class="mb-3">
            <label for="inputPassword" class="form-label text-light">Password</label>
            <input type="password" class="form-control" v-model="password" placeholder="Password">
          </div>
          <button type="submit" class="btn btn-primary w-100">Login</button>
        </form>

        <div class="container">
          <div class="row">
            <div class="col d-flex align-items-center justify-content-end">
              <div class="text-right text-light fs-5">New User?</div>
            </div>
            <div class="col d-flex align-items-center justify-content-center pb-2">
              <router-link to="/user-register" class="w-100">
                <button type="button" class="btn btn-primary w-100">Register</button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <footer>
      <p>&copy; 2024 Your Library Name. All rights reserved.</p>
    </footer>

  </div>
</template>

<script>
import Cookies from 'js-cookie';
import HomeNavbar from '@/components/HomeNavbar.vue';

export default {
  components: {
    HomeNavbar,
  },
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    login() {

      fetch('http://localhost:5000/user-login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: this.username,
          password: this.password
        })
      })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          alert(data.error);
        } else {
          Cookies.set('username', data.username, { expires: 1 });
          this.$router.push('/user-all-books');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });

    }
  }
};
</script>

<style scoped>
@import '../assets/css/style2.css'
</style>
