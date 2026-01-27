(function () {
  var dragging = false;
  var startX = 0;
  var startY = 0;
  var startLeft = 0;
  var startTop = 0;

  function isInteractive(target) {
    if (!target) return false;
    return (
      target.closest(".js-no-drag") ||
      target.closest("input, textarea, select, button, a") ||
      target.closest(".dash-graph") ||
      target.closest(".plotly") ||
      target.closest("svg, canvas")
    );
  }

  function onMouseDown(e) {
    if (e.button !== 0) return;
    var panel = document.getElementById("transport-drawer");
    if (!panel || panel.style.display === "none") return;
    if (!panel.contains(e.target)) return;
    if (isInteractive(e.target)) return;

    dragging = true;
    var rect = panel.getBoundingClientRect();
    startX = e.clientX;
    startY = e.clientY;
    startLeft = rect.left;
    startTop = rect.top;

    panel.style.right = "auto";
    panel.style.bottom = "auto";
    panel.style.left = startLeft + "px";
    panel.style.top = startTop + "px";
    document.body.style.userSelect = "none";
    e.preventDefault();
  }

  function onMouseMove(e) {
    if (!dragging) return;
    var panel = document.getElementById("transport-drawer");
    if (!panel) return;
    var dx = e.clientX - startX;
    var dy = e.clientY - startY;
    var rect = panel.getBoundingClientRect();
    var width = rect.width;
    var height = rect.height;
    var maxLeft = window.innerWidth - width;
    var maxTop = window.innerHeight - height;
    var newLeft = Math.max(0, Math.min(startLeft + dx, maxLeft));
    var newTop = Math.max(0, Math.min(startTop + dy, maxTop));
    panel.style.left = newLeft + "px";
    panel.style.top = newTop + "px";
  }

  function onMouseUp() {
    if (!dragging) return;
    dragging = false;
    document.body.style.userSelect = "";
  }

  document.addEventListener("mousedown", onMouseDown);
  document.addEventListener("mousemove", onMouseMove);
  document.addEventListener("mouseup", onMouseUp);
})();
