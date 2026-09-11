// Single orchestrated page-load moment: the hero "query" types itself out.
// Respects prefers-reduced-motion by rendering instantly for those users.
document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("terminal-query");
  if (!el) return;

  const query = el.dataset.query || "";
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduceMotion) {
    el.textContent = query;
    return;
  }

  let i = 0;
  const speed = 22; // ms per character

  function type() {
    if (i <= query.length) {
      el.textContent = query.slice(0, i);
      i++;
      setTimeout(type, speed);
    }
  }

  type();
});
