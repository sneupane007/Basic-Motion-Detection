/**
 * Main JavaScript for Motion Detection Dashboard
 */

document.addEventListener("DOMContentLoaded", function () {
  // Initial load
  fetchPlot();

  // Set up event listeners for filter changes
  document.getElementById("range").addEventListener("change", fetchPlot);
  document.getElementById("group_by").addEventListener("change", fetchPlot);
});

/**
 * Fetch the motion data plot from the API
 */
function fetchPlot() {
  // Show loading state
  const plotImage = document.getElementById("motion-plot");
  plotImage.src = "/static/img/loading.gif";
  plotImage.alt = "Loading...";

  // Get filter values
  const range = document.getElementById("range").value;
  const groupBy = document.getElementById("group_by").value;

  // Fetch data from API
  fetch(`/api/data?range=${range}&group_by=${groupBy}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (data.plot) {
        plotImage.src = `data:image/png;base64,${data.plot}`;
        plotImage.alt = "Motion Events Visualization";
      } else {
        showError("No data available for the selected range");
      }
    })
    .catch((error) => {
      console.error("Error fetching plot:", error);
      showError("Error loading data. Please try again later.");
    });
}

/**
 * Show error message
 */
function showError(message) {
  const plotImage = document.getElementById("motion-plot");
  plotImage.src = "";
  plotImage.alt = message;

  // Create an error message element
  const errorContainer = document.createElement("div");
  errorContainer.className = "error-message";
  errorContainer.textContent = message;

  // Replace the image with the error message
  plotImage.parentNode.insertBefore(errorContainer, plotImage);
  plotImage.style.display = "none";
}
