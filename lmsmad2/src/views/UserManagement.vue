<template>
    <div class="user-management">
      <header>
        <h1>User Management</h1>
        <button class="button3" @click="goBack">Back to Stats</button>
      </header>
      <div class="content">
        <div v-if="users.length">
          <div v-for="user in users" :key="user.id" class="user-card">
            <div class="user-details">
              <strong>{{ user.username }}</strong>
              <p>{{ user.email }}</p>
            </div>
            <div class="user-actions">
              <button class="button" @click="viewLibrary(user.id)">See Library</button>
              <button class="button2" @click="removeUser(user.id)">Remove User</button>
            </div>
          </div>
        </div>
        <div v-else>
          <p>No users found.</p>
        </div>
  
        <div v-if="selectedUserLibrary.length" class="user-library">
          <h2>{{ selectedUsername }}'s Library</h2>
          <div v-for="book in selectedUserLibrary" :key="book.id" class="book-card">
            <div class="book-details">
              <strong>{{ book.name }}</strong>
              <p>{{ book.author }}</p>
              <p>{{ book.content }}</p>
              <p><strong>Quantity:</strong> {{ book.quantity }}</p>
            </div>
            <div class="book-actions">
              <button class="button" @click="revokeBook(book.id)">Revoke Book</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserManagement',
    data() {
      return {
        users: [],
        selectedUserLibrary: [],
        selectedUsername: '',
        token: null,
        errorMessage: ''
      };
    },
    created() {
      this.token = localStorage.getItem('authToken');
      if (!this.token) {
        this.$router.push('/signin');
      } else {
        this.fetchUsers();
      }
    },
    methods: {
      fetchUsers() {
        axios
          .get('http://localhost:3000/users', {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            this.users = response.data.data;
          })
          .catch(error => {
            this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
            console.error('Error fetching users:', this.errorMessage);
          });
      },
      removeUser(userId) {
        axios
          .delete(`http://localhost:3000/users/${userId}`, {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            console.log('User removed:', response.data);
            this.users = this.users.filter(user => user.id !== userId);
          })
          .catch(error => {
            this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
            console.error('Error removing user:', this.errorMessage);
          });
      },
      viewLibrary(userId) {
            this.$router.push(`/admin-user-library/${userId}`);
      },
      revokeBook(bookId) {
        axios
          .delete(`http://localhost:3000/return_book/${bookId}`, {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            console.log('Book revoked:', response.data);
            this.selectedUserLibrary = this.selectedUserLibrary.filter(book => book.id !== bookId);
          })
          .catch(error => {
            this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
            console.error('Error revoking book:', this.errorMessage);
          });
      },
      goBack() {
        this.$router.push('/app-stats');
      }
    }
  };
  </script>
  
  <style scoped>
  /* Similar styles to match the design of other pages */
  .user-management {
    font-family: 'Roboto', sans-serif;
    color: #333;
    background-color: #f4f4f4;
    padding: 20px;
  }
  
  header {
    background-color: #2c3e50;
    color: white;
    padding: 20px 40px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  header h1 {
    margin: 0;
    font-size: 28px;
    font-weight: 500;
  }
  
  .content {
    padding: 20px 40px;
  }
  
  .user-card, .book-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .user-details, .book-details {
    flex: 1;
  }
  
  .user-actions, .book-actions {
    display: flex;
    gap: 10px;
  }
  
  .button {
    background-color: #2980b9;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .button:hover {
    background-color: orange;
  }
  .button2 {
    background-color: #2980b9;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .button2:hover {
    background-color: red;
  }
  .button3 {
    background-color: #2980b9;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .button3:hover {
    background-color: green;
  }
  </style>
  