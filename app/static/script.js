// ===============
// navigation
// ===============
const sidebar = document.querySelector(".sidebar");
const formToggler = document.getElementById("form-toggler");
const profForm = document.getElementById("togglable-form");
let isVisibleForm = false;
let compact = false;

const toggler = document.getElementById("toggler");

const collapse = () => {
  compact
    ? sidebar.classList.add("desactivate")
    : sidebar.classList.remove("desactivate");
  compact = !compact;
};

const toggleForm = () => {
  isVisibleForm
    ? profForm.classList.add("form-hidden")
    : profForm.classList.remove("form-hidden");
  isVisibleForm = !isVisibleForm;
};

toggler.addEventListener("click", collapse);
formToggler.addEventListener("click", toggleForm);
document.getElementById("form-reset").addEventListener("click", toggleForm);
