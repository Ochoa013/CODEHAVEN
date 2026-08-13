(function ($) {
    "use strict";

    var $menuButton = $(".nav-switch");
    var $menu = $(".main-menu");

    $menuButton.on("click", function () {
        var isOpen = $menuButton.attr("aria-expanded") === "true";
        $menuButton.attr("aria-expanded", String(!isOpen));
        $menuButton.attr("aria-label", isOpen ? "Abrir menú" : "Cerrar menú");
    });

    $(".main-menu a").on("click", function () {
        if (window.innerWidth < 1200) {
            $menu.stop(true, true).slideUp(250);
            $menuButton.attr("aria-expanded", "false").attr("aria-label", "Abrir menú");
        }
    });

    $(window).on("resize", function () {
        if (window.innerWidth >= 1200) {
            $menu.removeAttr("style");
            $menuButton.attr("aria-expanded", "false");
        }
    });

    var $expertiseCarousel = $(".expertise-carousel");
    if ($expertiseCarousel.length && $.fn.owlCarousel) {
        $expertiseCarousel.owlCarousel({
            loop: true,
            margin: 16,
            nav: true,
            dots: false,
            autoplay: true,
            autoplayTimeout: 4200,
            autoplayHoverPause: true,
            smartSpeed: 650,
            navText: ["<span aria-hidden='true'>‹</span><span class='sr-only'>Anterior</span>", "<span aria-hidden='true'>›</span><span class='sr-only'>Siguiente</span>"],
            responsive: {
                0: { items: 1 },
                700: { items: 2 },
                1200: { items: 3 }
            }
        });

        $expertiseCarousel.find(".owl-prev, .owl-next")
            .attr("role", "button")
            .attr("tabindex", "0");
        $expertiseCarousel.find(".owl-prev").attr("aria-label", "Especialidad anterior");
        $expertiseCarousel.find(".owl-next").attr("aria-label", "Siguiente especialidad");
        $expertiseCarousel.find(".owl-prev, .owl-next").on("keydown", function (event) {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                $(this).trigger("click");
            }
        });
    }

    var revealItems = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        revealItems.forEach(function (item) {
            item.classList.add("reveal-pending");
        });

        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.remove("reveal-pending");
                        entry.target.classList.add("reveal-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12, rootMargin: "0px 0px -35px 0px" }
        );

        revealItems.forEach(function (item) {
            observer.observe(item);
        });
    }

    var invalidField = document.querySelector(".field-has-errors .form-control");
    if (invalidField) {
        window.setTimeout(function () {
            document.getElementById("contacto").scrollIntoView({ behavior: "smooth" });
            invalidField.focus({ preventScroll: true });
        }, 200);
    }

    var quoteForm = document.getElementById("quote-form");
    if (quoteForm) {
        quoteForm.addEventListener("submit", function () {
            quoteForm.classList.add("was-validated");
            if (quoteForm.checkValidity()) {
                var submitButton = quoteForm.querySelector(".quote-submit");
                submitButton.disabled = true;
                submitButton.querySelector("span").textContent = "Registrando solicitud...";
            }
        });
    }

    var successModal = document.querySelector("[data-success-modal]");
    if (successModal) {
        document.body.classList.add("modal-open");
        var closeModal = function () {
            successModal.classList.remove("is-visible");
            document.body.classList.remove("modal-open");
        };
        successModal.querySelectorAll("[data-close-success]").forEach(function (control) {
            control.addEventListener("click", closeModal);
        });
        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeModal();
            }
        });
        window.setTimeout(function () {
            successModal.querySelector(".success-modal-close").focus();
        }, 150);
    }
})(jQuery);
