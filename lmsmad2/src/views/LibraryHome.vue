<template>
  <div class="library-home">
    <header>
      <h1>Welcome to the Library Management System</h1>
      <h2>IITM MAD2 PROJECT</h2>
      <p>Something Something cool cool</p>
    </header>
    <div class="actions">
      <button class="button" @click="goToSignUp">Sign Up</button>
      <button class="button" @click="goToSignIn">Sign In</button>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    goToSignUp() {
      this.$router.push('/signup'); 
    },
    goToSignIn() {
      this.$router.push('/signin');
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.library-home {
  font-family: 'Roboto', sans-serif;
  color: #333;
  background-color: #f4f4f4;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
}

header {
  margin-bottom: 40px;
}

header h1 {
  font-size: 36px;
  color: #2c3e50;
  margin-bottom: 10px;
}

header h2 {
  font-size: 24px;
  color: #2980b9;
  margin-bottom: 20px;
}

header p {
  font-size: 18px;
  color: #555;
  margin-bottom: 40px;
}

.actions {
  display: flex;
  gap: 20px;
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
</style>