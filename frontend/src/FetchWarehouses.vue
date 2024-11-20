<script>
import axios from "axios";

export const fetchWarehouses =(Funwarehouses, FunnamesWarehouses) => axios.get("http://localhost:8000/api/v1/warehouses/")
      .then(res => {
        const warehouses = res.data.results;
        const namesWarehouses = warehouses.map(item => item.name);
        Funwarehouses(warehouses)
        FunnamesWarehouses(namesWarehouses)
      })
      .catch(err => console.error("Warehouses fetch error:", err));
</script>