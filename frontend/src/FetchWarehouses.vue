<script>
import axios from "axios";

export const fetchWarehouses = () => axios.get("http://localhost:8000/api/v1/warehouses/")
    .then(res => {
      const warehouses = res.data.results;
      const namesWarehouses = warehouses.map(item => item.name);
      console.log(namesWarehouses);
      console.log(warehouses);
      return { warehouses, namesWarehouses }; // Возвращаем данные
    })
    .catch(err => {
      console.error("Warehouses fetch error:", err);
      throw err;
    });

</script>