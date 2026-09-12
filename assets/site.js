(function () {
	"use strict";

	var root = document.documentElement;
	var THEME_KEY = "ns-theme";

	// Hash aliases: some links point at a sub-section inside a page rather
	// than at a top-level <section>. "#supervision" is the Clinical
	// Supervision callout that lives inside Services and Fees.
	var SECTION_ALIASES = {
		supervision: "servicesandfees-section"
	};

	function applyTheme(theme) {
		root.setAttribute("data-theme", theme);
		var toggle = document.getElementById("theme-toggle");
		if (toggle) {
			toggle.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
			toggle.textContent = theme === "dark" ? "Switch to light mode" : "Switch to dark mode";
		}
		var themeColor = document.getElementById("theme-color-meta");
		if (themeColor) {
			themeColor.setAttribute("content", theme === "dark" ? "#171D14" : "#6C7C59");
		}
	}

	function initialTheme() {
		try {
			var saved = localStorage.getItem(THEME_KEY);
			if (saved === "dark" || saved === "light") {
				return saved;
			}
		} catch (e) {
			/* localStorage unavailable — fall through to default */
		}
		// Defaults to dark regardless of OS preference; visitors can still
		// switch to light mode with the toggle, which is then remembered.
		return "dark";
	}

	// Apply the theme immediately (before DOMContentLoaded) to avoid a
	// flash of the wrong theme on page load.
	applyTheme(initialTheme());

	document.addEventListener("DOMContentLoaded", function () {
		var toggle = document.getElementById("theme-toggle");
		if (toggle) {
			toggle.addEventListener("click", function () {
				var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
				try {
					localStorage.setItem(THEME_KEY, next);
				} catch (e) {
					/* ignore if storage is blocked */
				}
				applyTheme(next);
			});
		}

		// ---- Section routing ----
		// The original Carrd export relies on a bundled main.js that isn't
		// part of this download, so this replaces it with the minimum
		// needed to show one section at a time based on the URL hash.
		var sections = Array.prototype.slice.call(
			document.querySelectorAll(".site-main > .inner > section")
		);
		var sectionIds = sections.map(function (s) {
			return s.id;
		});

		function resolveHash() {
			var hash = window.location.hash.replace("#", "").toLowerCase();
			if (!hash) {
				return "home-section";
			}
			if (SECTION_ALIASES[hash]) {
				return SECTION_ALIASES[hash];
			}
			var withSuffix = hash + "-section";
			if (sectionIds.indexOf(withSuffix) !== -1) {
				return withSuffix;
			}
			if (sectionIds.indexOf(hash) !== -1) {
				return hash;
			}
			return "home-section";
		}

		function showSection(id) {
			sections.forEach(function (section) {
				if (section.id === id) {
					section.classList.remove("inactive");
				} else {
					section.classList.add("inactive");
				}
			});
		}

		function route() {
			showSection(resolveHash());
			// If the hash points at a sub-element (like the supervision
			// callout) rather than the section itself, scroll it into view
			// once its parent section is visible.
			var rawHash = window.location.hash.replace("#", "").toLowerCase();
			if (SECTION_ALIASES[rawHash]) {
				var target = document.querySelector('[data-scroll-id="' + rawHash + '"]');
				if (target) {
					window.requestAnimationFrame(function () {
						target.scrollIntoView({ behavior: "smooth", block: "start" });
					});
				}
			}
		}

		route();
		window.addEventListener("hashchange", route);
		document.body.classList.remove("is-loading");

		// ---- Footer year ----
		// Every footer embed shares the same content, so give the year a
		// class (not a duplicate id) and update every instance at once.
		var year = new Date().getFullYear();
		var yearNodes = document.querySelectorAll(".footer-dynamic-line");
		yearNodes.forEach(function (node) {
			node.innerHTML = "&reg; " + year + " Navigating Seasons";
		});
	});
})();
