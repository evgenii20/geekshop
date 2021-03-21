window.onload = function () {
    /*
    // можем получить DOM-объект меню через JS
    var menu = document.getElementsByClassName('menu')[0];
    menu.addEventListener('click', function (){
       console.log(event);
       event.preventDefault();
    });

    // можем получить DOM-объект меню через jQuery
    $('.menu').on('click', 'a', function (){
        console.log('event', event);
        console.log('this', this);
        console.log('event.target', event.target);
        event.preventDefault();
    });

    // получаем атрибут href
    $('.menu').on('click', 'a', function (){
        var target_href = event.target.href;
        if (target_href) {
            console.log('нужно перейти', target_href);
        }
        event.preventDefault();
    });
    */

    // $('.basket_list input[type="number"]').click(function () { - тоже применяется, но для динамики|.on
    // добавляем ajax-обработчик для обновления количества товара
    /* '.basket_list' - общий не меняемый элемент(на basket.html), весим событие ".on" на событие "click" по
    элементу с типом "number" и это событие обрабатываем в функции
    * */
    $('.basket_list').on('click', 'input[type="number"]', function () {
        // old
        let target_href = event.target;
        // jQuery
        // let target_href = $(this);

        if (target_href) {
            $.ajax({
                url: "/basket/edit/" + target_href.name + "/" + target_href.value + "/",

                success: function (data) {
                    $('.basket_list').html(data.result);
                    console.log('ajax done');
            },
        });
        }

        event.preventDefault();
    });
}