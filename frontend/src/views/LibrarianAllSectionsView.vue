<template>
  <div>
    <LibrarianNavbar  />

    <div class="list-background">
      <div class="scrollable-div" style="max-height: 500px; overflow: auto;">
        <div class="container mt-4">

          <div class="row">
            <div class="col-10 d-flex justify-content-right">
              <form id="searchForm" @submit.prevent="searchSections">
                <div class="input-group">
                  <input type="text" class="form-control" v-model="searchQuery" placeholder="Search by title or author">
                  <div class="input-group-append">
                    <button class="btn btn-outline-secondary" type="submit">Search</button>
                  </div>
                </div>
              </form>
            </div>
            <div class="col">
              <router-link to="/librarian-add-section" class="btn btn-success">
                <h5>Add Section</h5>
              </router-link>
            </div>
          </div>

          <div class="row mt-4">
            <div class="col-lg-4 col-md-6 col-sm-6" v-for="section in filteredSections" :key="section.id">
              <div class="mb-4">
                <div class="book-card border-2 border-primary">
                  <div class="row">
                    <div class="col-9">
                      <h5 class="card-title">{{ section.name }}</h5> 
                    </div>
                    <div class="col">
                      <button @click="deleteSection(section.id)">
                        <img :src="bin" alt="section image" class="img-fluid" width="20">
                      </button>
                    </div>
                      
                  </div>
                  <h6 class="card-title">{{ section.description }}</h6>
                  <div class="row">
                    <div class="col">
                      <router-link v-if="section.id" :to="'/librarian-list-of-books/' + section.id" class="btn btn-primary">View Books</router-link>
                    </div>
                    <div class="col">
                      <router-link v-if="section.id" :to="'/librarian-add-book/' + section.id" class="btn btn-info">Add Book</router-link>
                    </div>
                  </div>
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
import LibrarianNavbar from '@/components/LibrarianNavbar.vue';
import Logo from '../assets/Designer.png';
import Bin from '../assets/bin.png';
import Pencil from '../assets/pencil.png';

export default {
  components: {
    LibrarianNavbar,
  },
  data() {
    return {
      logo: Logo,
      bin: Bin,
      pencil: Pencil,
      username: 'User',
      searchQuery: '',
      allsections: [],
      filteredSections: [],
    };
  },
  mounted() {

    // Make get request to the server to get all sections
    fetch('http://localhost:5000/librarian-all-sections')
      .then((response) => response.json())
      .then((data) => {
        this.allsections = data;
        this.filteredSections = this.allsections;
      })
      .catch((error) => {
        console.error('Error:', error);
      });

  },
  methods: {
    searchSections() {
      this.filteredSections = this.allsections.filter((section) => {
        return section.name.toLowerCase().includes(this.searchQuery.toLowerCase()) || section.description.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
    },
    deleteSection(sectionId) {
      let url = 'http://localhost:5000/librarian-delete-section/' + sectionId;
      // alert(url);
      fetch(url, {
        method: 'DELETE',
      })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          alert(data.error);
          return;
        }
        this.allsections = this.allsections.filter((section) => section.id !== section.id);
        this.filteredSections = this.allsections;
        alert('Section Deleted Successfully');
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    },
  },
};
</script>

<style scoped>
@import '../assets/css/style2.css';
</style>
