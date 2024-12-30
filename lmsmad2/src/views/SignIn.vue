<template>
  <div class="sign-in">
    <header>
      <h1>Sign In</h1>
    </header>
    <form @submit.prevent="signin_fn">
      <div class="form-group">
        <input type="email" v-model="emailv" placeholder="Email" required />
      </div>
      <div class="form-group">
        <input type="password" v-model="passwordv" placeholder="Password" required />
      </div>
      <button class="button" type="submit">Sign In</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <p>Don't have an account? <router-link to="/signup">Sign Up</router-link></p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      emailv: '',
      passwordv: '',
      errorMessage: ''
    };
  },
  methods: {
    signin_fn() {
      this.errorMessage = '';
      console.log('Attempting to sign in with email:', this.emailv);
      console.log('Attempting to sign in with password:', this.passwordv);
      axios
        .post('http://localhost:3000/signin', 
          { 
            email: this.emailv,
            password: this.passwordv
          },
        )
        .then(response => {
          console.log('Response status:', response.status);
          if (response.status === 200) {
            const token = response.data.authToken;
            console.log('Token received:', token);
            if (!token) {
              this.errorMessage = 'Token not received from the server.';
              return;
            }

            localStorage.setItem('authToken', token);
            const userRole = response.data.role;
            console.log('User role:', userRole);

            if (userRole === 'admin') {
              this.$router.push('/admindashboard');
            } else {
              this.$router.push('/userdashboard');
            }
          } else {
            this.errorMessage = 'Invalid email or password';
          }
        })
        .catch(error => {
          console.error('Error signing in:', error.response ? error.response.data : error.message);
          this.errorMessage = 'Can not find user with this email and password';
        });
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.sign-in {
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
  margin-right: 10px;
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