<template>
      <div v-if="isLoading" class="loading-overlay">
        <div class="loader"></div>
      </div>
      <div class="container_up">
        <div class="logo-container">
        <img :src="logo" alt="Логотип Matrix" class="logo"/><span class="name-container">Matrix</span>

        <div class="button-container-up">
          <div class="filter-dropdown">
            <button type="button" class="button-filter">
              <i class="pi pi-filter" style="margin-right: 5px;"></i>
            </button>
              <div v-if="isOpenFilter" class="dropdown-menu-filter">
                <div class="dropdown-item-filter"></div>
              </div>
          </div>

      <!-- Dropdown -->
        <div class="dropdown">
          <button class="my-button-dropdown" @click="toggleDropdown">Салон</button>
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
        <button type="button" class="my-button">ОиП</button>
        </div>
          </div>
        <div class="wrap">
          <div class="search">
            <input type="text"
              class="searchTerm"
              v-model="searchTerm"
              placeholder="Поиск по артикулу" />
          <button type="submit" class="searchButton" @click="handleFetchData(1)">
            <i class="pi pi-search" style="color:white;"></i>
          </button>
          </div>
        </div>
      </div>
      <div class="pagination">
        <!-- Кнопка "Назад" -->
        <button
            @click="handleFetchData(currentPage - 1)"
            :disabled="!prevURL || currentPage === 1"
        >
          Назад
        </button>

        <!-- Кнопки страниц -->
        <button
            v-for="pageNumber in page"
            :key="pageNumber"
            :class="{ active: pageNumber === currentPage }"
            @click="handleFetchData(pageNumber)"
        >
          {{ pageNumber }}
        </button>

        <!-- Кнопка "Вперед" -->
        <button
            @click="handleFetchData(currentPage + 1)"
            :disabled="!nextURL || currentPage === page"
        >
          Вперед
        </button>
      </div>



  <!-- Table -->
      <div class="main-window">
        <table class="table" id="Table">
          <thead>
            <tr>
              <th colspan="1"></th>
              <th colspan="1"></th>
              <th colspan="7"></th>
              <th :colspan="namesWarehouses.length">Склады</th>
              <th v-for="(shop, index) in filteredShops" :key="index" :colspan="fieldShops.length">{{ shop }}<br/><span class="small-data">{{ getStoreInfo(shop) }}</span></th>
            </tr>
            <tr>
              <th @click="sortBy('article')">Артикул <span class="sort-direction" v-if="currentSort === 'article'">{{ currentSortDir === 'asc' ? '▲' : '▼' }}</span><span class="point_navigation" v-else> ●</span></th>
              <th @click="sortBy('name')">Номенклатура <span class="sort-direction" v-if="currentSort ==='name'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span><span class="point_navigation" v-else> ●</span></th>
              <th @click="sortBy('model')">Модель <span class="sort-direction" v-if="currentSort ==='model'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span><span class="point_navigation" v-else> ●</span></th>
              <th @click="sortBy('manufacturer')">Производитель <span class="sort-direction" v-if="currentSort ==='manufacturer'">{{currentSortDir ==='asc'? '▼' : '▲'}}</span><span class="point_navigation" v-else> ●</span></th>
              <th @click="sortBy('square')">Площадь номенклатуры <span class="sort-direction" v-if="currentSort ==='square'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span><span class="point_navigation" v-else> ●</span></th>
              <th @click="sortBy('segment')">Сегмент<span class="sort-direction" v-if="currentSort === 'segment'">{{ currentSortDir === 'asc' ? '▲' : '▼' }}</span><span class="point_navigation" v-else> ●</span></th>
              <th @click="sortBy('matrix')">Матрица <span class="sort-direction" v-if="currentSort ==='matrix'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span><span class="point_navigation" v-else> ●</span></th>
              <th @click="sortBy('category')">Категория <span class="sort-direction" v-if="currentSort ==='category'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span><span class="point_navigation" v-else> ●</span></th>
              <th @click="sortBy('room_class')">Комната <span class="sort-direction" v-if="currentSort ==='room_class'">{{currentSortDir ==='asc'? '▲' : '▼'}}</span><span class="point_navigation" v-else> ●</span></th>
              <th v-for="warehouse in namesWarehouses" :key="warehouse" @click="sortByWarehouses(warehouse)">{{ warehouse }}<span class="sort-direction" v-if="currentSort === `warehouse:${warehouse}`">{{ currentSortDir === 'asc' ? '▲' : '▼' }}</span><span class="point_navigation" v-else> ●</span></th>

              <template v-for="shop in filteredShops" :key="shop">
                <th v-for="field in fieldShops" :key="field" @click="sortByShopField(shop, field)">{{ field }}<span class="sort-direction" v-if="currentSort === `shop:${shop}:${field}`">{{ currentSortDir === 'asc' ? '▲' : '▼' }}</span><span class="point_navigation" v-else> ●</span></th>
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
                <td v-if="item.warehouses && item.warehouses[nameWARE]">{{ item.warehouses[nameWARE].stock }}</td><td v-else>0</td>
              </template>

            <template v-for="shop in filteredShops" :key="shop">
              <td  v-for="field in fieldShops" :key="field">
                <template v-if="field === 'Комментарии'">
                  <CommentButon :shop-name="shop" :good-article="item.article" :good-name="item.name"/><span class="comment-label"> кол-во комментариев: {{ item.comments_count }}</span>
                </template>
                <template v-else-if="field === 'План'">
                  <span @click="enableEdit(index, shop, item.stores[shop]?.plan_exibition || '')" style="display: block; width: 100%;">
                    <input class="cell_input"
                      v-if="editIndex === index && editShop === shop"
                      type="text"
                      v-model="editedValue"
                      @blur="saveChanges(index, shop)"
                      @keyup.enter="saveChanges(index, shop)"/><span v-else>{{ item.stores[shop]?.plan_exibition || '-' }}</span>
                  </span>
                </template>
                <template v-else>{{ getShopField(item.stores[shop], field, item) }}</template>
              </td>
            </template>
            </tr>
          </tbody>
        </table>
      </div>
</template>


<script>
import "primeicons/primeicons.css";
import CommentButon from "@/CommentButon.vue";
import logo from './logo.png';
import {ref} from "vue";
import {fetchData} from "./FetchData.vue";
import {fetchStores} from "./FetchStores.vue";
import {fetchWarehouses} from "./FetchWarehouses.vue";
import { sortData} from './SortScript.js';
import {getShopField} from "./SortScript.js";

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
      isLoadingData: false, // Индикатор загрузки
      hasMoreData: true,
      currentSort: ' ',
      currentSortDir: ref('asc'),
      currentPage: 1, // Текущая страница
      totalItems: 0, // Общее количество товаров
      nextPageUrl: null, // URL для следующей страницы
      previousPageUrl: null, // URL для предыдущей страницы

    };
  },
  computed: {
    filteredShops() {
      return this.selectShop.length === 0 ? this.storeNames : this.selectShop;
    },
    sortedData() {
      // Используем функцию sortData
      return sortData(this.product2, this.currentSort, this.currentSortDir);
    },
  },

  created() {
    this.isLoading = true;
    Promise.all([ this.handleFetchData(1), this.handleFetchStores(),this.handleFetchWarehouses()])
        .finally(() => {
          console.log('Все данные загружены');  // Отладочное сообщение
          this.isLoading = false;  // Отключаем заглушку
        });
  },


  methods: {
    getShopField,
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

    //Название магазинов
    async handleFetchStores() {
        try {
          const { stores, storeNames } = await fetchStores();
          this.stores = stores;
          this.storeNames = storeNames;
        } catch (error) {
          console.error("Ошибка при загрузке магазинов:", error);
        }
      },
    //Товары
    async handleFetchData(page = 1) {
      try {
        this.isLoading = true;
        this.currentPage = page;
        const data = await fetchData(this.searchTerm, this.currentPage);
        this.product2 = data.products;
        this.totalItems = data.totalItems;
        this.nextURL = data.nextURL;
        this.prevURL = data.prevURL;
        this.page = Math.ceil(this.totalItems / 100);
        this.isLoading= false;
      } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
      }
    },
    //Склады
    async handleFetchWarehouses() {
      try {
        const {warehouses, namesWarehouses} = await fetchWarehouses();
        this.warehouses = warehouses;
        console.log("crkfls",this.warehouses);
        this.namesWarehouses = namesWarehouses;
      } catch (error) {
        console.log("Ошибка при загрузке данных:", error``)
      }
    },

    //Выподающий список для выбора магазина
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

    // Изменение занчения для поля "План"
    //TODO: Изменить,для отправки запроса
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

  }
};
</script>

