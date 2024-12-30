  <template>
    <div class="add-section">
      <h2>Add Section</h2>
      <form @submit.prevent="addsection">
        <div class="form-group">
          <input type="text" v-model="name" placeholder="Title" required />
        </div>
        <div class="form-group">
          <textarea v-model="desc" placeholder="Description" required></textarea>
        </div>
        <button class="button" type="submit">Add Section</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        name: '',
        desc: '',
        errorMessage: ''
      };
    },
    created() {
      this.token = localStorage.getItem('authToken');
      console.log('Token:', this.token);
      if (!this.token) {
        this.$router.push('/signin');
      }
    },
    methods: {
      addsection() {
        axios
          .post('http://localhost:3000/book_section', 
            {
              name: this.name,
              description: this.desc
            }, 
            {
              headers: {
                Authorization: `${this.token}`
              }
            }
          )
          .then(response => {
            console.log('Response status:', response.status);
            if (response.status === 201) {
              this.$router.push('/admindashboard');
            } else {
              this.errorMessage = 'Invalid section';
            }
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
  
  .add-section {
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
    margin: 10px;
  }
  
  h2 {
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
  .form-group textarea {
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
    padding: 10px 10px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }
  
  .button:hover {
    background-color: orange;
  }
  
  .error {
    color: #e74c3c;
    margin-top: 20px;
  }
  </style>
  
  