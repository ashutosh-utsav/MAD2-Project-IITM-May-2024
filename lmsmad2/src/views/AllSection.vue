<template>
    <div>
      <header>
        <h1>All Sections</h1>
      </header>
      <div class="content">
        <div class="section-container">
          <div v-for="section in sections" :key="section.id" class="section-card">
            <div class="section-details">
              <strong>{{ section.name }}</strong>
              <p>{{ section.description }}</p>
            </div>
            <div class="section-actions">
              <button class="button1" @click="goToSection(section.id)">Go to Section</button>
              <button class="button2" @click="startEditing(section)">Edit</button>
              <button class="button3" @click="deleteSection(section.id)">Delete</button>
            </div>
          </div>
        </div>
      </div>
  
      <div v-if="editingSection" class="edit-section">
        <h2>Edit Section</h2>
        <form @submit.prevent="editSection">
          <div>
            <label for="name">Name:</label>
            <input type="text" v-model="editingSection.name" id="name" required>
          </div>
          <div>
            <label for="description">Description:</label>
            <textarea v-model="editingSection.description" id="description" required></textarea>
          </div>
          <button type="submit" class="button2">Save</button>
          <button @click="cancelEditing" class="button3">Cancel</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AllSection',
    data() {
      return {
        sections: [],
        editingSection: null,
        errorMessage: ''
      };
    },
    created() {
      this.fetchAllSections();
    },
    methods: {
          deleteSection(sectionId) {
        axios
          .delete(`http://localhost:3000/book_section/${sectionId}`)
          .then(response => {
            console.log('Response:', response.status);
            this.fetchAllSections(); 
          })
          .catch(error => {
            this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
            console.error('Error:', this.errorMessage);
          });
    },

      goToSection(sectionId) {
        this.$router.push(`/sections/${sectionId}`);
    },  
      startEditing(section) {
        this.editingSection = { ...section }; 
      },
      cancelEditing() {
        this.editingSection = null;
      },
      editSection() {
        axios
          .put(`http://localhost:3000/book_section`, {
            id: this.editingSection.id,
            name: this.editingSection.name,
            description: this.editingSection.description
          })
          .then(response => {
            console.log('Response:', response.status);
            this.fetchAllSections(); 
            this.cancelEditing(); 
          })
          .catch(error => {
            this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
            console.error('Error:', this.errorMessage);
          });
      },
      rejectRequest(requestId) {
          axios
            .delete(`http://localhost:3000/request_book`, {
              headers: { Authorization: `${this.token}` },
              data: { id: requestId } 
            })
            .then(response => {
              console.log('Response:', response.status);
              this.fetchBookRequests(); 
            })
            .catch(error => {
              this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
              console.error('Error:', this.errorMessage);
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
      text-align: center;
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

    .button1 {
      background-color: #007bff;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 5px;
      cursor: pointer;
      text-align: center;
      margin: 5px;
      transition: background-color 0.3s ease;
    }

    .button1:hover {
      background-color: #0056b3;
    }

    .button2 {
      background-color: #28a745;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 5px;
      cursor: pointer;
      text-align: center;
      margin: 5px;
      transition: background-color 0.3s ease;
    }

    .button2:hover {
      background-color: #218838;
    }

    .button3 {
      background-color: #dc3545;
      color: white;
      border: none;
      padding: 10px 15px;
      border-radius: 5px;
      cursor: pointer;
      text-align: center;
      margin: 5px;
      transition: background-color 0.3s ease;
    }

    .button3:hover {
      background-color: #c82333;
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

    .success-message {
      color: green;
      margin-top: 10px;
    }
  </style>
  