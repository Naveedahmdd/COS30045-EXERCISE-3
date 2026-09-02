"use strict";

document.addEventListener("DOMContentLoaded", () => {
  updateFooterYear();
  setupAccordion();
  setupEnergyCalculator();
});

function updateFooterYear() {
  const yearElements = document.querySelectorAll(".current-year");
  const currentYear = new Date().getFullYear();

  yearElements.forEach((element) => {
    element.textContent = currentYear;
  });
}

function setupAccordion() {
  const buttons = document.querySelectorAll(".accordion-button");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const contentId = button.getAttribute("aria-controls");
      const content = document.getElementById(contentId);
      const isOpen = button.getAttribute("aria-expanded") === "true";

      button.setAttribute("aria-expanded", String(!isOpen));
      content.hidden = isOpen;
    });
  });
}

function setupEnergyCalculator() {
  const form = document.getElementById("energy-form");
  if (!form) return;

  const applianceInput = document.getElementById("appliance");
  const powerInput = document.getElementById("power");
  const hoursInput = document.getElementById("hours");
  const priceInput = document.getElementById("price");

  applianceInput.addEventListener("change", () => {
    if (applianceInput.value !== "") {
      powerInput.value = applianceInput.value;
    }
    calculateAndDisplay();
  });

  [powerInput, hoursInput, priceInput].forEach((input) => {
    input.addEventListener("input", calculateAndDisplay);
  });

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    calculateAndDisplay();
  });

  function calculateAndDisplay() {
    const power = Number(powerInput.value);
    const hours = Number(hoursInput.value);
    const price = Number(priceInput.value);

    const powerValid = validateField(powerInput, "power-error", power > 0, "Enter a power value greater than 0 watts.");
    const hoursValid = validateField(hoursInput, "hours-error", hours > 0 && hours <= 24, "Enter daily use between 0.1 and 24 hours.");
    const priceValid = validateField(priceInput, "price-error", price > 0, "Enter an electricity price greater than 0.");

    if (!powerValid || !hoursValid || !priceValid) {
      document.getElementById("form-message").textContent = "Please correct the highlighted input values.";
      clearResults();
      return;
    }

    const dailyEnergy = calculateDailyEnergy(power, hours);
    const monthlyEnergy = dailyEnergy * 30;
    const yearlyEnergy = dailyEnergy * 365;
    const yearlyCost = yearlyEnergy * (price / 100);

    document.getElementById("daily-result").textContent = `${dailyEnergy.toFixed(2)} kWh`;
    document.getElementById("monthly-result").textContent = `${monthlyEnergy.toFixed(2)} kWh`;
    document.getElementById("yearly-result").textContent = `${yearlyEnergy.toFixed(2)} kWh`;
    document.getElementById("cost-result").textContent = formatCurrency(yearlyCost);
    document.getElementById("form-message").textContent = "Estimate calculated from your current values.";
  }
}

function calculateDailyEnergy(watts, hours) {
  return (watts * hours) / 1000;
}

function validateField(input, errorId, isValid, message) {
  const errorElement = document.getElementById(errorId);
  input.classList.toggle("input-invalid", !isValid);
  input.setAttribute("aria-invalid", String(!isValid));
  errorElement.textContent = isValid ? "" : message;
  return isValid;
}

function clearResults() {
  ["daily-result", "monthly-result", "yearly-result", "cost-result"].forEach((id) => {
    document.getElementById(id).textContent = "—";
  });
}

function formatCurrency(amount) {
  return new Intl.NumberFormat("en-AU", {
    style: "currency",
    currency: "AUD"
  }).format(amount);
}
