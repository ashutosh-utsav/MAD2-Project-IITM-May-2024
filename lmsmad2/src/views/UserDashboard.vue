<template>
  <div>
    <header>
      <h1>Welcome, User</h1>
      <div class="user-actions">


        <div class="search-bar">
          <form @submit.prevent="searchBooks">
            <input type="text" v-model="query" placeholder="Search books/Section" required />
            <button class="button" type="submit">Search</button>
          </form>
        </div>


        <button class="button" @click="goToLibrary">My Library</button>
        <button class="button logout" @click="logout">Log Out</button>
      </div>
    </header>
    <div class="content">
      <div class="section-container">
        <div v-if="successMessage" class="message success-message">{{ successMessage }}</div>
        <p class="error-message" v-if="errorMessage">{{ errorMessage }}</p>
        <h2>Latest Books</h2>
        <div class="sections">
          <div v-for="book in latestBooks" :key="book.id" class="section-card">
            <div class="section-details">
              <strong>{{ book.name }}</strong>
              <p>{{ book.author }}</p>
            </div>
            <button class="button" @click="requestBook(book.id)">Request Book</button>
          </div>
        </div>
        <button v-if="latestBooks.length > 5" class="button show-all">Show All Books</button>
      </div>
      <hr class="divider">
      <div class="section-container">
        <h2>All The Latest Sections</h2>
        <div class="sections">
          <div v-for="section in latestSections" :key="section.id" class="section-card">
            <div class="section-details">
              <strong>{{ section.name }}</strong>
              <p>{{ section.description }}</p>
            </div>
            <button class="button" @click="goToSection(section.id)">Go to Section</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserDashboard',
  data() {
    return {
      token: null,
      query: '',
      latestBooks: [],
      latestSections: [],
      successMessage: '',
      errorMessage: ''
    };
  },
  created() {
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      this.$router.push('/signin');
    } else {
      this.fetchLatestBooks();
      this.fetchLatestSections();
    }
  },
  methods: {
    goToLibrary() {
      this.$router.push('/user-library');
    },
    fetchLatestBooks() {
      axios
        .get('http://localhost:3000/book', {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(response => {
          this.latestBooks = response.data.data.slice(-5).reverse();
        })
        .catch(error => {
          console.error('Error fetching books:', error);
        });
    },
    fetchLatestSections() {
      axios
        .get('http://localhost:3000/book_section', {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(response => {
          this.latestSections = response.data.data.reverse();
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
    searchBooks() {
      this.$router.push({ name: 'Search', query: { q: this.query } });
    },
    logout() {
      localStorage.removeItem('authToken');
      this.$router.push('/signin');
    },
    goToSection(sectionId) {
      this.$router.push(`/user-sections/${sectionId}`);
    },
    requestBook(bookId) {
      axios
        .post(
          'http://localhost:3000/request_book', 
          { book_id: bookId }, 
          {
            headers: { Authorization: `${this.token}` }
          }
        )
        .then(response => {
          console.log('Book requested successfully:', response.data);
          this.successMessage = 'Book requested successfully.';
          this.errorMessage = '';
        })
        .catch(error => {
          if (error.response && error.response.data.message) {
            this.errorMessage = error.response.data.message;
          } else {
            this.errorMessage = 'An unexpected error occurred.';
          }
          console.error('Error requesting book:', error);
        });
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

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
.user-actions {
  display: flex;
  align-items: center;
}
.user-actions .search-bar {
  margin-right: 20px;
}
.user-actions .search-bar input {
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
}
.user-actions .search-bar button {
  background-color: #2980b9;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}
.user-actions .button.logout {
  background-color: #e74c3c;
}
.content {
  padding: 20px 40px;
}
.section-container {
  margin-bottom: 40px;
}
.section-container h2 {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 20px;
}
.sections {
  display: grid;
  grid-gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
}
.section-card {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.section-details {
  margin-bottom: 20px;
}
.section-details strong {
  font-size: 18px;
  color: #2c3e50;
}
.section-details p {
  color: #555;
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
.button:hover{
  background-color: orange;
}
.button.show-all {
  margin-top: 20px;
  background-color: #3498db;
}
.divider {
  border: 0;
  height: 1px;
  background: #ddd;
  margin: 40px 0;
}
.error-message {
  color: red;
  margin-top: 10px;
}
</style>
