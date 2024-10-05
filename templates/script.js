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

    // Animate Moving Background using GSAP
    gsap.to(".moving-background", {
        x: 100,
        duration: 60,
        repeat: -1,
        yoyo: true,
        ease: "linear"
    });

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
        const container = document.getElementById('three-container');
        const scene = new THREE.Scene();

        // Camera Setup
        const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
        camera.position.z = 50;

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

        // Create Stars
        const starsGeometry = new THREE.BufferGeometry();
        const starsCount = 10000;
        const positions = [];

        for (let i = 0; i < starsCount; i++) {
            const x = (Math.random() - 0.5) * 2000;
            const y = (Math.random() - 0.5) * 2000;
            const z = (Math.random() - 0.5) * 2000;
            positions.push(x, y, z);
        }

        starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

        const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 1 });
        const starField = new THREE.Points(starsGeometry, starsMaterial);
        scene.add(starField);

        // Add Exoplanet Sphere (Optional)
        const planetGeometry = new THREE.SphereGeometry(5, 32, 32);
        const planetMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
        const planet = new THREE.Mesh(planetGeometry, planetMaterial);
        scene.add(planet);

        // Animation Loop
        function animate() {
            requestAnimationFrame(animate);
            starField.rotation.x += 0.0005;
            starField.rotation.y += 0.001;
            planet.rotation.y += 0.005;
            renderer.render(scene, camera);
        }
        animate();

        // Optional: Add OrbitControls for Interaction
        /*
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        function animate() {
            requestAnimationFrame(animate);
            starField.rotation.x += 0.0005;
            starField.rotation.y += 0.001;
            planet.rotation.y += 0.005;
            controls.update();
            renderer.render(scene, camera);
        }
        animate();
        */
    }
});
