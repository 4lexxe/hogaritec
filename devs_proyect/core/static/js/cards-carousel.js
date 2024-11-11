var swiper = new Swiper(".mySwiper", {
	slidesPerView: 1,
	loop: true,
	spaceBetween: 10,
	pagination: {
		el: ".swiper-pagination",
	},
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
			spaceBetween: 20,
		},
		950: {
			slidesPerView: 3,
			spaceBetween: 50,
		},
		1120: {
			slidesPerView: 4,
			spaceBetween: 50,
		},
	},
});
