<template>
  <div class="sign-up">
    <header>
      <h1>Sign Up</h1>
    </header>
    <form @submit.prevent="register_fn">
      <div class="form-group">
        <input type="email" v-model="emailv" placeholder="Email" required />
      </div>
      <div class="form-group">
        <input type="text" v-model="usernamev" placeholder="Username" required />
      </div>
      <div class="form-group">
        <input type="password" v-model="passwordv" placeholder="Password" required />
      </div>
      <button class="button" type="submit">Sign Up</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <p>Already have an account? <router-link to="/signin">Sign In</router-link></p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterView',
  data() {
    return {
      emailv: '',
      usernamev: '',
      passwordv: '',
      errorMessage: ''
    };
  },
  methods: {
    // Register function for user
    register_fn() {
      this.errorMessage = ''; // Clear any previous error messages
      axios
        .post('http://localhost:3000/signup', {
          email: this.emailv,
          password: this.passwordv,
          username: this.usernamev
        })
        .then(response => {
          if (response.status === 201) {
            this.$router.push('/signin');
          } else {
            this.errorMessage = 'Registration failed. Please try again.';
          }
        })
        .catch(error => {
          console.error('Error registering:', error.response ? error.response.data : error.message);
          this.errorMessage = 'Error registering. Please try again.';
        });
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.sign-up {
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
  margin-bottom: 20px;
  margin-right: 20px;
}

.form-group input {
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

.error {
  color: #e74c3c;
  margin-top: 20px;
}
</style>