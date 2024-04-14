<template>
    <div>
      
      <LibrarianNavbar />
      
      <div class="background">
          <div class="login-container">
              <h1 class="white-text">Add Section</h1>
              <form class="mb-3" @submit.prevent="addSection">
                  <div class="mb-3">
                      <label class="form-label white-text">Name</label>
                      <input type="text" class="form-control" v-model="name" placeholder="Name">
                  </div>
                  <div class="mb-3">
                      <label class="form-label white-text">Description</label>
                      <input type="text" class="form-control" v-model="description" placeholder="Describe this section.">
                  </div>
                  <button type="submit" class="btn btn-primary w-100">Add</button>
              </form>
              <router-link to="/librarian-all-sections" class="w-100">
                  <button type="button" class="btn btn-danger w-100">Cancel</button>
              </router-link>
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
      name: '',
      description: ''
    };
  },
  methods: {
    addSection() {
      
      fetch('http://localhost:5000/librarian-add-section', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            name: this.name,
            description: this.description
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.error) {
            alert(data.error);
          } else {
            alert('Section added successfully');
            this.$router.push({ name: 'librarian-all-sections' });
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });

    }
  }
};
</script>