function setupPageWidth() {
  const root = document.querySelector(":root");
  const innerWidth = window.innerWidth;
  const scrollbarWidth = innerWidth - root.clientWidth;
  root.style.setProperty("--page-width", innerWidth + "px");
  root.style.setProperty("--scrollbar-width", scrollbarWidth + "px");
}
window.addEventListener("resize", () => {
  setupPageWidth();
});
window.addEventListener("scroll", () => {
  setupPageWidth();
});
console.log("hi");
