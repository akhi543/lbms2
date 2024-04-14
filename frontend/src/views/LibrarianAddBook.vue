<template>
    <div>
      
      <LibrarianNavbar />
      
      <div class="background">
          <div class="login-container">
              <h1 class="white-text">Add Book</h1>
              <form class="mb-3" @submit.prevent="addBook">
                  <div class="mb-3">
                      <label class="form-label white-text">Title</label>
                      <input type="text" class="form-control" v-model="title" placeholder="Title">
                  </div>
                  
                  <div class="mb-3">
                      <label class="form-label white-text">Author</label>
                      <input type="text" class="form-control" v-model="author" placeholder="Author">
                  </div>

                  <div class="mb-3">
                      <label class="form-label white-text">Pages</label>
                      <input type="text" class="form-control" v-model="pages" placeholder="Number of pages">
                  </div>

                  <div class="mb-3">
                      <label class="form-label white-text">Volume</label>
                      <input type="text" class="form-control" v-model="volume" placeholder="Volume number">
                  </div>

                  <button type="submit" class="btn btn-primary w-100">Add</button>
              </form>
          </div>
      </div>
    </div>
</template>

<script>
import LibrarianNavbar from '@/components/LibrarianNavbar.vue';

export default {
  components: {
      LibrarianNavbar
  },
  data() {
    return {
      title: '',
      author: '',
      pages: '',
      volume: '',
      sectionId: ''
    };
  },
  created() {
    this.sectionId = this.$route.params.sectionId;
    // alert("sectionId: " + this.sectionId);
  },
  methods: {
    addBook() {
      let url = 'http://localhost:5000/librarian-add-book/' + this.sectionId;
      // alert("url: " + url);
      fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            title: this.title,
            author: this.author,
            pages: this.pages,
            volume: this.volume
          })
        })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          alert(data.error);
        } else {
          alert('Book added successfully');
          this.$router.push('/librarian-list-of-books/' + this.sectionId);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });

    }
  }
};
</script>