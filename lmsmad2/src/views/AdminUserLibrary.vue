<template>
    <div class="admin-user-library">
      <header>
        <h1>{{ username }}'s Library</h1>
        <button class="button" @click="goBack">Back to Dashboard</button>
      </header>
      <div class="content">
        <div v-if="books.length">
          <div v-for="book in books" :key="book.id" class="book-card">
            <div class="book-details">
              <strong>{{ book.name }}</strong>
              <p>{{ book.author }}</p>
              <p>{{ book.content }}</p>
            </div>
            <div class="book-actions">
              <button class="button revoke" @click="revokeBook(book.id)">Revoke Access</button>
            </div>
          </div>
        </div>
        <div v-else>
          <p>This user has no books in their library.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AdminUserLibrary',
    data() {
      return {
        books: [],
        username: '',
        token: null,
        errorMessage: ''
      };
    },
    created() {
      this.token = localStorage.getItem('authToken');
      if (!this.token) {
        this.$router.push('/signin');
      } else {
        const userId = this.$route.params.userId;
        this.fetchUserLibrary(userId);
      }
    },
    methods: {
      fetchUserLibrary(userId) {
        axios
          .get(`http://localhost:3000/admin_user_library/${userId}`, {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            this.books = response.data.books;
            this.username = response.data.username;
          })
          .catch(error => {
            this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
            console.error('Error fetching user library:', this.errorMessage);
          });
      },
      revokeBook(bookId) {
        const userId = this.$route.params.userId;
        axios
          .delete(`http://localhost:3000/admin_user_library/${bookId}/${userId}`, {
            headers: { Authorization: `${this.token}` }
          })
          .then(() => {
            this.books = this.books.filter(book => book.id !== bookId);
          })
          .catch(error => {
            console.error('Error revoking book:', error);
          });
      },
      goBack() {
        this.$router.push('/admindashboard');
      }
    }
  };
  </script>
  
  <style scoped>
  .admin-user-library {
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
  .book-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }
  .book-details {
    margin-bottom: 10px;
  }
  .book-actions {
    display: flex;
    justify-content: flex-end;
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
  .button.revoke {
    background-color: #e74c3c;
  }
  .button.revoke:hover {
    background-color: red;
  }
  </style>
  