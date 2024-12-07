// Fetch plot and update the chart image
async function fetchPlot() {
    const range = document.getElementById('range').value;
    const groupBy = document.getElementById('group_by').value;

    // Construct API URL
    const apiUrl = `/api/plot?range=${range}&group_by=${groupBy}`;

    try {
        // Fetch data from the API
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error('Failed to fetch plot');
        }

        const data = await response.json();
        const imgElement = document.getElementById('motion-plot');

        // Update the image source
        imgElement.src = `data:image/png;base64,${data.plot}`;
    } catch (error) {
        console.error('Error fetching plot:', error);
        alert('Could not load plot. Please try again.');
    }
}