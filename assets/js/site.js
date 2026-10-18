// Before/after slider: the range input drives a CSS variable that clips the "before" image.
document.querySelectorAll(".compare").forEach((fig) => {
  const range = fig.querySelector(".compare-range");
  const stage = fig.querySelector(".compare-stage");
  const set = (v) => {
    const pos = Math.max(0, Math.min(100, v));
    fig.style.setProperty("--pos", pos + "%");
    range.value = pos;
  };
  range.addEventListener("input", () => set(+range.value));

  // Let people drag directly on the image too, not only on the slider bar.
  let dragging = false;
  const fromPointer = (e) => {
    const box = stage.getBoundingClientRect();
    set(((e.clientX - box.left) / box.width) * 100);
  };
  stage.addEventListener("pointerdown", (e) => { dragging = true; stage.setPointerCapture(e.pointerId); fromPointer(e); });
  stage.addEventListener("pointermove", (e) => { if (dragging) fromPointer(e); });
  stage.addEventListener("pointerup", () => { dragging = false; });
  stage.addEventListener("pointercancel", () => { dragging = false; });
  stage.style.touchAction = "pan-y";
  // Images are natively draggable; that drag would fire pointercancel after the first move.
  stage.addEventListener("dragstart", (e) => e.preventDefault());
  stage.querySelectorAll("img").forEach((img) => { img.draggable = false; });
});
