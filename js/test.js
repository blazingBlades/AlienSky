// script.js

document.addEventListener('DOMContentLoaded', () => {
  // Section Elements
  const introVideo = document.getElementById('intro-video');
  const planetSelection = document.getElementById('planet-selection');
  const starMap = document.getElementById('star-map');

  // Button Elements
  const planetButtons = document.querySelectorAll('.planet-button');

  // Loading Spinner
  const loadingSpinner = document.getElementById('loading-spinner');

  // Exoplanet Data
  const exoplanetData = {
      'kepler-22b': {
          seed: 1,
          atmosphereColor: 0x1e90ff, // DodgerBlue
          description: "Kepler-22b: A potentially habitable exoplanet located in the habitable zone."
      },
      'proxima-centauri-b': {
          seed: 2,
          atmosphereColor: 0xff4500, // OrangeRed
          description: "Proxima Centauri b: An exoplanet orbiting within the habitable zone of Proxima Centauri."
      },
      'gliese-667-cc': {
          seed: 3,
          atmosphereColor: 0x32cd32, // LimeGreen
          description: "Gliese 667 Cc: An exoplanet located within the habitable zone of its star."
      },
      'trappist-1e': {
          seed: 4,
          atmosphereColor: 0xffa500, // Orange
          description: "TRAPPIST-1e: An exoplanet in the habitable zone of TRAPPIST-1."
      }
      // Add more exoplanets as needed
  };

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
   * Seeded Random Number Generator (LCG)
   * @param {Number} seed 
   * @returns {Function} - Returns a function that generates a pseudo-random number between 0 and 1
   */
  function seededRandom(seed) {
      let value = seed;
      return function() {
          value = (value * 9301 + 49297) % 233280;
          return value / 233280;
      }
  }

  /**
   * Render Star Map using Three.js
   * @param {String} planetId 
   */
  function renderStarMap(planetId) {
      console.log("Rendering star map for planet:", planetId); // Debugging log

      // Show loading spinner
      loadingSpinner.classList.remove('hidden');
      loadingSpinner.classList.add('visible');

      // Get exoplanet data
      const planet = exoplanetData[planetId];
      if (!planet) {
          console.error("Exoplanet data not found for:", planetId);
          return;
      }

      // Basic Three.js Setup
      const container = document.getElementById('three-container');
      
      // Clear any existing content in the container
      container.innerHTML = '';

      const scene = new THREE.Scene();

      const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 10000);
      camera.position.set(0, 0, 1000); // Observer's position

      // Renderer Setup
      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(container.clientWidth, container.clientHeight);
      container.appendChild(renderer.domElement);
      renderer.setClearColor(0x000000); // Black background

      // OrbitControls for interactivity
      const controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableZoom = true; // Allow zooming
      controls.enablePan = true;  // Allow panning
      controls.enableDamping = true; // Smooth controls
      controls.dampingFactor = 0.05;

      // Handle window resize
      window.addEventListener('resize', () => {
          camera.aspect = container.clientWidth / container.clientHeight;
          camera.updateProjectionMatrix();
          renderer.setSize(container.clientWidth, container.clientHeight);
      });

      // Add Ambient Light
      const ambientLight = new THREE.AmbientLight(0xffffff, 1);
      scene.add(ambientLight);

      // Create Stars with Seeded Randomness
      const starsGeometry = new THREE.BufferGeometry();
      const starsCount = 10000;
      const positions = [];

      const rand = seededRandom(planet.seed);

      for (let i = 0; i < starsCount; i++) {
          const theta = Math.acos(2 * rand() - 1); // Uniformly distributed points on a sphere
          const phi = rand() * 2 * Math.PI;
          const radius = 5000; // Adjust for density
          const x = radius * Math.sin(theta) * Math.cos(phi);
          const y = radius * Math.sin(theta) * Math.sin(phi);
          const z = radius * Math.cos(theta);
          positions.push(x, y, z);
      }

      starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
      const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 1 });
      const starField = new THREE.Points(starsGeometry, starsMaterial);
      scene.add(starField);

      // Add Atmospheric Effect
      const atmosphereGeometry = new THREE.SphereGeometry(1000, 32, 32);
      const atmosphereMaterial = new THREE.MeshBasicMaterial({
          color: planet.atmosphereColor,
          transparent: true,
          opacity: 0.2,
          side: THREE.BackSide
      });
      const atmosphere = new THREE.Mesh(atmosphereGeometry, atmosphereMaterial);
      scene.add(atmosphere);

      // Add Planet-Specific Features
      addPlanetSpecificFeatures(scene, planetId);

      // Optional: Add subtle rotation to the star field
      const rotationSpeed = 0.0005; // Adjust as needed

      // Animation Loop
      function animate() {
          requestAnimationFrame(animate);
          // Rotate the star field slowly
          starField.rotation.y += rotationSpeed;
          controls.update(); // Update controls
          renderer.render(scene, camera);
      }
      animate();

      // Hide loading spinner after rendering starts
      // Since rendering is continuous, we'll hide it immediately after setting up
      // For more accurate loading status, implement event-based checks
      setTimeout(() => {
          loadingSpinner.classList.remove('visible');
          loadingSpinner.classList.add('hidden');
      }, 2000); // 2 seconds delay; adjust as needed based on actual loading time

      // Optional: Display Exoplanet Description
      displayExoplanetDescription(planet.description);
  }

  /**
   * Add planet-specific features to the scene
   * @param {THREE.Scene} scene 
   * @param {String} planetId 
   */
  function addPlanetSpecificFeatures(scene, planetId) {
      switch (planetId) {
          case 'kepler-22b':
              // Example: Add a hypothetical moon
              addMoon(scene, 100, 0xaaaaaa, 300, 0, -500, 'keplerMoon');
              break;
          case 'proxima-centauri-b':
              // Example: Add Proxima Centauri's star and planet
              addCelestialBody(scene, 'proxima', 200, 0xff4500); // Star
              addMoon(scene, 50, 0x555555, 200, 0, -300, 'proximaMoon'); // Planet
              break;
          case 'gliese-667-cc':
              // Example: Add multiple moons
              addMoon(scene, 80, 0x888888, 250, 150, -400, 'glieseMoon1');
              addMoon(scene, 60, 0xcccccc, -250, -150, -400, 'glieseMoon2');
              break;
          case 'trappist-1e':
              // Example: Add TRAPPIST-1's star and multiple planets
              addCelestialBody(scene, 'trappist', 300, 0x00ff00); // Star
              addMoon(scene, 40, 0xffa500, 180, -100, -350, 'trappistMoon1');
              addMoon(scene, 40, 0x1e90ff, -180, 100, -350, 'trappistMoon2');
              break;
          // Add more cases for other planets as needed
          default:
              break;
      }
  }

  /**
   * Helper function to create a celestial body (e.g., moon, star)
   * @param {THREE.Scene} scene
   * @param {String} type - Type of celestial body (e.g., 'moon', 'star')
   * @param {Number} size - Radius of the sphere
   * @param {Number} color - Hex color value
   * @param {Number} x - X position
   * @param {Number} y - Y position
   * @param {Number} z - Z position
   * @param {String} name - Name identifier for the object
   */
  function addMoon(scene, size, color, x, y, z, name) {
      const geometry = new THREE.SphereGeometry(size, 32, 32);
      const material = new THREE.MeshStandardMaterial({ color: color });
      const moon = new THREE.Mesh(geometry, material);
      moon.position.set(x, y, z);
      moon.name = name; // Assign a name for identification
      scene.add(moon);
  }

  /**
   * Helper function to create a celestial body like a star
   * @param {THREE.Scene} scene
   * @param {String} type
   * @param {Number} size
   * @param {Number} color
   */
  function addCelestialBody(scene, type, size, color) {
      const geometry = new THREE.SphereGeometry(size, 32, 32);
      const material = new THREE.MeshBasicMaterial({ color: color, emissive: color });
      const star = new THREE.Mesh(geometry, material);
      star.position.set(0, 0, -1000); // Position it far in the background
      star.name = `${type}Star`; // Assign a name for identification
      scene.add(star);
  }

  /**
   * Display Exoplanet Description
   * @param {String} description 
   */
  function displayExoplanetDescription(description) {
      // Create a description overlay
      let descriptionOverlay = document.getElementById('description-overlay');
      if (!descriptionOverlay) {
          descriptionOverlay = document.createElement('div');
          descriptionOverlay.id = 'description-overlay';
          descriptionOverlay.style.position = 'absolute';
          descriptionOverlay.style.bottom = '20px';
          descriptionOverlay.style.left = '50%';
          descriptionOverlay.style.transform = 'translateX(-50%)';
          descriptionOverlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
          descriptionOverlay.style.color = '#fff';
          descriptionOverlay.style.padding = '10px 20px';
          descriptionOverlay.style.borderRadius = '5px';
          descriptionOverlay.style.maxWidth = '80%';
          descriptionOverlay.style.textAlign = 'center';
          descriptionOverlay.style.fontSize = '1rem';
          descriptionOverlay.style.zIndex = '20';
          document.body.appendChild(descriptionOverlay);
      }
      descriptionOverlay.textContent = description;
  }

});
