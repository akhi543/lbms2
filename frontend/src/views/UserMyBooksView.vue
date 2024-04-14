<template>
    <div>

      <UserNavbar />

      <div class="list-background">
        
        <div class="scrollable-div" style="max-height: 500px; overflow: auto; background-color: #dadfe7">
          <div class="container">
            <div class="col-12 mt-4 d-flex justify-content-center">
              <form id="searchForm" @submit.prevent="searchBooks">
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control"
                    v-model="searchQuery"
                    placeholder="Search by title or author"
                  />
                  <div class="input-group-append">
                    <button class="btn btn-outline-secondary" type="submit">Search</button>
                  </div>
                </div>
              </form>
            </div>
            <br> <br>
            <h2>Currently Issued</h2>
            <div class="row mt-1">
              <div
                class="col-lg-3 col-md-6 col-sm-6"
                v-for="book in filteredBooks.currentlyIssued"
                :key="book.id"
              >
                <div class="mb-4">
                  <div class="book-card">
                    <h5 class="card-title">{{ book.title }}</h5>
                    <p class="card-text">by {{ book.author }}</p>
                  </div>
                </div>
              </div>
            </div>
    
            <h2>Completed</h2>
            <div class="row mt-1">
              <div
                class="col-lg-3 col-md-6 col-sm-6"
                v-for="book in filteredBooks.completed"
                :key="book.id"
              >
                <div class="mb-4">
                  <div class="book-card">
                    <h5 class="card-title">{{ book.title }}</h5>
                    <p class="card-text">by {{ book.author }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
    
        <footer class="footer">
          <div class="container text-center">
            <span class="navbar-text">© 2024 Bookwise</span>
          </div>
        </footer>
      </div>

    </div>
  </template>
  
<script>
import Logo from '../assets/Designer.png';
import UserNavbar from '@/components/UserNavbar.vue';
import Cookies from 'js-cookie';

export default {
  components: {
    UserNavbar,
  },
  name: 'BooksPage',
  data() {
    return {
      logo: Logo,
      username: 'User',
      searchQuery: '',
      currentlyIssuedBooks: [],
      completedBooks: [],
      filteredBooks: {
        currentlyIssued: [],
        completed: [],
      },
    };
  },
  created() {
    let usernameFromCookies = Cookies.get('username');
    fetch('http://localhost:5000/user-my-books/' + usernameFromCookies)
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert(data.error);
        return;
      }
      alert('data: ' + JSON.stringify(data));
      this.currentlyIssuedBooks = data.currentlyIssued;
      this.completedBooks = data.completed;
      this.filteredBooks.currentlyIssued = this.currentlyIssuedBooks;
      this.filteredBooks.completed = this.completedBooks;
    })
    .catch((error) => alert(error));
  },
  methods: {
    searchBooks() {
      const filter = (books) =>
        books.filter((book) => {
          return (
            book.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            book.author.toLowerCase().includes(this.searchQuery.toLowerCase())
          );
        });
      this.filteredBooks.currentlyIssued = filter(this.currentlyIssuedBooks);
      this.filteredBooks.completed = filter(this.completedBooks);
    },
  },
};
</script>

<style>
@import "../assets/css/style2.css";
</style>
