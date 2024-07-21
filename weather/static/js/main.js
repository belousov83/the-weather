$("#select_city").suggestions({
    token: document.getElementById('select_city').getAttribute('data-api-key'),
    type: "ADDRESS",
    /* Вызывается, когда пользователь выбирает одну из подсказок */
    onSelect: function(suggestion) {
        console.log(suggestion);
    }
});