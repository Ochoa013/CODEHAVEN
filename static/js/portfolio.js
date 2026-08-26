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
    if (quoteForm && $.fn.validate) {
        $.validator.addMethod("professionalName", function (value, element) {
            return this.optional(element) || /^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ.' -]+$/.test(value);
        }, "Escribe un nombre válido, sin números ni caracteres especiales.");

        $(quoteForm).validate({
            ignore: "[name='website'], [name='started_at']",
            errorElement: "small",
            errorClass: "jquery-field-error",
            validClass: "jquery-field-valid",
            focusInvalid: false,
            rules: {
                nombre: {
                    required: true,
                    minlength: 2,
                    maxlength: 80,
                    professionalName: true,
                    normalizer: function (value) { return $.trim(value); }
                },
                empresa: {
                    maxlength: 120,
                    normalizer: function (value) { return $.trim(value); }
                },
                telefono: {
                    required: true,
                    digits: true,
                    minlength: 7,
                    maxlength: 15,
                    normalizer: function (value) { return $.trim(value); }
                },
                email: {
                    required: true,
                    email: true,
                    maxlength: 254,
                    normalizer: function (value) { return $.trim(value); }
                },
                tipo_proyecto: { required: true },
                presupuesto: {
                    maxlength: 80,
                    normalizer: function (value) { return $.trim(value); }
                },
                descripcion: {
                    required: true,
                    minlength: 30,
                    maxlength: 4000,
                    normalizer: function (value) { return $.trim(value); }
                },
                preferencia_contacto: { required: true }
            },
            messages: {
                nombre: {
                    required: "Indica tu nombre completo para poder contactarte.",
                    minlength: "El nombre debe contener al menos 2 caracteres.",
                    maxlength: "El nombre no puede superar los 80 caracteres."
                },
                empresa: {
                    maxlength: "El nombre de la empresa no puede superar los 120 caracteres."
                },
                telefono: {
                    required: "Indica un número de teléfono o WhatsApp.",
                    digits: "Ingresa únicamente números, sin espacios ni símbolos.",
                    minlength: "Ingresa al menos 7 números.",
                    maxlength: "Ingresa un máximo de 15 números."
                },
                email: {
                    required: "Indica un correo electrónico para responder tu solicitud.",
                    email: "Escribe un correo electrónico válido, por ejemplo nombre@empresa.com.",
                    maxlength: "El correo electrónico es demasiado largo."
                },
                tipo_proyecto: {
                    required: "Selecciona el servicio que mejor corresponde a tu proyecto."
                },
                presupuesto: {
                    maxlength: "El presupuesto no puede superar los 80 caracteres."
                },
                descripcion: {
                    required: "Describe brevemente el proyecto o problema que deseas resolver.",
                    minlength: "Incluye un poco más de información; escribe al menos 30 caracteres.",
                    maxlength: "La descripción no puede superar los 4.000 caracteres."
                },
                preferencia_contacto: {
                    required: "Selecciona cómo prefieres que te contactemos."
                }
            },
            errorPlacement: function (error, element) {
                if (element.attr("name") === "preferencia_contacto") {
                    error.insertAfter(element.closest(".preference-options"));
                } else {
                    error.insertAfter(element);
                }
            },
            highlight: function (element) {
                var $field = $(element);
                $field.addClass("jquery-input-invalid").removeClass("jquery-input-valid");
                $field.closest(".form-group").addClass("field-has-errors").removeClass("field-is-valid");
            },
            unhighlight: function (element) {
                var $field = $(element);
                $field.removeClass("jquery-input-invalid").addClass("jquery-input-valid");
                $field.closest(".form-group").removeClass("field-has-errors").addClass("field-is-valid");
            },
            invalidHandler: function (event, validator) {
                if (validator.errorList.length) {
                    var firstInvalid = validator.errorList[0].element;
                    firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
                    window.setTimeout(function () { firstInvalid.focus(); }, 350);
                }
            },
            submitHandler: function (form) {
                var submitButton = form.querySelector(".quote-submit");
                submitButton.disabled = true;
                submitButton.setAttribute("aria-busy", "true");
                submitButton.querySelector("span").textContent = "Enviando solicitud...";
                form.submit();
            }
        });
    }

    var quoteFeedback = document.getElementById("cotizacion-feedback");
    if (quoteFeedback) {
        var feedbackStatus = quoteFeedback.getAttribute("data-status");
        var feedbackTitle = quoteFeedback.querySelector("strong").textContent.trim();
        var feedbackText = quoteFeedback.querySelector("p").textContent.trim();

        if (window.Swal) {
            window.Swal.fire({
                icon: feedbackStatus === "success" ? "success" : "error",
                title: feedbackTitle,
                text: feedbackText,
                confirmButtonText: "Aceptar",
                buttonsStyling: false,
                allowOutsideClick: false,
                customClass: {
                    popup: "codehaven-swal-popup",
                    title: "codehaven-swal-title",
                    htmlContainer: "codehaven-swal-text",
                    confirmButton: "codehaven-swal-confirm"
                }
            }).then(function () {
                quoteFeedback.remove();
            });
        } else {
            quoteFeedback.hidden = false;
            quoteFeedback.scrollIntoView({ behavior: "smooth", block: "center" });
        }
    }
})(jQuery);
