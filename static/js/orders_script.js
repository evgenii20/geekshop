window.onload = function () {
    //  количество текущее, цена, форма из форм сета, разница по кол-ву было-стало, кол-во у тек. формы, разрыв по деньгам
    var _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    var quantity_arr = [];
    var price_arr = [];

    var TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    // Можно вытаскивать по id
    // var TOTAL_FORMS = parseInt($('#id-TOTAL_FORMS').val());
    var order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    // в JS необходимо заменять "," на точку "."
    var order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for (var i = 0; i < TOTAL_FORMS; i++) {
        // "input[name="orderitems-" - можно сказать, подселектор. JS приведёт тип "i" к строке, слева и справа то же строки
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            // если строка пустая, то выводим "0" в столбце "цена"
            price_arr[i] = 0;
        }
    }
    // console.log(quantity_arr);
    // console.log(price_arr);
    if (!order_total_quantity) {
        for (var i = 0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
        }

        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }

    // Будем обрабатывать события изменения количества или удаления товаров в заказе при помощи
    // jQuery метода «.on()»:
    $('.order_form').on('click', 'input[type="number"]', function () {
        // 1-й вариант
        // this.target
        // 2-й:
        var target = event.target;
        // "orderitem_num" - номер строки с формой и заменой ".replace" на пусто ''
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        // проверяем выбранную строку
        if (price_arr[orderitem_num]) {
            // если строка не пустая, обновляем кол-во
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            // обновляем кол-во
            quantity_arr[orderitem_num] = orderitem_quantity;
            // функция обновления кол-ва и цены
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
        }

    });
    $('.order_form').on('click', 'input[type="checkbox"]', function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            // если строка отмечена, удаляем "-quantity_arr[orderitem_num]"
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            // если строка не отмечена, оставляем текущее значение
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });
    
    // function orderSummaryUpdate(orderitem_price, delta_quantity) {
    function orderSummaryUpdate(orderitem_num, delta_quantity) {
        delta_cost = orderitem_num * delta_quantity;

        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    function deleteOrderItem(row){
        var target_name = row[0].querySelector('input[type=number]').name;
        // orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        // однозначное удаление строки
        delta_quantity = -quantity_arr[orderitem_num];
        // обновление записи
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    }

    $('.order_form select').change(function () {
        var target = event.target;
        console.log(target);
    });

    // вызов селектора с формсетами. JQuery FormSet
    $('.formset_row').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });



}
