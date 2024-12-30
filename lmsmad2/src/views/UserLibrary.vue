<template>
    <div>
      <header>
        <h1>Your Library</h1>
        <button class="button" @click="goBack">Back to Dashboard</button>
      </header>
      <div class="content">
        <div class="book-container">
          <div v-for="book in books" :key="book.id" class="book-card">
            <div class="book-details">
              <strong>{{ book.name }}</strong>
              <p>{{ book.author }}</p>
            </div>
            <div class="book-actions">
              <button class="button view" @click="viewBook(book.content)">View Book</button>
              <button class="button return" @click="returnBook(book.id)">Return Book</button>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Modal for viewing book content -->
      <div v-if="showModal" class="modal">
        <div class="modal-content">
          <span class="close" @click="closeModal">&times;</span>
          <h2>{{ modalTitle }}</h2>
          <p>{{ modalContent }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'UserLibrary',
    data() {
      return {
        books: [],
        token: null,
        showModal: false,
        modalTitle: '',
        modalContent: '',
      };
    },
    created() {
      this.token = localStorage.getItem('authToken');
      console.log('Retrieved token:', this.token); // Debugging log
      if (!this.token) {
        this.$router.push('/signin');
      } else {
        this.fetchUserLibrary();
      }
    },
    methods: {
      fetchUserLibrary() {
        axios
          .get('http://localhost:3000/user_library', {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            console.log('Response data:', response.data); // Debugging log
            this.books = response.data.data;
          })
          .catch(error => {
            console.error('Error fetching user library:', error);
            console.error('Error details:', error.response.data); // More detailed error log
          });
      },
      goBack() {
        this.$router.push('/userDashboard');
      },
      viewBook(content) {
        this.modalTitle = 'Book Content';
        this.modalContent = content;
        this.showModal = true;
      },
      closeModal() {
        this.showModal = false;
        this.modalContent = '';
      },
      returnBook(bookId) {
        axios
          .delete(`http://localhost:3000/return_book/${bookId}`, {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            console.log('Book returned successfully:', response.data);
            this.fetchUserLibrary(); // Refresh the library after returning the book
          })
          .catch(error => {
            console.error('Error returning book:', error);
          });
      }
    }
  };
  </script>
  
  <style scoped>
  body {
    font-family: 'Roboto', sans-serif;
    margin: 0;
    padding: 0;
    color: #333;
    background-color: #f4f4f4;
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
  .book-container {
    display: grid;
    grid-gap: 20px;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
  .book-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .book-details {
    margin-bottom: 20px;
  }
  .book-details strong {
    font-size: 18px;
    color: #2c3e50;
  }
  .book-details p {
    color: #555;
  }
  .book-actions {
    display: flex;
    justify-content: space-between;
  }
  .button {
    background-color: #2980b9;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
    text-align: center;
    margin: 5px;
  }
  .button:hover {
    background-color: green;
  }
  .button.view {
    background-color: #3498db;
  }
  .button.return {
    background-color: #e74c3c;
  }
  .modal {
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
  }
  .modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    width: 80%;
    max-width: 600px;
    text-align: left;
  }
  .close {
    float: right;
    font-size: 24px;
    cursor: pointer;
  }
  </style>
  