const menuOpenButton = document.querySelector("#menu-open-button");
const menuCloseButton = document.querySelector("#menu-close-button");

menuOpenButton.addEventListener("click", () => {

    document.body.classList.toggle("show-mobile-menu");
})
//closes menu when the close button is clicked

menuCloseButton.addEventListener("click", () => menuOpenButton.click());


//Initializing Swiper 
const swiper = new Swiper('.slider-wrapper', {
    loop: true,
    grabCursor: true,
    spaceBetween: 25,

  
    // If we need pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
      dynamicBullets: true,
    },
  
    // Navigation arrows
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },

    breakpoints: {
        0: {
            sliderPerview: 1
        },
        
        768: {
            sliderPerview: 2
        },
        1024: {
            sliderPerview: 3
        }
    }
  });