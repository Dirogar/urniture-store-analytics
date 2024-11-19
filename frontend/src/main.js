import './assets/main.css'; // Импорт стилей
import { createApp } from 'vue'; // Импорт функции для создания приложения Vue
import App from './App.vue'; // Импорт основного компонента App
import { library } from '@fortawesome/fontawesome-svg-core'; // Импорт библиотеки Font Awesome
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'; // Импорт компонента Font Awesome
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons'; // Импорт иконки лупы
import { createHead } from '@vueuse/head'; // Импорт функции для работы с мета-тегами

// Добавление иконки в библиотеку
library.add(faMagnifyingGlass);

// Создание приложения Vue
const app = createApp(App);

// Создание объекта для работы с мета-тегами
const head = createHead();

// Использование head-плагина в приложении
app.use(head);

// Регистрация компонента Font Awesome
app.component('font-awesome-icon', FontAwesomeIcon);

// Монтирование приложения в элемент с ID "app"
app.mount('#app');
