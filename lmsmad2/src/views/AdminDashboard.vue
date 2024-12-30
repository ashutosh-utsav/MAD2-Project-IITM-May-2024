<template>
  <div>
    <header>
      <h1>Welcome, Admin</h1>
      <div class="user-actions">
        <div class="search-bar">
        </div>
        <button class="button" @click="download">Download</button>
        <button class="button" @click="goToAppStats">App Stats</button>
        <button class="button" @click="goToAddSection">Add Section</button>
        <button class="button" @click="goToAddBook">Add Book</button>
        <button class="button logout" @click="logout">Log Out</button>
      </div>
    </header>
    <div class="content">
      <div class="section-container">
        <h2>All Sections</h2>
        <div class="sections">
          <div v-for="section in visibleSections" :key="section.id" class="section-card">
            <div class="section-details">
              <strong>{{ section.name }}</strong>
              <p>{{ section.description }}</p>
            </div>
            <button class="button" @click="goToSection(section.id)">Go to this section</button>
          </div>
        </div>
        <button class="button show-all" @click="goToAllSections">Show All Sections</button>
      </div>
      <hr class="divider" />
      <div class="section-container">
        <h2>Book Requests</h2>
        <div class="requests">
          <div v-for="request in bookRequests" :key="request.id" class="request-card">
            <div class="request-details">
              <strong>Request ID: {{ request.id }}</strong>
              <p>User: {{ request.user.email }}</p>
              <p>Book Title: {{ request.book.name }}</p>
              <p>Requested On: {{ request.request_date }}</p>
              <p>Status: {{ request.status ? 'Approved' : 'Pending' }}</p>
            </div>
            <div class="request-actions">
              <button class="button approve" @click="approveRequest(request.id)">Approve</button>
              <button class="button deny" @click="rejectRequest(request.id)">Deny</button>
            </div>
          </div>
          <p v-if="bookRequests.length === 0">No book requests found.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminDashboard',
  data() {
    return {
      query: '',
      latestSection: [],
      bookRequests: [],
      showAll: false,
      token: null,
      errorMessage: ''
    };
  },
  created() {
    this.token = localStorage.getItem('authToken');
    if (!this.token) {
      this.$router.push('/signin');
    } else {
      this.fetchLatestSections();
      this.fetchBookRequests();
    }
  },
  computed: {
    visibleSections() {
      return this.showAll ? this.latestSection : this.latestSection.slice(0, 5);
    }
  },
  methods: {
    download(){
      window.location.href = 'http://localhost:3000/download-books-csv';
    },
    goToAppStats() {
      this.$router.push('/app-stats');
    },
    fetchLatestSections() {
      axios
        .get('http://localhost:3000/book_section', {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        .then(response => {
          this.latestSection = response.data.data;
        })
        .catch(error => {
          console.error('Error fetching sections:', error);
        });
    },
    fetchBookRequests() {
      axios
        .get('http://localhost:3000/request_book', {
          headers: { Authorization: `${this.token}` }
        })
        .then(response => {
          this.bookRequests = response.data.data;
        })
        .catch(error => {
          console.error('Error fetching book requests:', error);
        });
    },
    goToAddBook() {
      this.$router.push('/add-book');
    },
    goToAddSection() {
      this.$router.push('/add-section');
    },
    logout() {
      localStorage.removeItem('authToken');
      this.$router.push('/signin');
    },
    goToSection(sectionId) {
      if (sectionId === null) {
        this.$router.push('/books/no-section');
      } else {
        this.$router.push(`/sections/${sectionId}`);
      }
    },
    goToAllSections() {
      this.$router.push('/all-sections');
    },
    approveRequest(requestId) {
      axios
        .put(`http://localhost:3000/request_book/${requestId}`, {}, {
          headers: { Authorization: `${this.token}` }
        })
        .then(response => {
          console.log('Response:', response.status);
          this.bookRequests = this.bookRequests.filter(request => request.id !== requestId);
        })
        .catch(error => {
          this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
          console.error('Error:', this.errorMessage);
        });
    },
    rejectRequest(requestId) {
      axios
        .delete(`http://localhost:3000/request_book/${requestId}`, {
          headers: { Authorization: `${this.token}` }
        })
        .then(response => {
          console.log('Response:', response.status);
          this.bookRequests = this.bookRequests.filter(request => request.id !== requestId); 
        })
        .catch(error => {
          this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
          console.error('Error:', this.errorMessage);
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
.sections, .requests {
  display: grid;
  grid-gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
}
.section-card, .request-card {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.section-details, .request-details {
  margin-bottom: 20px;
}
.section-details strong, .request-details strong {
  font-size: 18px;
  color: #2c3e50;
}
.section-details p, .request-details p {
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
.button:hover {
    background-color: orange;
  }
.button.approve {
  background-color: #27ae60;
  margin: 15px;
}
.button.deny {
  background-color: #e74c3c;
  margin: 5px;
}
.button.show-all {
  margin-top: 20px;
  background-color: #3498db;
}
.button.show-all:hover {
  background-color: orange;
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
