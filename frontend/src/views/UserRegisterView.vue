<template>
    
    <div>
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

        <div class="home-background">
            <div class="login-container">
                <h1>User Registration</h1>
            
                <form class="mb-3" @submit.prevent="registerUser">
                    <div class="mb-3">
                    <label for="inputUsername" class="form-label text-light">Username</label>
                    <input type="text" class="form-control" id="inputUsername" v-model="user.username" placeholder="Username">
                    </div>
                    <div class="mb-3">
                    <label for="inputEmail" class="form-label text-light">Email address</label>
                    <input type="email" class="form-control" id="inputEmail" v-model="user.email" placeholder="name@example.com">
                    </div>
                    <div class="mb-3">
                    <label for="inputPassword" class="form-label text-light">Password</label>
                    <input type="password" class="form-control" id="inputPassword" v-model="user.password" placeholder="Password">
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Register</button>
                </form>
            </div>
        </div>
    </div>
  </template>
  
  <script>
  import Logo from '../assets/Designer.png';
  export default {
    data() {
      return {
        logo: Logo,
        user: {
          username: '',
          email: '',
          password: ''
        }
      };
    },
    methods: {
      registerUser() {
        // Call "user-register" API endpoint
        fetch('http://localhost:5000/user-register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.user)
        })
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            alert(data.error);
          } else {
            alert('User registered successfully');
            this.$router.push({ name: 'user-login' });
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
      }
    }
  };
  </script>
  
  <style>
  @import '../assets/css/style2.css'
  </style>
  