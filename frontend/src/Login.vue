<!-- src/components/Login.vue -->
<template>
  <div class="auth-container">
    <h2  class="auth" style=" font-size: 20px; text-align: center; top: 0;">Добро Пожаловать!</h2>
    <input type="text" class="username" placeholder="Логин" v-model="username" />
    <input type="password" class="password" placeholder="Пароль" v-model="password" />
    <button class="button-enter" @click="login">Войти</button>


    <p v-if="error" class="error">{{ error }}</p>
  </div>
  <div class="name-logo">
    <img :src="logo" alt="Логотип Matrix" class="logo-auth"/>
    <span class="Matrix-auth">Matrix</span>
  </div>
</template>

<script>
import logo from './logo.png'


export default {
  data() {
    return {
      username: '',
      password: '',
      error: null,
      logo
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
.auth{
  font-family: "Varela Round", "Comfortaa Light", Verdana, Geneva, Tahoma, sans-serif;
}
.auth-container {
  width: 400px;
  height: auto;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  background-color: rgb(255, 255, 255);
  position: fixed;
  top: 45%; /* Чуть выше относительно центра */
  left: 50%;
  transform: translate(-50%, -50%);
}

.name-logo {
  width: 400px;
  padding: 20px;
  border-radius: 8px;
  position: fixed;
  top: 25%; /* Выше предыдущего окна */
  left: 50%;
  transform: translate(-50%, -50%);
  margin-bottom: 30px;
  text-align: center;

}

.logo-auth {
  width: 50px;
  text-align: center;
}

.Matrix-auth {
  font-size: 50px;
  color: #000000;
  font-family: "Varela Round", "Comfortaa Light", Verdana, Geneva, Tahoma, sans-serif;
}

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
