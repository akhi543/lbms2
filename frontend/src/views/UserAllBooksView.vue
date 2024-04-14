<template>
  <div>

    <UserNavbar />

    <div class="list-background">

      <div class="scrollable-div" style="max-height: 500px; overflow: auto; background-color: #DADFE7">
          <div class="container">
            <div class="col-12 mt-4 d-flex justify-content-center">
              <form id="searchForm" @submit.prevent="searchBooks">
                <div class="input-group">
                  <input type="text" class="form-control" v-model="searchQuery" placeholder="Search by title or author">
                  <div class="input-group-append">
                    <button class="btn btn-outline-secondary" type="submit">Search</button>
                  </div>
                </div>
              </form>
            </div>

            <div class="row mt-4">
              <div class="col-lg-4 col-md-6 col-sm-6" v-for="book in filteredBooks" :key="book.id">
                <div class="mb-4">
                  <div class="book-card">
                    <h5 class="card-title">{{ book.title }}</h5>
                    <p class="card-text">by {{ book.author }}</p>
                    <button @click="requestBook(book.id)" class="btn btn-primary">Request</button>
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
    UserNavbar
  },
  name: 'BooksPage',
  data() {
    return {
      logo: Logo,
      searchQuery: '',
      allBooks: [],
      filteredBooks: []
    };
  },
  mounted() {
    fetch('http://localhost:5000/user-all-books')
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          alert(data.error);
          return;
        }
        this.allBooks = data;
        this.filteredBooks = data;
      })
      .catch((error) => {
        console.error('Error:', error);
      });

  },
  methods: {
    searchBooks() {
      this.filteredBooks = this.allBooks.filter(book => {
        return book.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          book.author.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
    },
    requestBook(bookId) {
      const usernameFromCookies = Cookies.get('username');
      fetch('http://localhost:5000/user-request-book', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: usernameFromCookies,
          book_id: bookId
        })
      })
      .then(response => response.json())
      .then(data => {
        // alert('data: ' + JSON.stringify(data));
        if (data.error) {
          alert(data.error);
        } else {
          alert('Book requested successfully');
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });

    }
  }
}
</script>

<style>
@import '../assets/css/style2.css';
</style>
