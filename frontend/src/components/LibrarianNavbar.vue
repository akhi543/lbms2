<template>
    <nav class="navbar navbar-expand-lg">
      <div class="container">
        <router-link to="/" class="logo">
          <img :src="logo" alt="Company Logo" style="height:50px; width:50px;">
        </router-link>
        <router-link class="navbar-brand pl-3" style="color: white;" :to="linkDestination">Bookwise</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/librarian-requests">Requests</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link">Welcome {{ username }}!</a>
            </li>
            <li class="nav-item">
              <button class="nav-link" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
</template>

<script>
import logo from '../assets/Designer.png';
import Cookies from 'js-cookie';

export default {
    name: 'LibrarianNavbar',
    data() {
        return {
            logo: logo,
            username: ''
        };
    },
    created() {
        // Fetch username from cookies
        const usernameFromCookies = Cookies.get('username');
        if (usernameFromCookies) {
        this.username = usernameFromCookies;
        }
    },
    computed: {
      linkDestination() {
        const username = Cookies.get('username');
        return username ? `/librarian-all-sections` : `/`;
      }
    },
    methods: {
        logout() {
            Cookies.remove('username');
            this.$router.push('/');
        }
    }
};
</script>