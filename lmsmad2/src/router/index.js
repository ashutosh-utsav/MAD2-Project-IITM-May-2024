// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LibraryHome from '../views/LibraryHome.vue';
import Signup from '../views/SignUp.vue';
import Signin from '../views/SignIn.vue';
import UserDashboard from '../views/UserDashboard.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import AddSection from '../views/AddSection.vue';
import AddBook from '../views/AddBook.vue';
import AllSection from '@/views/AllSection.vue';
import SectionBooks from '@/views/SectionBooks.vue';
import UserLibrary from '@/views/UserLibrary.vue';
import UserSectionBooks from '@/views/UserSectionBooks.vue';
import AppStats from '@/views/AppStats.vue';
import UserManagement from '@/views/UserManagement.vue';
import AdminUserLibrary from '@/views/AdminUserLibrary.vue';
import Search from '@/views/Search.vue';





const routes = [
  {
    path: '/',
    name: 'LibraryHome',
    component: LibraryHome,
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: Signup,
  },
  {
    path: '/signin',
    name: 'SignIn',
    component: Signin,
  },
  {
    path: '/userdashboard',
    name: 'UserDashboard',
    component: UserDashboard
  },
  {
    path: '/admindashboard',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/add-section',
    name: 'AddSection',
    component: AddSection
  },
  {
    path: '/add-book',
    name: 'AddBook',
    component: AddBook
  },
  {
    path: '/all-sections',
    name: 'AllSection',
    component: AllSection
  },
  {
    path: '/sections/:id',
    name: 'SectionBooks',
    component: SectionBooks
  },
  {
    path: '/user-library',
    name: 'UserLibrary',
    component: UserLibrary
  },
  {
    path: '/user-sections/:id',
    name: 'UserSectionBooks',
    component: UserSectionBooks
  },
  {
    path: '/app-stats',
    name: 'AppStats',
    component: AppStats
  },
  {
    path: '/user-management',
    name: 'UserManagement',
    component: UserManagement
  },
  {
    path: '/admin-user-library/:userId',
    name: 'AdminUserLibrary',
    component: AdminUserLibrary
  },
  {
    path : '/search',
    name : 'Search',
    component : Search
  }
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
