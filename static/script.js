document.getElementById('view-sky').addEventListener('click', function() {
  const exoplanet = document.getElementById('exoplanet-select').value;
  const skyMap = document.getElementById('sky-map');
  if (exoplanet) {
      skyMap.textContent = `Displaying sky view from ${exoplanet}...`;
  } else {
      skyMap.textContent = 'Please select an exoplanet!';
  }
});
