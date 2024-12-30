<template>
    <div class="search-page">
      <header>
        <h1>Search Results</h1>
        <form @submit.prevent="search">
          <input type="text" v-model="query" placeholder="Search books/sections..." required />
          <button class="button" type="submit">Search</button>
        </form>
        <button class = "button" @click = "goback">Dashboard</button>
      </header>
      <div class="content">
        <div v-if="searchResults.books.length || searchResults.sections.length">
          <div class="search-results">
            <div v-if="searchResults.sections.length">
              <h3>Sections</h3>
              <div v-for="section in searchResults.sections" :key="section.id" class="result-card">
                <div class="section-details">
                  <strong>{{ section.name }}</strong>
                  <p>{{ section.description }}</p>
                </div>
                <button class="button" @click="goToSection(section.id)">Go to this section</button>
              </div>
            </div>
            <div v-if="searchResults.books.length">
              <h3>Books</h3>
              <div v-for="book in searchResults.books" :key="book.id" class="result-card">
                <div class="book-details">
                  <strong>{{ book.name }}</strong>
                  <p>{{ book.author }}</p>
                  <p>{{ book.content }}</p>
                </div>
                <button class="button" @click="requestBook(book.id)">Request this book</button>
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="query">
          <p>No results found for "{{ query }}".</p>
        </div>
        <div v-else>
          <p>Start typing to search for books and sections.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'SearchPage',
    data() {
      return {
        query: this.$route.query.q || '',
        searchResults: {
          books: [],
          sections: []
        },
        errorMessage: '',
        token: null
      };
    },
    created() {
      this.token = localStorage.getItem('authToken');
      if (!this.token) {
        this.$router.push('/signin');
      } else {
        if (this.query) {
          this.search();
        }
      }
    },
    methods: {
       goback(){
            this.$router.push('/userdashboard');
        },
      search() {
        axios.get(`http://localhost:3000/search?q=${this.query}`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(response => {
          this.searchResults = response.data;
        })
        .catch(error => {
          this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
        });
      },
      goToSection(sectionId) {
        this.$router.push(`/user-sections/${sectionId}`);
      },
      requestBook(bookId) {
        axios.post(`http://localhost:3000/request_book`, { book_id: bookId }, {
          headers: { Authorization: `${this.token}` }
        })
        .then(() => {
          this.errorMessage = "Book request sent successfully.";
          this.search();
        })
        .catch(error => {
          this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .search-page {
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
  
  header form {
    display: flex;
    align-items: center;
  }
  
  header input {
    padding: 10px 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-right: 10px;
    font-size: 16px;
  }
  
  header .button {
    background-color: #2980b9;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  header .button:hover {
    background-color: orange;
  }
  
  .content {
    padding: 20px 40px;
  }
  
  .search-results {
    margin-top: 20px;
  }
  
  .result-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }
  
  .result-card .button {
    margin-top: 10px;
  }
  
  .result-card .section-details strong {
    font-size: 18px;
    color: #2c3e50;
  }
  
  .result-card .book-details strong {
    font-size: 18px;
    color: #2c3e50;
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
    background-color: green;
    }
  </style>
  