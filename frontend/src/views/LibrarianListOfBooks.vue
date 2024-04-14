<template>
    <div>
        <LibrianNavbar />

        <div class="list-background">
            <div class="scrollable-div" style="max-height: 500px; overflow: auto;">
                <div class="container mt-4">
                    <div class="row">
                        <div class="col-8">
                            <form @submit.prevent="searchBooks" class="input-group">
                            <input v-model="searchQuery" type="text" placeholder="Search by title or author">
                            <button class="btn btn-outline-secondary" type="submit">Search</button>
                            </form>
                        </div>
                        <div class="col">
                            <router-link :to="'/librarian-add-book/' + sectionId" class="btn btn-success">
                            <h5>Add Book</h5>
                            </router-link>
                        </div>
                    </div>
                    <div class="row mt-4">
                        <div v-for="book in filteredBooks" :key="book.id" class="col-lg-4 col-md-6 col-sm-6">
                            <div class="mb-4">
                            <div class="book-card border-2 border-primary">
                                <h5 class="card-title">{{ book.title }}</h5>
                                <h6 class="card-title">{{ book.author }}</h6>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
  <script>
  import LibrianNavbar from '@/components/LibrarianNavbar.vue';

  export default {
    components: {
      LibrianNavbar,
    },
    data() {
      return {
        allBooks: [],
        searchQuery: '',
        sectionId: this.$route.params.sectionId,
        filteredBooks: []
      };
    },
    mounted() {
      let url = 'http://localhost:5000/librarian-list-of-books/' + this.sectionId;
      fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          alert(data.error); 
        } else {
          this.allBooks = data;
          this.filteredBooks = this.allBooks;
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    },
    methods: {
      searchBooks() {
        this.filteredBooks = this.allBooks.filter((book) => {
          return book.title.toLowerCase().includes(this.searchQuery.toLowerCase()) || book.author.toLowerCase().includes(this.searchQuery.toLowerCase());
        });
      }
    }
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  