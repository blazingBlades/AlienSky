document.addEventListener("DOMContentLoaded", function() {
    
    // Show the planet selection section after a delay (3 seconds)
    setTimeout(() => {
        const planetSelection = document.getElementById('planet-selection');
        planetSelection.classList.remove('hidden');
        planetSelection.classList.add('visible'); // Make it visible with a transition
    }, 3000); // Show the selection section after 3 seconds

    // Set a timeout to change the background after 3 seconds
    setTimeout(() => {
        // Change the body background to a solid color or a new image smoothly
        document.body.style.background = '#000'; // Change to a solid color or another image
        document.body.style.backgroundSize = 'cover'; // Ensure the new background is sized properly
    }, 3000); // Background changes after 3 seconds

    // Grab all the planet buttons
    const planetButtons = document.querySelectorAll('.planet-button');
    
    // Loop through each planet button and add a click event listener
    planetButtons.forEach(button => {
        button.addEventListener('click', () => {
            const planet = button.getAttribute('data-planet');
            console.log("Selected planet:", planet);

            // Hide the planet selection section smoothly
            const planetSelection = document.getElementById('planet-selection');
            planetSelection.classList.remove('visible'); // Remove visible class
            planetSelection.classList.add('hidden'); // Add hidden class

            // Show the star map section smoothly
            const starMap = document.getElementById('star-map');
            starMap.classList.remove('hidden'); // Remove hidden class
            setTimeout(() => {
                starMap.classList.add('visible'); // Add visible class after a brief pause
            }, 100); // Delay for visibility transition effect

            // Load the star map based on the selected planet
            loadStarMap(planet);
        });
    });

    // Function to load star maps based on the selected planet
    function loadStarMap(planet) {
        // Placeholder function for loading star map based on selected planet
        console.log(`Loading star map for ${planet}...`);
        // Initialize your Three.js rendering here for the specific planet
    }
});
