/*
 * ============================================================
 *  ЕДИНЫЙ КОНФИГ САЙТА AURORA (Сербия) — ПЛЕЙСХОЛДЕРЫ
 * ============================================================
 *  Все контактные и брендовые данные собраны здесь, чтобы
 *  заменить их в ОДНОМ месте, когда заказчик пришлёт реальные.
 *
 *  Значения-плейсхолдеры помечены префиксом __ и словом TODO.
 *  Поиск по проекту "__TODO" покажет все места, ждущие данных.
 *
 *  Скрипт при загрузке подставляет значения в элементы с
 *  атрибутом data-cfg="ключ" (текст) и data-cfg-href="ключ"
 *  (атрибут href). Так контакты не хардкодятся в HTML.
 * ============================================================
 */
(function () {
  "use strict";

  // --- Реальные данные заказчик пришлёт позже (заменить здесь) ---
  const CONFIG = {
    // Бренд — ПОДТВЕРЖДЁН заказчиком: просто "Aurora"
    brandName: "Aurora",

    // Домен сайта (для canonical/og)
    domain: "pretapaciranje.rs",

    // Телефон в сербском формате +381 (плейсхолдер)
    phoneDisplay: "+381 __ TODO",          // как показывать на странице
    phoneHref: "381000000000",             // для tel: (только цифры, без +)

    // Мессенджеры (плейсхолдеры)
    whatsapp: "https://wa.me/381000000000",
    telegram: "https://t.me/__TODO",
    viber: "viber://chat?number=%2B381000000000",

    // Почта (реальный адрес)
    email: "info.pretapaciranje@gmail.com",

    // Endpoint формы Formspree
    formEndpoint: "https://formspree.io/f/xvkpaode",

    // Google Analytics 4 (заменит Яндекс.Метрику)
    ga4Id: "G-__TODO",

    // Адреса и координаты по городам (для карт и JSON-LD)
    cities: {
      beograd: {
        nameRu: "Белград",
        nameSr: "Beograd",
        address: "__TODO адрес, Beograd, Srbija",
        lat: 44.786568,   // центр Белграда (плейсхолдер — уточнить)
        lng: 20.448922
      },
      noviSad: {
        nameRu: "Нови-Сад",
        nameSr: "Novi Sad",
        address: "__TODO адрес, Novi Sad, Srbija",
        lat: 45.267136,   // центр Нови-Сада (плейсхолдер — уточнить)
        lng: 19.833549
      }
    },

    country: "RS",
    currencyPrimary: "RSD",
    currencySecondary: "EUR"
  };

  // Делаем доступным в консоли/других скриптах при необходимости
  window.SITE_CONFIG = CONFIG;

  // --- Подстановка значений в DOM после загрузки ---
  function applyConfig() {
    // Текстовые подстановки: <span data-cfg="phoneDisplay"></span>
    document.querySelectorAll("[data-cfg]").forEach(function (el) {
      const key = el.getAttribute("data-cfg");
      if (key in CONFIG && typeof CONFIG[key] === "string") {
        el.textContent = CONFIG[key];
      }
    });
    // Подстановки в href: <a data-cfg-href="whatsapp"></a>
    document.querySelectorAll("[data-cfg-href]").forEach(function (el) {
      const key = el.getAttribute("data-cfg-href");
      let value = CONFIG[key];
      if (key === "phoneHref") value = "tel:+" + CONFIG.phoneHref;
      if (key === "email") value = "mailto:" + CONFIG.email;
      if (typeof value === "string") el.setAttribute("href", value);
    });
    // Подстановка action у форм: <form data-cfg-action="formEndpoint">
    document.querySelectorAll("[data-cfg-action]").forEach(function (el) {
      const key = el.getAttribute("data-cfg-action");
      if (key in CONFIG && typeof CONFIG[key] === "string") {
        el.setAttribute("action", CONFIG[key]);
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyConfig);
  } else {
    applyConfig();
  }
})();
