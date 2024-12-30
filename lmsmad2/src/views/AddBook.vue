<template>
  <div class="add-book">
    <header>
      <h1>Add Book</h1>
    </header>
    <form @submit.prevent="addBook">
      <div class="form-group">
        <input type="text" v-model="name" placeholder="Book Name" required />
      </div>
      <div class="form-group">
        <input type="text" v-model="author" placeholder="Author" required />
      </div>
      <div class="form-group">
        <textarea v-model="content" placeholder="Content" required></textarea>
      </div>
      <div class="form-group">
        <select v-model="sectionId" required>
          <option disabled value="">Select Section</option>
          <option v-for="section in sections" :key="section.id" :value="section.id">
            {{ section.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <input type="number" v-model="quantity" placeholder="Quantity" required />
      </div>
      <button class="button" type="submit">Add Book</button>
      <p v-if="message" :class="messageClass">{{ message }}</p>
      
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      name: '',
      author: '',
      content: '',
      sectionId: null,
      quantity: null,
      sections: [],
      message: '',
      messageClass: '',
    };
  },
  created() {
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      this.$router.push('/signin');
    } else {
      this.fetchSections();
    }
  },
  methods: {
    fetchSections() {
      axios
        .get('http://localhost:3000/book_section', {
          headers: { Authorization: `${this.token}` },
        })
        .then(response => {
          if (response.status === 200) {
            this.sections = response.data.data;
          } else {
            this.message = 'Failed to load sections';
            this.messageClass = 'error';
          }
        })
        .catch(error => {
          this.message = error.response ? error.response.data.message : 'An unexpected error occurred.';
          this.messageClass = 'error';
        });
    },
    addBook() {
      axios
        .post(
          'http://localhost:3000/book',
          {
            name: this.name,
            author: this.author,
            content: this.content,
            section_id: this.sectionId,
            quantity: this.quantity,
          },
          {
            headers: { Authorization: `${this.token}` },
          }
        )
        .then(response => {
          if (response.status === 201) {
            this.$router.push('/admindashboard');
            this.message = 'Book added successfully.';
            this.messageClass = 'success';
          } else {
            this.message = 'An unexpected error occurred.';
            this.messageClass = 'error';
          }
        })
        .catch(error => {
          this.message = error.response ? error.response.data.message : 'An unexpected error occurred.';
          this.messageClass = 'error';
        });
    },
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.add-book {
  font-family: 'Roboto', sans-serif;
  color: #333;
  background-color: #f4f4f4;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
  padding: 20px;
}

header {
  margin-bottom: 40px;
}

header h1 {
  font-size: 36px;
  color: #2c3e50;
  margin-bottom: 20px;
}

form {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin: 20px;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.button {
  background-color: #2980b9;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: orange;
}

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
