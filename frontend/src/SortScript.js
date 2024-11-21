/**
 * Функция для Заполения поей для магазина
 * @param {Object} storeData - Данные магазина
 * @param {string} field - Поле для сортировки
 * @param {Object} product - Продукт
 * @returns {string|number} Значение для сортировки
 */
export function getShopField(storeData, field, product) {
    if (!storeData) return '-';
    switch (field) {
        case "План":
            return storeData.plan_exibition || '-';
        case "Факт":
            return storeData.fact_exhibition || '-';
        case "Комментарии":
            return storeData.comments_count || '-';
        case "Площадь":
            return product.square ? product.square * 2 : '-';
        default:
            return '-';
    }
}

/**
 * Сортировка данных
 * @param {Array} data - Данные для сортировки
 * @param {string} currentSort - Поле для сортировки
 * @param {string} currentSortDir - Направление сортировки ('asc' | 'desc')
 * @returns {Array} - Отсортированные данные
 */
export function sortData(data, currentSort, currentSortDir) {
    if (!currentSort) return data;

    const modifier = currentSortDir === 'asc' ? 1 : -1;

    return [...data].sort((a, b) => {
        if (currentSort === 'category') {
            const valA = parseInt(a.category?.replace(/\D/g, '') || '0', 10);
            const valB = parseInt(b.category?.replace(/\D/g, '') || '0', 10);
            return (valA - valB) * modifier;
        }

        // Сортировка для столбцов магазинов
        if (currentSort.startsWith('shop:')) {
            const [, shop, field] = currentSort.split(':'); // "shop:shopName:field"
            const valA = getShopField(a.stores?.[shop], field, a) || '-';
            const valB = getShopField(b.stores?.[shop], field, b) || '-';

            if (!isNaN(parseFloat(valA)) && !isNaN(parseFloat(valB))) {
                return (parseFloat(valA) - parseFloat(valB)) * modifier;
            }
            return String(valA).localeCompare(String(valB)) * modifier;
        }

        // Сортировка для складов
        if (currentSort.startsWith('warehouse:')) {
            const warehouseName = currentSort.split(':')[1];
            const valA = parseFloat(a.warehouses?.[warehouseName]?.stock || 0);
            const valB = parseFloat(b.warehouses?.[warehouseName]?.stock || 0);
            return (valA - valB) * modifier;
        }

        // Общая логика для остальных полей
        const valA = a[currentSort] || '';
        const valB = b[currentSort] || '';

        if (!isNaN(parseFloat(valA)) && !isNaN(parseFloat(valB))) {
            return (parseFloat(valA) - parseFloat(valB)) * modifier;
        }
        return String(valA).localeCompare(String(valB)) * modifier;
    });
}
