<template>
  <div>
    <button @click="openModal" class="my-button">Комментарий</button>

    <!-- Модальное окно с переданным названием магазина -->
    <Modal ref="modal" :title="` ${shopName} - ${goodName} - ${goodArticle}` ">
      <hr />
    </Modal>

  </div>
</template>

<script>
import Modal from "./CommentWindow.vue";

export default {
  components: { Modal },
  props: {
    shopName: {
      type: String,
      required: true
    },
    goodArticle: {
      type: String,
      required: true
    },
    goodName:{
      type: String,
      required: true
    }
  },
  methods: {
    openModal() {
      this.$refs.modal.openModal();
    }
  }
};
</script>

<style scoped>
.my-button {
  font-size:20px;
  padding: 0 0;
  background-color: #007efb;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: opacity 0.5s ease, transform 0.5s ease, visibility 10s linear 0.5s;
  height: 25px;
  width: auto;

}

.my-button:hover {
  background-color: #0056b3;
}
</style>
