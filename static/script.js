// Sample data for exoplanets (In a real application, you might fetch this from a server)
const exoplanets = [
    { name: "Kepler-22b", id: "kepler-22b" },
    { name: "Proxima Centauri b", id: "proxima-centauri-b" },
    { name: "TRAPPIST-1d", id: "trappist-1d" },
    // Add more exoplanets as needed
];

// Populate the exoplanet selection dropdown
const select = document.getElementById('exoplanet-select');
exoplanets.forEach(planet => {
    const option = document.createElement('option');
    option.value = planet.id;
    option.textContent = planet.name;
    select.appendChild(option);
});

// Function to view the sky for the selected exoplanet
document.getElementById('view-sky').addEventListener('click', () => {
    const selectedPlanet = select.value;
    renderSkyMap(selectedPlanet);
});

// Function to render the sky map
function renderSkyMap(planet) {
    const skyMapDiv = document.getElementById('sky-map');
    skyMapDiv.innerHTML = ''; // Clear previous content
    const message = document.createElement('p');
    message.textContent = `Rendering sky map for ${planet}...`;
    skyMapDiv.appendChild(message);
    
    // Here you would implement the sky rendering logic using a library
    // For demonstration purposes, we're showing a placeholder
    const placeholder = document.createElement('div');
    placeholder.style.width = '100%';
    placeholder.style.height = '100%';
    placeholder.style.background = 'rgba(255, 255, 255, 0.1)';
    placeholder.textContent = 'Sky map will be displayed here.';
    placeholder.style.display = 'flex';
    placeholder.style.justifyContent = 'center';
    placeholder.style.alignItems = 'center';
    skyMapDiv.appendChild(placeholder);
}
