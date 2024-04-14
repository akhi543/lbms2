import Vue from 'vue';
import Vuex from 'vuex';
import user from './user';
import librarian from './librarian';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    user,
    librarian
  }
});
