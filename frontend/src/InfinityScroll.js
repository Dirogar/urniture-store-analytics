import axios from "axios";

/**
 * Загрузка данных с API
 * @param {number} currentPage - Текущая страница
 * @returns {Promise<Object>} - Обновлённые данные и флаги состояния
 */
export async function loadData(currentPage) {
    console.log("Загрузка товаров...");
    console.log("Текущая страница:", currentPage);

    try {
        console.log("ЗАПРОС ОТПРАВЛЕН");

        // Делаем запрос на сервер
        const response = await axios.get(`http://localhost:8000/api/v1/products/?page=${currentPage}`);
        const newProducts = response.data.results;

        console.log("Полученные данные:", newProducts);

        // Проверяем, есть ли новые данные
        if (newProducts.length === 0) {
            return {
                hasMoreData: false, // Данные закончились
                currentPage, // Текущая страница не меняется
            };
        } else {
            console.log("Удаление дубликатов");
            return {
                products: newProducts, // Возвращаем новые данные
                hasMoreData: true, // Ещё есть данные
                currentPage: currentPage + 1, // Увеличиваем номер страницы
            };
        }
    } catch (err) {
        console.error("Ошибка загрузки данных:", err);
        throw err; // Пробрасываем ошибку для обработки в вызывающем коде
    }
}
