// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', () => {
    // Section Elements
    const introVideo = document.getElementById('intro-video');
    const planetSelection = document.getElementById('planet-selection');
    const starMap = document.getElementById('star-map');

    // Button Elements
    const planetButtons = document.querySelectorAll('.planet-button');

    // Transition from Intro Video to Planet Selection after 10 seconds
    setTimeout(() => {
        fadeOut(introVideo, () => {
            fadeIn(planetSelection);
        });
    }, 10000); // 10,000 milliseconds = 10 seconds

    // Add Event Listeners to Planet Buttons
    planetButtons.forEach(button => {
        button.addEventListener('click', () => {
            const planetId = button.getAttribute('data-planet');
            fadeOut(planetSelection, () => {
                fadeIn(starMap);
                renderStarMap(planetId);
            });
        });
    });

    /**
     * Fade In Effect
     * @param {HTMLElement} element 
     */
    function fadeIn(element) {
        element.classList.remove('hidden');
        element.classList.add('visible');
    }

    /**
     * Fade Out Effect
     * @param {HTMLElement} element 
     * @param {Function} callback 
     */
    function fadeOut(element, callback) {
        element.classList.remove('visible');
        element.classList.add('hidden');
        // Wait for the transition to complete before executing callback
        setTimeout(() => {
            if (callback) callback();
        }, 1000); // Match the CSS transition duration
    }

    /**
     * Render Star Map using Three.js
     * @param {String} planetId 
     */
    function renderStarMap(planetId) {
        // Basic Three.js Setup
        const container = document.getElementById('star-map');
        const scene = new THREE.Scene();

        // Camera Setup
        const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.set(0, 1.6, 0); // Set camera at height of 1.6 meters

        // Renderer Setup
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        // Handle Window Resize
        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        }, false);

        // Create Static Stars
        const starsGeometry = new THREE.BufferGeometry();
        const starsCount = 10000;
        const positions = [];

        for (let i = 0; i < starsCount; i++) {
            const x = (Math.random() - 0.5) * 2000; // Random position within a large range
            const y = (Math.random() - 0.5) * 2000;
            const z = (Math.random() - 0.5) * 2000;
            positions.push(x, y, z);
        }

        starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

        // Create a Points Material for Stars
        const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 1 });
        const starField = new THREE.Points(starsGeometry, starsMaterial);
        scene.add(starField);

        // Add Exoplanet Sphere based on selected planet
        let planet;
        if (planetId === '1') {
            planet = createPlanet(5, 0x00ff00); // Example properties for Planet 1
        } else if (planetId === '2') {
            planet = createPlanet(10, 0xff0000); // Example properties for Planet 2
        } else if (planetId === '3') {
            planet = createPlanet(15, 0x0000ff); // Example properties for Planet 3
        }

        if (planet) {
            scene.add(planet);
        }

        // Animation Loop
        function animate() {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
        }
        animate();
    }

    // Create a planet mesh
    function createPlanet(radius, color) {
        const planetGeometry = new THREE.SphereGeometry(radius, 32, 32);
        const planetMaterial = new THREE.MeshBasicMaterial({ color: color });
        return new THREE.Mesh(planetGeometry, planetMaterial);
    }
});
