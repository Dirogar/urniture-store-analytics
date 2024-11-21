<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal">
      <div class="modal-header">
        <h3>{{ title }}</h3>
        <div>
        <button @click="closeModal" class="close-button">&times;</button>
        </div>
      </div>
      <div class="modal-body">

        <slot></slot> <!-- Слот для передачи содержимого в модальное окно -->
      </div>
      <div class="textarea_input">
        <label class="form-label">Комментарий</label>
        <textarea name="text" class="form-control" placeholder="Введите комментарий"></textarea>
      </div>

      <div class="date-input">
      <label class="date-complete">Планируемая дата выполнения</label>

      <input class="data-calendar" type="date" id="start" name="trip-start"/>
        <div>
          <button class="send-data">Отправить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: 'Модальное окно'
    }
  },
  data() {
    return {
      isVisible: false
    };
  },
  methods: {
    openModal() {
      this.isVisible = true;
    },
    closeModal() {
      this.isVisible = false;
    }
  }

};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(94, 89, 89, 0.48);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: #eef4fd;
  border-radius: 15px;
  padding: 20px; /* Добавлен отступ внутри модального окна */
  width: 100%;
  max-width: 80%; /* Ограничение ширины для адаптации */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Легкая тень для выделения окна */
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 0s linear 0.5s;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 15px; /* Отступ снизу для разделения от основного содержимого */
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 0s linear 0.5s;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 0s linear 0.5s;
}

h3 {
  font-size: 24px;
  margin: 0; /* Убираем внешние отступы */
  font-family: Arial, sans-serif;
  font-weight: 400;
  text-align: center;
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 0s linear 0.5s;
}

.form-label {
  font-size: 18px;
  margin-bottom: 5px;
  margin-left: 68%;
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 0s linear 0.5s;
}

.form-control {
  width: 30%; /* Полная ширина для выравнивания с меткой */
  padding: 10px;
  margin-left: 68%;
  font-size: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: vertical;
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 0s linear 0.5s;
}

.textarea_input {
  display: flex;
  flex-direction: column; /* Размещает метку над полем ввода */
  align-items: flex-start; /* Выравнивание по левому краю */
  width: 100%; /* Занимает всю ширину контейнера */
  margin-bottom: 15px; /* Отступ снизу для разделения с другими элементами */
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 0s linear 0.5s;
}

.date-input {
  display: flex;
  flex-direction: column; /* Размещаем метку и поле ввода вертикально */
  gap: 5px; /* Добавляем небольшой отступ между меткой и полем */
  margin-bottom: 15px; /* Добавляем отступ снизу */
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 0s linear 0.5s;
}

.date-complete {
  font-size: 16px;
  font-weight: bold;
  margin-left: 53%;
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 0s linear 0.5s;
}

.data-calendar {
  padding: 8px;
  font-size: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-left: 68%;
  width: 30%;
}
.send-data{
  margin-top: 10px;
  width: 32%;
  height: 35px;
  margin-left: 68%;
  font-size: 16px;
  background-color: #4250ed;
  border-radius: 5px;
border: none;
  color: white;

}
.send-data:hover{
  background-color: #529ffa;
}
</style>

