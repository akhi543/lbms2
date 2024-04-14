import Vue from 'vue';
import VueRouter from 'vue-router';
import HomeView from '../views/HomeView.vue';
import UserLoginView from '../views/UserLoginView.vue';
import UserRegisterView from '@/views/UserRegisterView.vue';
import UserAllBooksView from '../views/UserAllBooksView.vue';
import UserMyBooksView from '../views/UserMyBooksView.vue';
import LibrarianAddBook from '@/views/LibrarianAddBook.vue';
import LibrarianAddSection from '@/views/LibrarianAddSection.vue';
import LibrarianAllSectionsView from '@/views/LibrarianAllSectionsView.vue';
import LibrarianListOfBooks from '@/views/LibrarianListOfBooks.vue';
import LibrarianLoginView from '@/views/LibrarianLoginView.vue';
import LibrarianRequestsView from '@/views/LibrarianRequestsView.vue';

Vue.use(VueRouter);

const routes = [
  { path: '/', component: HomeView },
  { path: '/user-login', component: UserLoginView, name: 'user-login'},
  { path: '/user-register', component: UserRegisterView, name: 'user-register'},
  { path: '/user-all-books', component: UserAllBooksView, name: 'user-all-books'},
  { path: '/user-my-books', component: UserMyBooksView, name: 'user-my-books'},
  { path: '/librarian-add-book/:sectionId', component: LibrarianAddBook, name: 'librarian-add-book'},
  { path: '/librarian-add-section', component: LibrarianAddSection, name: 'librarian-add-section'},
  { path: '/librarian-all-sections', component: LibrarianAllSectionsView, name: 'librarian-all-sections'},
  { path: '/librarian-list-of-books/:sectionId', component: LibrarianListOfBooks, name: 'librarian-list-of-books'},
  { path: '/librarian-login', component: LibrarianLoginView, name: 'librarian-login'},
  { path: '/librarian-requests', component: LibrarianRequestsView, name: 'librarian-requests'}
];

const router = new VueRouter({
  mode: 'history',
  routes
});

export default router;
