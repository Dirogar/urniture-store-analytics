<template>

</template>

<script>
import axios from "axios";
export function fetchData(searchTerm) {
        if(!searchTerm.trim()){
          return axios.get('http://localhost:8000/api/v1/products/')
              .then(res => {
                return res.data.results;
              })
              .catch(err => console.error("Product fetch error:", err));
        }
        else{
          return axios.get(`http://localhost:8000/api/v1/products/${searchTerm.trim()}/`)
              .then(res => {
                return [res.data];
              })
              .catch(err => {
                console.log(err);
              })

        }
      }


</script>