/*
  This js file is for individual users to modify the scripts for their personal site,
  or for the implementation of features specifically for their site. Anything that
  is an official part of the theme (ex. Pull Requests) should be included in main.js
  and follow the formatting and style given.
*/

var savedTheme = localStorage.getItem("dark-mode-storage") || "light";

var toggle = document.getElementById("dark-mode-toggle");
var icon_toggle = document.getElementById("dark-mode-toggle-icon");
var darkTheme = document.getElementById("dark-mode-theme");
const userPrefersDark =
  window.matchMedia &&
  window.matchMedia("(prefers-color-scheme: dark)").matches;

const userPrefersLight =
  window.matchMedia &&
  window.matchMedia("(prefers-color-scheme: light)").matches;

if (userPrefersDark) {
  setTheme("dark");
}

if (savedTheme == "dark") {
  setTheme(savedTheme);
}

if (savedTheme == "light") {
  setTheme(savedTheme);
}

toggle.addEventListener("click", () => {
  if (icon_toggle.className === "fas fa-moon fa-lg") {
    setTheme("dark");
  } else if (icon_toggle.className === "fas fa-sun fa-lg") {
    setTheme("light");
  }
});

var inserthtml = function () {
  var doc = document;
  var head = doc.getElementsByTagName("head")[0];
  console.log("Insert!");
  head.insertAdjacentHTML(
    "afterbegin",
    '<link id="always-adopt-theme" rel="stylesheet" href="/css/always.css">'
  );
};

setTimeout(inserthtml, 600);

function setTheme(mode) {
  if (mode === "dark") {
    darkTheme.disabled = false;
    icon_toggle.className = "fas fa-sun fa-lg";
    localStorage.setItem("dark-mode-storage", mode);
  } else if (mode === "light") {
    darkTheme.disabled = true;
    icon_toggle.className = "fas fa-moon fa-lg";
    localStorage.setItem("dark-mode-storage", mode);
  }
}
