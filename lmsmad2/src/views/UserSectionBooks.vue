<template>
  <div>
    <header>
      <h1>{{ sectionName }}</h1>
    </header>
    <div class="content">
      <h2>Books in this Section</h2>
      <div v-if="books.length">
        <div v-for="book in books" :key="book.id" class="book-card">
          <div class="book-details">
            <strong>Book Name: {{ book.name }}</strong>
            <p><strong>Author:</strong> {{ book.author }}</p>
            <p>Quantity: {{ book.quantity }}</p>
          </div>
          <div class="book-actions">
            <button class="button3" @click="requestBook(book.id)">Request the Book</button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No books found in this section.</p>
      </div>
      <p v-if="message" :class="messageClass">{{ message }}</p> 
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SectionBooks',
  data() {
    return {
      sectionId: this.$route.params.id,
      sectionName: '',
      books: [],
      sections: [],
      editingBook: null,
      message: '', 
      messageClass: '' 
    };
  },
  created() {
    this.fetchSectionBooks();
    this.fetchAllSections();
    this.token = localStorage.getItem('authToken'); 
  },
  methods: {
    fetchSectionBooks() {
      axios
        .get(`http://localhost:3000/book_section/${this.sectionId}`)
        .then(response => {
          console.log('API response:', response.data);
          this.sectionName = response.data.section.name;
          this.books = response.data.books;
          console.log('Books:', this.books);
        })
        .catch(error => {
          console.error('Error fetching section books:', error);
        });
    },
    fetchAllSections() {
      axios
        .get('http://localhost:3000/book_section')
        .then(response => {
          this.sections = response.data.data;
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
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
.header {
  padding: 20px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.content {
  padding: 20px;
}

.book-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px 0;
  border-radius: 4px;
  background-color: #fff;
}

.book-details {
  margin-bottom: 10px;
}

.book-actions {
  display: flex;
  justify-content: space-between;
}

.button2 {
  padding: 10px 20px;
  background-color: #0f4d8e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button3 {
  padding: 10px 20px;
  background-color: #0f4d8e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button2:hover {
  background-color: orange;
}

.button3:hover {
  background-color: red;
}

.edit-book {
  margin-top: 20px;
}

.edit-book form {
  display: flex;
  flex-direction: column;
}

.edit-book label {
  margin-top: 10px;
}

.edit-book input,
.edit-book textarea,
.edit-book select {
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* Add styles for message */
.message {
  margin-top: 20px;
  font-size: 16px;
}

.message.success {
  color: #2ecc71;
}

.message.error {
  color: #e74c3c;
}
</style>
