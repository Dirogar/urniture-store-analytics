<!-- src/components/Login.vue -->
<template>
  <div class="auth-container">
    <h2 style=" font-size: 20px; text-align: center; top: 0;">Авторизация</h2>
    <input type="text" class="username" placeholder="Логин" v-model="username" />
    <input type="password" class="password" placeholder="Пароль" v-model="password" />
    <button class="button-enter" @click="login">Войти</button>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
    };
  },
  methods: {
    login() {
      if (this.username === '1' && this.password === '1') {
        this.$emit('auth-success'); // Сообщаем родителю об успехе
      } else {
        this.error = 'Неверный логин или пароль';
      }
    },
  },
};
</script>

<style>
.button-enter{
    width: 100%;
    padding: 10px;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  font-size: 20px;
}
.auth-container {
  width: 400px;
  margin: 15% auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  background-color: rgb(255, 255, 255);
}
.password{
  font-size: 20px;
  width: 95%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.username {
  font-size: 20px;
  width: 95%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button:hover {
  background-color: #0056b3;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>
