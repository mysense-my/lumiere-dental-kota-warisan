/* Lumiere Dental Kota Warisan — interactions */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- header state ---------- */
  var nav = document.getElementById("siteNav");
  var hero = document.getElementById("home");
  function onScroll() {
    var limit = hero ? hero.offsetHeight - 90 : 400;
    nav.classList.toggle("scrolled", window.scrollY > limit);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  var burger = document.getElementById("navBurger");
  burger.addEventListener("click", function () {
    var open = nav.classList.toggle("menu-open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) nav.classList.add("scrolled");
    else onScroll();
  });
  document.querySelectorAll(".nav-drawer a").forEach(function (a) {
    a.addEventListener("click", function () {
      nav.classList.remove("menu-open");
      burger.setAttribute("aria-expanded", "false");
      onScroll();
    });
  });

  /* ---------- appear on scroll ---------- */
  var appearEls = [].slice.call(document.querySelectorAll("[data-appear]"));
  if (reduced) {
    appearEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add("in");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    appearEls.forEach(function (el) { io.observe(el); });
  }

  /* ---------- count-up stats ---------- */
  function animateCount(el) {
    var to = parseFloat(el.getAttribute("data-count-to"));
    var dec = parseInt(el.getAttribute("data-dec") || "0", 10);
    var dur = 1800;
    var t0 = null;
    function frame(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = (to * eased).toFixed(dec);
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  var counters = [].slice.call(document.querySelectorAll("[data-count-to]"));
  if (reduced) {
    counters.forEach(function (el) {
      var dec = parseInt(el.getAttribute("data-dec") || "0", 10);
      el.textContent = parseFloat(el.getAttribute("data-count-to")).toFixed(dec);
    });
  } else {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          animateCount(en.target);
          cio.unobserve(en.target);
        }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------- FAQ accordion ---------- */
  document.querySelectorAll(".faq-item").forEach(function (item) {
    var btn = item.querySelector(".faq-q");
    btn.addEventListener("click", function () {
      var isOpen = item.classList.contains("open");
      document.querySelectorAll(".faq-item.open").forEach(function (other) {
        other.classList.remove("open");
        other.querySelector(".faq-q").setAttribute("aria-expanded", "false");
      });
      if (!isOpen) {
        item.classList.add("open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });

  /* ---------- anchor offset for fixed header ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("href");
      if (id.length < 2) return;
      var target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      var y = target.getBoundingClientRect().top + window.scrollY - 70;
      window.scrollTo({ top: y, behavior: reduced ? "auto" : "smooth" });
    });
  });
})();
