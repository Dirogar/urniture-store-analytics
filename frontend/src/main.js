import './assets/main.css'; // Импорт стилей
import { createApp } from 'vue'; // Импорт функции для создания приложения Vue
import App from './App.vue'; // Импорт основного компонента App
import { createHead } from '@vueuse/head'; // Импорт функции для работы с мета-тегами


// Создание приложения Vue
const app = createApp(App);
// Создание объекта для работы с мета-тегами
const head = createHead();
// Использование head-плагина в приложении
app.use(head);
// Монтирование приложения в элемент с ID "app"
app.mount('#app');
