var swiper1 = new Swiper(".swiperCarousel", {
    centeredSlides: true,
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});


var swiper2 = new Swiper(".swiperCarouselCards", {
	slidesPerView: 1,
	loop: true,
	spaceBetween: 10,
	navigation: {
		nextEl: ".swiper-button-next",
		prevEl: ".swiper-button-prev",
	},
	keyboard: {
		enabled: true,
	},

	breakpoints: {
		640: {
			slidesPerView: 2,
		},
		950: {
			slidesPerView: 3,
		},
		1200: {
			slidesPerView: 4,
		},
	},
});