<template>
    <div>
      <LibrarianNavbar  />
  
      <div class="list-background">
        <div class="scrollable-div" style="max-height: 500px; overflow: auto;">
          <div class="container mt-4">
  
            <div class="row mt-4">
              <div class="col-lg-4 col-md-6 col-sm-6" v-for="request in allRequests" :key="request.id">
                <div class="mb-4">
                  <div class="book-card border-2 border-primary">
                    <h5 class="card-title">Title: {{ request.title }}</h5><br>
                    <h6 class="card-title">Author: {{ request.author }}</h6><br>
                    <h6 class="card-title">Section: {{ request.sectionName }}</h6><br>
                    <h6 class="card-title">Requested by: {{ request.requestedby }}</h6><br>
                    <h6 class="card-title">Number of books issued to {{ request.numBooksToRequester }}</h6>
                    <div class="row">
                      <div class="col">
                        <button @click="approve(request.id)" class="btn btn-primary">Approve</button>
                      </div>
                      <div class="col">
                        <button @click="reject(request.id)" class="btn btn-danger">Reject</button>
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

export default {
    components: {
        LibrarianNavbar,
    },
    data() {
        return {
            allRequests: []
        };
    },
    mounted() {
        fetch('http://localhost:5000/librarian-book-requests')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                this.allRequests = data;
            })
            .catch(error => alert(error));
    },
    methods: {
        approve(requestId) {
            fetch('http://localhost:5000/librarian-approve-request/' + requestId, {
              method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                this.allRequests = this.allRequests.filter(request => request.id !== requestId);
                alert('Request Approved');
            })
            .catch(error => alert(error));
        },
        reject(requestId) {
            fetch('http://localhost:5000/librarian-reject-request/' + requestId, {
              method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                this.allRequests = this.allRequests.filter(request => request.id !== requestId);
                alert('Request Rejected');
            })
            .catch(error => alert(error));
        }
    },
    };
</script>

<style scoped>
@import '../assets/css/style2.css';
</style>
