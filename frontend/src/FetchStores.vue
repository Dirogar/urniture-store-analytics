<template>/*Для названия магазинов*/</template>
<script>
import axios from "axios";

export const fetchStores = () => axios.get("http://localhost:8000/api/v1/stores/")
    .then(res => {
      const stores = res.data.results;
      const storeNames = stores.map(item => item.name).sort();
      return {stores, storeNames}; // Возвращаем объект с данными
    })
    .catch(err => {
      console.error("Stores fetch error:", err);
      throw err; // Пробрасываем ошибку для обработки
    });

</script>
