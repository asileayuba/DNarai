// Remove preload class after short delay (HTML5 UP pattern)
window.addEventListener("load", function () {
  window.setTimeout(function () {
    document.body.classList.remove("is-preload");
    console.log("is-preload removed on load");
  }, 100);
});

// Fallback removal if something blocks the load event
setTimeout(function () {
  if (document.body.classList.contains("is-preload")) {
    document.body.classList.remove("is-preload");
    console.warn("is-preload removed by fallback");
  }
}, 2000);

document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menuToggle");
  const closeBtn = document.querySelector("#menu .close");
  const overlay = document.querySelector("#menu-overlay");

  // Open menu
  toggle?.addEventListener("click", (e) => {
    e.preventDefault();
    document.body.classList.add("is-menu-visible");
  });

  // Close when clicking close button
  closeBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    document.body.classList.remove("is-menu-visible");
  });

  // Close when clicking overlay
  overlay?.addEventListener("click", () => {
    document.body.classList.remove("is-menu-visible");
  });

  // Initialize scrolly if jQuery + plugin exist
  if (window.jQuery && jQuery.fn && typeof jQuery.fn.scrolly === "function") {
    jQuery(function ($) {
      $(".scrolly").scrolly({
        offset: function () {
          const nav = document.querySelector("#navbar"); // adjust if needed
          return nav ? nav.offsetHeight : 0;
        },
      });
    });
    console.log("scrolly initialized");
  } else {
    console.warn(
      "scrolly plugin not found — check if jquery.scrolly.min.js is loaded after jQuery"
    );
  }
});

// Initialize Swiper
document.addEventListener("DOMContentLoaded", function () {
  const swiper = new Swiper(".testimonial-slider", {
    slidesPerView: 1,
    spaceBetween: 30,
    loop: true,
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
    breakpoints: {
      640: { slidesPerView: 1, spaceBetween: 20 },
      768: { slidesPerView: 2, spaceBetween: 30 },
      1024: { slidesPerView: 3, spaceBetween: 40 },
    },
  });
});

// AJAX Contact Form
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contact-form");
  const messageContainer = document.getElementById("form-message-container");

  if (!form || !messageContainer) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
        },
        body: formData,
      });

      if (!response.ok) throw new Error("Network error");

      const html = await response.text();
      messageContainer.innerHTML = html;

      // Reset form if success message present
      if (messageContainer.querySelector(".form-message.success")) {
        form.reset();
      }

      // Clear messages after 5 seconds
      setTimeout(() => {
        messageContainer.innerHTML = "";
      }, 5000);
    } catch (error) {
      messageContainer.innerHTML =
        '<div class="form-message error">An error occurred. Please try again.</div>';

      // Clear error message after 5 seconds
      setTimeout(() => {
        messageContainer.innerHTML = "";
      }, 5000);
    }
  });
});
