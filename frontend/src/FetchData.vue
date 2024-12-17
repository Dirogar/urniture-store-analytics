<template>/*Для товаров*/</template>
<script>
import axios from "axios";

export function fetchData(searchTerm,currentPage) {
        if(!searchTerm.trim()){
          return axios.get(`http://localhost:8000/api/v1/products/?page=${currentPage}`)
              .then(res => {
                return {
                  products: res.data.results, // Список товаров

                  totalItems: res.data.count, // Общее количество товаров
                  nextURL: res.data.next, // URL для следующей страницы
                  prevURL: res.data.previous, // URL для предыдущей страницы
                };
              })
              .catch(err => console.error("Product fetch error:", err));
        }
        else{
          return axios.get(`http://localhost:8000/api/v1/products/${searchTerm.trim()}/`)
              .then(res => {
                return{
                  products: [res.data],
                  totalItems: null,
                  nextURL: null,
                  prevURL: null,
                };
              })
              .catch(err => {
                console.log(err);
              })

        }
      }


</script>