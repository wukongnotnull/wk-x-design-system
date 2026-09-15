const THEMES = ["lights-out", "dim", "default"];
const ACCENTS = {
  blue: "var(--accent-blue)",
  yellow: "var(--accent-yellow)",
  pink: "var(--accent-pink)",
  purple: "var(--accent-purple)",
  orange: "var(--accent-orange)",
  green: "var(--accent-green)"
};

function applyTheme(root, theme) {
  const next = THEMES.includes(theme) ? theme : "lights-out";
  root.dataset.theme = next;
  return next;
}

function applyAccent(root, accent) {
  const next = ACCENTS[accent] ? accent : "blue";
  root.style.setProperty("--main-accent", ACCENTS[next]);
  return next;
}

function persist(storage, theme, accent) {
  storage.setItem("xds-theme", theme);
  storage.setItem("xds-accent", accent);
}

function loadPersisted(storage) {
  return {
    theme: storage.getItem("xds-theme") || "lights-out",
    accent: storage.getItem("xds-accent") || "blue"
  };
}

function boot(root, storage) {
  const loaded = loadPersisted(storage);
  const theme = applyTheme(root, loaded.theme);
  const accent = applyAccent(root, loaded.accent);
  persist(storage, theme, accent);
  return { theme, accent };
}

function onReady() {
  const root = document.documentElement;
  const storage = window.localStorage;
  boot(root, storage);

  document.querySelectorAll("[data-set-theme]").forEach((button) => {
    button.addEventListener("click", () => {
      const theme = applyTheme(root, button.getAttribute("data-set-theme"));
      persist(storage, theme, loadPersisted(storage).accent);
    });
  });

  document.querySelectorAll("[data-set-accent]").forEach((button) => {
    button.addEventListener("click", () => {
      const accent = applyAccent(root, button.getAttribute("data-set-accent"));
      persist(storage, loadPersisted(storage).theme, accent);
    });
  });
}

if (typeof document !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onReady);
  } else {
    onReady();
  }
}

const api = {
  THEMES,
  ACCENTS,
  applyTheme,
  applyAccent,
  persist,
  loadPersisted,
  boot
};

if (typeof module === "object" && module.exports) {
  module.exports = api;
}
