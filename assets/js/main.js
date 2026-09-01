(() => {
  const fallbackPhoto = "assets/img/foto-perfil.png";

  document.querySelectorAll("[data-profile-photo]").forEach((image) => {
    const restorePlaceholder = () => {
      if (!image.src.endsWith("foto-perfil.png")) image.src = fallbackPhoto;
    };
    image.addEventListener("error", restorePlaceholder);
    if (image.complete && image.naturalWidth === 0) restorePlaceholder();
  });

  // Manejador de clics en fotos de perfil para abrir el Perfil Profesional
  document.querySelectorAll("[data-profile-photo-trigger], .brand-photo-link").forEach((trigger) => {
    trigger.addEventListener("click", (e) => {
      // Si la página actual no es perfil-profesional.html y no es un link específico
      if (!window.location.pathname.endsWith("perfil-profesional.html") && trigger.tagName !== "A") {
        window.location.href = "perfil-profesional.html";
      }
    });
  });

  document.querySelectorAll("[data-current-year]").forEach((element) => {
    element.textContent = new Date().getFullYear();
  });

  const menuButton = document.querySelector("[data-menu-button]");
  const menu = document.querySelector("[data-menu]");
  if (menuButton && menu) {
    menuButton.addEventListener("click", () => {
      const isOpen = menu.classList.toggle("is-open");
      menuButton.setAttribute("aria-expanded", String(isOpen));
      menuButton.setAttribute("aria-label", isOpen ? "Cerrar menú" : "Abrir menú");
    });

    menu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        menu.classList.remove("is-open");
        menuButton.setAttribute("aria-expanded", "false");
        menuButton.setAttribute("aria-label", "Abrir menú");
      });
    });
  }

  document.querySelectorAll("[data-whatsapp-widget]").forEach((widget) => {
    const options = widget.querySelector(".whatsapp-options");
    const toggle = widget.querySelector("[data-whatsapp-toggle]");
    if (!options || !toggle) return;

    const closeWidget = () => {
      options.hidden = true;
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Abrir opciones de WhatsApp");
    };

    toggle.addEventListener("click", (e) => {
      e.stopPropagation();
      const isOpen = options.hidden;
      options.hidden = !isOpen;
      toggle.setAttribute("aria-expanded", String(isOpen));
      toggle.setAttribute("aria-label", isOpen ? "Cerrar opciones de WhatsApp" : "Abrir opciones de WhatsApp");
    });

    document.addEventListener("click", (event) => {
      if (!widget.contains(event.target)) closeWidget();
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") closeWidget();
    });
  });

  const revealElements = document.querySelectorAll(".reveal");

  // Carrusel automático del hero (sin flechas)
  const reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelectorAll("[data-carousel]").forEach((carousel) => {
    const slides = Array.from(carousel.querySelectorAll(".carousel-slide"));
    const dotsContainer = carousel.querySelector("[data-carousel-dots]");
    if (slides.length === 0) return;

    let current = 0;
    let timer = null;
    const INTERVAL_MS = 4000;

    const buildDots = () => {
      if (!dotsContainer) return;
      slides.forEach((_, i) => {
        const dot = document.createElement("span");
        if (i === 0) dot.classList.add("is-active");
        dotsContainer.appendChild(dot);
      });
    };

    const show = (index) => {
      slides.forEach((slide, i) => slide.classList.toggle("is-active", i === index));
      if (dotsContainer) {
        dotsContainer.querySelectorAll("span").forEach((dot, i) => dot.classList.toggle("is-active", i === index));
      }
      current = index;
    };

    const next = () => show((current + 1) % slides.length);

    const start = () => {
      if (reduceMotion) return;
      stop();
      timer = setInterval(next, INTERVAL_MS);
    };
    const stop = () => {
      if (timer) clearInterval(timer);
      timer = null;
    };

    buildDots();
    show(0);
    start();

    carousel.addEventListener("mouseenter", stop);
    carousel.addEventListener("mouseleave", start);
    carousel.addEventListener("focusin", (e) => {
      if (carousel.contains(e.target)) stop();
    });
    carousel.addEventListener("focusout", () => start());
  });

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealElements.forEach((element) => observer.observe(element));
  } else {
    revealElements.forEach((element) => element.classList.add("is-visible"));
  }
})();

