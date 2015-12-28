/**
 * Created by openlex on 13.08.2015.
 */

(function () {
    var app = angular.module('pinst', []);
    app.controller('ClientsController', function ($scope) {
        $scope.clients = clients;
    });

    var clients= [
        {
            img:'img/clients/c11.jpg',
            name:'ochki_ru_',
            description:'Солнцезащитные очки мировых брендов',
            followers:'15k'
        },
        {
            img:'img/clients/c18.jpg',
            name:'easy_mom',
            description:'производитель товаров для мам и малышей',
            followers:'8,216'
        },
        {
            img:'img/clients/c12.jpg',
            name:'gulyanail',
            description:'Представитель LUXIO в Казахстане ',
            followers:'13k'
        },
        {
            img:'img/clients/c13.jpg',
            name:'showroomkhv',
            description:'Уютный шоу рум',
            followers:'10.3k'
        },
        {
            img:'img/clients/c14.jpg',
            name:'swarovski_baby_store',
            description:'Инкрустация кристаллами Swarovski',
            followers:'36k'
        },
        {
            img:'img/clients/c15.jpg',
            name:'luxbox.su',
            description:'Шкатлки для часов и украшений',
            followers:'13k'
        },
        {
            img:'img/clients/c1.jpg',
            name:'dostavkacvetovalmaty',
            description:'Доставка Цветов Алматы',
            followers:'40k',
        },
        {
            img:'img/clients/c2.jpg',
            name:'blissboutiquenew',
            description:'Итальянский бутик',
            followers:'10.9k'
        },
        {
            img:'img/clients/c3.jpg',
            name:'daniel.salon',
            description:'Маникюр, Педикюр, Эпиляция',
            followers:'31.8k'
        },
        {
            img:'img/clients/c4.jpg',
            name:'21shop.ru',
            description:'Итальянский бутик',
            followers:'20.7k '
        },
        {
            img:'img/clients/c5.jpg',
            name:'naildesiqn_tatianavasileva',
            description:'Курсы по маникюру и моделированию. ',
            followers:'11.2k'
        },
        {
            img:'img/clients/c6.jpg',
            name:'yulemelyanova',
            description:'Торты на заказ',
            followers:'24.5k'
        },
        {
            img:'img/clients/c7.jpg',
            name:'lady_kz3085',
            description:'Sunny Онлайн магазин Алматы',
            followers:'10.9k'
        },
        {
            img:'img/clients/c8.jpg',
            name:'aleksandra_shoppingvrimini',
            description:'Лучший шоппинг в Римини',
            followers:'12.4k'
        },
        {
            img:'img/clients/c9.jpg',
            name:'azbuka_krasoti',
            description:'Салон красоты, МАХАЧКАЛА',
            followers:'13.2k'
        },
        {
            img:'img/clients/c10.jpg',
            name:'_fashion_room_',
            description:'Итальянская одежда',
            followers:'20.8k'
        },

        {
            img:'img/clients/c16.jpg',
            name:'the_one_studio_',
            description:'Showroom-Atelier',
            followers:'11.6k'
        },
        {
            img:'img/clients/c17.jpg',
            name:'my.frenchbulldog',
            description:'Подарки ручной работы декупаж',
            followers:'8,488'
        },


    ];
})();