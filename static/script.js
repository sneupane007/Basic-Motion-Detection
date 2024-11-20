document.getElementById('fetchData').addEventListener('click', async () => {
    const range = document.getElementById('range').value;
    const chartDiv = document.getElementById('chart');
    const plotImage = document.getElementById('plotImage');

    // Fetch the plot image from the API
    try {
        const response = await fetch(`/api/data?range=${range}`);
        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }
        // Set the image source to the response URL
        plotImage.src = `/api/data?range=${range}&_=${new Date().getTime()}`;
    } catch (error) {
        console.error("Error fetching data:", error);
        chartDiv.innerHTML = '<p>Failed to load data.</p>';
    }
});
