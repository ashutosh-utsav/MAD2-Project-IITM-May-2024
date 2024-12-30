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
              <strong>Book Name:{{ book.name }}</strong>
              <p><strong>Author:</strong>{{ book.author }}</p>
                <p>Quantity: {{ book.quantity }}</p>
            </div>
            <div class="book-actions">
              <button class="button2" @click="startEditing(book)">Edit</button>
              <button class="button3" @click="deleteBook(book.id)">Delete</button>
            </div>
          </div>
        </div>
        <div v-else>
          <p>No books found in this section.</p>
        </div>
  
        <div v-if="editingBook" class="edit-book">
          <h2>Edit Book</h2>
          <form @submit.prevent="editBook">
            <div>
              <label for="name">Name:</label>
              <input type="text" v-model="editingBook.name" id="name" required>
            </div>
            <div>
              <label for="author">Author:</label>
              <input type="text" v-model="editingBook.author" id="author" required>
            </div>
            <div>
              <label for="content">Content:</label>
              <textarea v-model="editingBook.content" id="content" required></textarea>
            </div>
            <div>
              <label for="section">Section:</label>
              <select v-model="editingBook.section_id" id="section" required>
                <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
              </select>
            </div>
            <div>
              <label for="quantity">Quantity:</label>
              <input type="number" v-model="editingBook.quantity" id="quantity" required>
            </div>
            <button type="submit" class="button2">Save</button>
            <button @click="cancelEditing" class="button3">Cancel</button>
          </form>
        </div>
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
        editingBook: null
      };
    },
    created() {
      this.fetchSectionBooks();
      this.fetchAllSections();
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
      startEditing(book) {
        this.editingBook = { ...book }; 
      },
      cancelEditing() {
        this.editingBook = null;
      },
      editBook() {
        console.log('Editing book:', this.editingBook);
        axios
          .put(`http://localhost:3000/book/${this.editingBook.id}`, {
            name: this.editingBook.name,
            Nname: this.editingBook.name,
            description: this.editingBook.content,
            author: this.editingBook.author,
            section_id: this.editingBook.section_id,
            quantity: this.editingBook.quantity
          })
          .then(response => {
            console.log('Response:', response.data);
            this.fetchSectionBooks(); 
            this.cancelEditing(); 
          })
          .catch(error => {
            console.error('Error editing book:', error);
          });
      },
      deleteBook(bookId) {
        axios
          .delete('http://localhost:3000/book', {
            data: { id: bookId } 
          })
          .then(response => {
            console.log('Response:', response.status);
            this.fetchSectionBooks();
          })
          .catch(error => {
            console.error('Error deleting book:', error);
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
  </style>
  