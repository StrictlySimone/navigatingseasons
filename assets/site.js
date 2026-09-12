(function () {
	"use strict";

	var root = document.documentElement;
	var THEME_KEY = "ns-theme";

	// The <head> of every page sets data-theme synchronously (inline script)
	// before CSS paints, to avoid a flash of the wrong theme. This file only
	// needs to sync the toggle button/meta tag to whatever was already set,
	// and handle clicks.

	function syncControls(theme) {
		var toggle = document.getElementById("theme-toggle");
		if (toggle) {
			toggle.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
			var label = toggle.querySelector(".theme-toggle-label");
			if (label) {
				label.textContent = theme === "dark" ? "Light" : "Dark";
			}
		}
		var themeColor = document.getElementById("theme-color-meta");
		if (themeColor) {
			themeColor.setAttribute("content", theme === "dark" ? "#171D14" : "#6C7C59");
		}
	}

	document.addEventListener("DOMContentLoaded", function () {
		syncControls(root.getAttribute("data-theme") || "dark");

		var toggle = document.getElementById("theme-toggle");
		if (toggle) {
			toggle.addEventListener("click", function () {
				var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
				root.setAttribute("data-theme", next);
				try {
					localStorage.setItem(THEME_KEY, next);
				} catch (e) {
					/* ignore if storage is blocked */
				}
				syncControls(next);
			});
		}

		var year = new Date().getFullYear();
		document.querySelectorAll(".current-year").forEach(function (node) {
			node.textContent = year;
		});
	});
})();
