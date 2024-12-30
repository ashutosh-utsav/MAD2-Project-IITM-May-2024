<template>
    <div class="app-stats">
      <header>
        <h1>App Statistics</h1>
        <button class="button1" @click="goBack">Back to Dashboard</button>
      </header>
      <div class="content">
        <div class="stats-container">
          <div class="stat-card">
            <strong>Total Users:</strong>
            <p>{{ totalUsers }}</p>
            <button class="button" @click="goToUserManagement">View/Modify Users</button>
          </div>
          <div class="stat-card">
            <strong>Total Books:</strong>
            <p>{{ totalBooks }}</p>
          </div>
          <div class="stat-card">
            <strong>Total Sections:</strong>
            <p>{{ totalSections }}</p>
          </div>
          <div class="stat-card">
            <strong>Total Approved Requests:</strong>
            <p>{{ approvedRequests }}</p>
          </div>
          <div class="stat-card">
            <strong>Current Pending Request:</strong>
            <p>{{ pendingRequests }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'AppStats',
    data() {
      return {
        totalUsers: 0,
        totalBooks: 0,
        totalSections: 0,
        totalRequests: 0,
        approvedRequests: 0,
        deniedRequests: 0,
        token: null,
        errorMessage: ''
      };
    },
    created() {
      this.token = localStorage.getItem('authToken');
      if (!this.token) {
        this.$router.push('/signin');
      } else {
        this.fetchStats();
      }
    },
    methods: {
      goToUserManagement() {
           this.$router.push('/user-management');
    },
      fetchStats() {
        axios
          .get('http://localhost:3000/app-stats', {
            headers: { Authorization: `${this.token}` }
          })
          .then(response => {
            const stats = response.data;
            this.totalUsers = stats.totalUsers;
            this.totalBooks = stats.totalBooks;
            this.totalSections = stats.totalSections;
            this.totalRequests = stats.totalRequests;
            this.approvedRequests = stats.approvedRequests;
            this.deniedRequests = stats.deniedRequests;
            this.pendingRequests = stats.pendingRequests;
          })
          .catch(error => {
            this.errorMessage = error.response ? error.response.data.message : 'An unexpected error occurred.';
            console.error('Error fetching stats:', this.errorMessage);
          });
      },
      goBack() {
        this.$router.push('/admindashboard');
      }
    }
  };
  </script>
  
  <style scoped>
  .app-stats {
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
  
  .stats-container {
    display: grid;
    grid-gap: 20px;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
  
  .stat-card {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
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
  .button1 {
    background-color: #2980b9;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
  }
  
  .button1:hover {
    background-color: green;
  }
  </style>
  