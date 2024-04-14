<template>
  <div>

    <HomeNavbar />

    <div class="home-background">
      <div class="login-container">
        <h1>Librarian Login</h1>
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

      </div>
    </div>
    
    <footer>
      <p>&copy; 2024 Your Library Name. All rights reserved.</p>
    </footer>

  </div>
</template>

<script>
import Logo from '../assets/Designer.png';
import Cookies from 'js-cookie';
import HomeNavbar from '@/components/HomeNavbar.vue';

export default {
  components: {
    HomeNavbar,
  },
  data() {
    return {
      logo: Logo,
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
          this.$router.push('/librarian-all-sections');
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
.navbar {
    overflow: hidden;
    background-color: #0560A2;
}
.navbar-nav {
  justify-content: flex-end;
}

.home-background {
  background-image: url('../assets/lib.jpeg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.login-container {
  width: 100%;
  max-width: 400px;
  background: #000000;
  padding: 20px;
  position: relative;
  top: 50px;
}
</style>
