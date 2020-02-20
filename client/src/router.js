import Vue from 'vue';
import Router from 'vue-router';
import Users from './components/Users.vue';
import Groups from './components/Groups.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Users',
      component: Users,
    },
    {
      path: '/groups',
      name: 'Groups',
      component: Groups,
    },
  ],
});
