document.addEventListener("DOMContentLoaded",()=>{
   const form = document.getElementById("rent-form");
    if (!form) return;

  const start = document.getElementById("id_start_date");
  const end = document.getElementById("id_end_date");
  const errors = document.getElementById("rent-errors");
  errors.innerHTML = "";
  form.addEventListener("submit", (e) => {

    if (!start.value || !end.value) {
      e.preventDefault();
      errors.textContent = "Please select both start and end dates.";
      return;
    }

    const startDate = new Date(start.value);
    const endDate = new Date(end.value);
    const today = new Date();
    today.setHours(0,0,0,0);

    if (startDate >= endDate) {
      e.preventDefault();
      errors.textContent = "End date must be after start date.";
      return;
    }

    if (startDate < today) {
      e.preventDefault();
      errors.textContent = "Start date cannot be in the past.";
      return;
    }
  });

});