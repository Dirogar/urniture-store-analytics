<template>/*Для названия магазинов*/</template>
<script>
import axios from "axios";

export const fetchStores = (setStores, setStoreNames) => axios.get("http://localhost:8000/api/v1/stores/")
    .then(res => {
      const stores = res.data.results;
      const storeNames = stores.map(item => item.name).sort();
      setStores(stores); // Передаем данные обратно через функции
      setStoreNames(storeNames);
    })
    .catch(err => console.error("Stores fetch error:", err));

</script>
