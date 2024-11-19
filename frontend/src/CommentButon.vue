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
  padding: 0px 0px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
}

.my-button:hover {
  background-color: #0056b3;
}
</style>
