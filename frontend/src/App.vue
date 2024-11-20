<template xmlns="http://www.w3.org/1999/html">
  <div v-if="isLoading" class="loading-overlay">
    <div class="loader"></div>
  </div>
  <div class="container_up">
    <div class="logo-container">
      <img :src="logo" alt="Логотип Matrix" class="logo"/>
      <div class="name-container">Matrix</div>

      <div class="button-container-up">

        <div class="filter-dropdown">
          <button type="button" class="button-filter">Фильтрация</button>
          <div v-if="isOpenFilter" class="dropdown-menu-filter">
            <div class="dropdown-item-filter"></div>
          </div>
        </div>
        <!-- Dropdown -->
        <div class="dropdown">
          <button class="my-button-dropdown" @click="toggleDropdown">Выберите магазин</button>
          <div v-if="isOpen" class="dropdown-menu">
            <div class="dropdown-item" v-for="(name, id) in storeNames" :key="id">
              <input type="checkbox"
                     :value="name"
                     :id="id"
                     v-model="selectShop"/>
              <label>{{ name }}</label>
            </div>
          </div>
        </div>

        <button type="button" class="my-button">Все комментарии</button>
        <button type="button" class="my-button">Отзывы и предложения</button>
      </div>

      <div class="wrap">
        <div class="search">
          <input type="text"
                 class="searchTerm"
                 v-model="searchTerm"
                 placeholder="Поиск по артикулу" />
          <button type="submit" class="searchButton" @click="handleFetchData">
            <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
          </button>
        </div>
      </div>
    </div>

    <div class="main-window" ref="scrollContainer" @scroll="handleScroll">
      <table class="table" id="Table">
        <thead>
        <tr>
          <th colspan="1"></th>
          <th colspan="1"></th>
          <th colspan="7"></th>
          <th :colspan="namesWarehouses.length">Склады</th>
          <th v-for="(shop, index) in filteredShops" :key="index" :colspan="fieldShops.length">
            {{ shop }}
            <br/>
            <span class="small-data">{{ getStoreInfo(shop) }}</span>
          </th>
        </tr>
        <tr>
          <th @click="sortBy('article')">Артикул <span v-if="currentSort === 'article'">{{ currentSortDir === 'asc' ? '▲' : '▼' }}</span></th>
          <th @click="sortBy('name')">Номенклатура <span v-if="currentSort ==='name'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span></th>
          <th @click="sortBy('model')">Модель <span v-if="currentSort ==='model'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span></th>
          <th @click="sortBy('manufacturer')">Производитель <span v-if="currentSort ==='manufacturer'">{{currentSortDir ==='asc'? '▼' : '▲'}}</span></th>
          <th @click="sortBy('square')">Площадь номенклатуры <span v-if="currentSort ==='square'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span></th>
          <th @click="sortBy('segment')">Сегмент <span v-if="currentSort ==='segment'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span></th>
          <th @click="sortBy('matrix')">Матрица <span v-if="currentSort ==='matrix'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span></th>
          <th @click="sortBy('category')">Категория <span v-if="currentSort ==='category'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span></th>
          <th @click="sortBy('room_class')">Комната <span v-if="currentSort ==='room_class'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span></th>
          <th v-for="warehouse in namesWarehouses" :key="warehouse" @click="sortByWarehouses(warehouse)">
            {{ warehouse}}
            <span v-if="currentSort === warehouse ">
              {{currentSortDir ==='asc'? '▲' : '▼'}}
            </span>
          </th>
          <template v-for="shop in filteredShops" :key="shop">
            <th v-for="field in fieldShops" :key="field" @click="sortByShopField(shop, field)">
              {{ field + " 🔄" }}
            </th>
          </template>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(item, index) in sortedData" :key="item.article">
          <td>{{ item.article }}</td>
          <td>{{ item.name }}</td>
          <td>{{ item.model || "-" }}</td>
          <td>{{ item.manufacturer || "-" }}</td>
          <td>{{ item.square || "-" }}</td>
          <td>{{ item.segment || "-" }}</td>
          <td>{{ item.matrix || "-" }}</td>
          <td>{{ item.category || "-" }}</td>
          <td>{{ item.room_class || "-" }}</td>
          <template v-for="nameWARE in namesWarehouses">
            <td v-if="item.warehouses && item.warehouses[nameWARE]">
              {{ item.warehouses[nameWARE].stock }}
            </td>
            <td v-else>0</td>
          </template>
          <template v-for="shop in filteredShops" :key="shop">
            <td  v-for="field in fieldShops" :key="field">
              <template v-if="field === 'Комментарии'">
                <CommentButon :shop-name="shop" :good-article="item.article" :good-name="item.name"/>
                <span class="comment-label"> кол-во комментариев: {{ item.comments_count }}</span>
              </template>
              <template v-else-if="field === 'План'">
                  <span @click="enableEdit(index, shop, item.stores[shop]?.plan_exibition || '')" style="display: block; width: 100%;">
                    <input class="cell_input"
                        v-if="editIndex === index && editShop === shop"
                        type="text"
                        v-model="editedValue"
                        @blur="saveChanges(index, shop)"
                        @keyup.enter="saveChanges(index, shop)"
                    />
                    <span v-else>{{ item.stores[shop]?.plan_exibition || '-' }}</span>
                  </span>
              </template>
              <template v-else>
                {{ getShopField(item.stores[shop], field, item) }}
              </template>
            </td>
          </template>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import CommentButon from "@/CommentButon.vue";
import logo from './logofull.png';
import {ref} from "vue";
import {fetchData} from "./FetchData.vue";

export default {
  components: {CommentButon},
  data() {
    return {
      isOpenFilter: false,
      isOpen: false,
      isLoading: true,
      logo,
      fieldShops: ["План", "Факт", "Площадь", "Комментарии"],
      searchTerm: '',
      selectShop: [],
      product2: [],
      storeNames: [],
      stores: [],
      warehouses: [],
      namesWarehouses: [],
      editIndex: null,
      editShop: null,
      editedValue: '',
      currentPageNew: 2, // Текущая страница данных
      isLoadingData: false, // Индикатор загрузки
      hasMoreData: true,
      currentSort: ' ',
      currentSortDir: ref('asc')

    };
  },
  computed: {
    filteredShops() {
      return this.selectShop.length === 0 ? this.storeNames : this.selectShop;
    },
    sortedData() {
      if (!this.currentSort) return this.product2;
      return [...this.product2].sort((a, b) => {
        const modifier = this.currentSortDir === 'asc' ? 1 : -1;
        if (this.currentSort === 'category') {
          const valA = parseInt(a.category?.replace(/\D/g, '') || '-', 10);
          const valB = parseInt(b.category?.replace(/\D/g, '') || '-', 10);
          return (valA - valB) * modifier;
        }
        // Сортировка для столбцов магазинов
        if (this.currentSort.startsWith('shop:')) {
          const [, shop, field] = this.currentSort.split(':'); // "shop:shopName:field"
          const valA = this.getShopField(a.stores?.[shop], field, a) || '-';
          const valB = this.getShopField(b.stores?.[shop], field, b) || '-';
          // Если значения числа, сортируем численно
          if (!isNaN(parseFloat(valA)) && !isNaN(parseFloat(valB))) {
            return (parseFloat(valA) - parseFloat(valB)) * modifier;
          }
          // Сортировка строк
          return String(valA).localeCompare(String(valB)) * modifier;
        }
        // Сортировка для складов
        if (this.currentSort.startsWith('warehouse:')) {
          const warehouseName = this.currentSort.split(':')[1]; // "warehouse:warehouseName"
          const valA = parseFloat(a.warehouses?.[warehouseName]?.stock || 0);
          const valB = parseFloat(b.warehouses?.[warehouseName]?.stock || 0);
          return (valA - valB) * modifier;
        }
        // Общая логика для остальных полей
        const valA = a[this.currentSort] || '';
        const valB = b[this.currentSort] || '';
        // Если значения числа, сортируем численно
        if (!isNaN(parseFloat(valA)) && !isNaN(parseFloat(valB))) {
          return (parseFloat(valA) - parseFloat(valB)) * modifier;
        }
        // Иначе строковая сортировка
        return String(valA).localeCompare(String(valB)) * modifier;
      });
    },
  },
  created() {
    this.handleFetchData(this.searchTerm);
    this.isLoading = true;  // Включаем заглушку
    Promise.all([this.fetchStores(), this.fetchWarehouses()])
        .finally(() => {
          console.log('Все данные загружены');  // Отладочное сообщение
          this.isLoading = false;  // Отключаем заглушку
        });
  },
  beforeDestroy() {
    document.removeEventListener('click', this.closeDropdown);
  },

  methods: {
    sortByWarehouses(name) {
      this.sortBy(`warehouse:${name}`);
    },
    sortByShopField(shop, field) {
      // Формируем идентификатор сортировки в формате "shop:field"
      this.sortBy(`shop:${shop}:${field}`);
    },
    sortBy(field) {
      if (this.currentSort === field) {
        // Меняем направление сортировки
        this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
      } else {
        // Устанавливаем новое поле и направление по умолчанию
        this.currentSort = field;
        this.currentSortDir = 'asc';
      }
    },
    //Товары
    async handleFetchData() {
      try {
        const data = await fetchData(this.searchTerm); // Ожидаем завершения fetchData
        this.product2 = data || []; // Записываем результат в product2
      } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
      }
    },
    fetchStores() {
      return axios.get('http://localhost:8000/api/v1/stores/')
          .then(res => {
            this.stores = res.data.results;
            this.storeNames = this.stores.map(item => item.name);
            this.storeNames = this.storeNames.sort()
          })
          .catch(err => console.error("Stores fetch error:", err));
    },
    fetchWarehouses() {
      return axios.get("http://localhost:8000/api/v1/warehouses/")
          .then(res => {
            this.warehouses = res.data.results;
            this.namesWarehouses = this.warehouses.map(item => item.name);
            console.log("склады", this.warehouses);
          })
          .catch(err => console.error("Warehouses fetch error:", err));
    },
    getShopField(storeData, field, product) {
      if (!storeData) return '-';
      switch (field) {
        case "План":
          return storeData.plan_exibition || '-';
        case "Факт":
          return storeData.fact_exhibition || '-';
        case "Комментарии":
          return storeData.comments_count || '-';
        case "Площадь":
          return product.square ? (product.square * 2) : '-';
        default:
          return '-';
      }
    },
    toggleDropdown() {
      this.isOpen = !this.isOpen;
      if (this.isOpen) {
        document.addEventListener('click', this.closeDropdown);
      } else {
        document.removeEventListener('click', this.closeDropdown);
      }
    },
    closeDropdown(event) {
      if (!event.target.closest('.dropdown')) {
        this.isOpen = false;
        document.removeEventListener('click', this.closeDropdown);
      }
    },
    getStoreInfo(shop) {
      const store = this.stores.find(s => s.name === shop);
      return store ? store.info : '-';
    },
    enableEdit(index, shop, currentValue) {
      this.editIndex = index;
      this.editShop = shop;
      this.editedValue = currentValue;
    },
    saveChanges(index, shop) {
      let updatedProducts = [...this.product2];
      const item = updatedProducts[index];
      if (!item.stores[shop]) {
        item.stores[shop] = { plan_exibition: this.editedValue };
      } else {
        item.stores[shop].plan_exibition = this.editedValue;
      }
      this.product2 = updatedProducts;
      this.resetEditState();
    },
    resetEditState() {
      this.editIndex = null;
      this.editShop = null;
      this.editedValue = '';
    },

    loadData() {
      console.log("загрузка товаров")

      axios.get(`http://localhost:8000/api/v1/products/?page=${this.currentPageNew}`)
          .then(res => {
            const newProducts = res.data.results;
            console.log('new_prod',newProducts);

            if (newProducts.length === 0) {
              this.hasMoreData = false; // Если больше данных нет, отключаем дальнейшую загрузку
            } else {
              this.product2 = [...new Set(this.product2), ...newProducts];
              console.log("новые данные добавленны")
              this.currentPageNew +=1 ;
              console.log(this.currentPageNew);
            }
          })
          .catch(err => console.error("Ошибка загрузки данных:", err))
          .finally(() => {
          });
    },
       handleScroll() {
        const scrollContainer = this.$refs.scrollContainer;
        const scrollBottom = scrollContainer.scrollHeight - scrollContainer.scrollTop - scrollContainer.clientHeight;

        if (this.product2.length === 1) {
          // Ничего не делаем
        } else if (scrollBottom === 1) {// Если до конца контейнера менее 100px
          this.loadData();
        }

      }
  }
};
</script>

