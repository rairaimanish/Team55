function getCoordinates(str) {
  var regex = /\-?\d+\.\d+, \-?\d+\.\d+/g;
  var coordinates = str.match(regex);
  return coordinates;
}

function initMap(cords, infoContent) {
  if (cords) {
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 12,
      center: cords
    });

    var marker = new google.maps.Marker({
      position: cords,
      map: map
    });

    // Create a new info window with the provided content
    var infowindow = new google.maps.InfoWindow({
      content: infoContent
    });

    // Open the info window when the marker is clicked
    marker.addListener('click', function() {
      infowindow.open(map, marker);
    });
  }
}

window.onload = function () {
  document.getElementsByClassName("chat-form")[0].addEventListener("submit", function (event) {
    // Prevent the form from submitting and refreshing the page
    event.preventDefault();

    let userInput = document.getElementsByClassName("user-input")[0].value;
    let url = `/palm2`;

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_input: userInput })
    })
      .then((response) => response.json())
      .then((data) => {
        let content = data.content;
        let cords = data.cords;
        let attributes = data.attributes;

        cords = getCoordinates(cords);
        let resultDiv = document.getElementsByClassName("result")[0];
        resultDiv.innerHTML = content;

        let attributesDiv = document.getElementsByClassName("attributes")[0];
        attributesDiv.textContent = attributes;

        if (cords) {
          var latLng = cords[0].split(',').map(Number);
          var newCords = { lat: latLng[0], lng: latLng[1] };
          initMap(newCords, content); // Update the map with new coordinates and info window content
        }
      })
      .catch((error) => {
        console.error("Error fetching PaLM response:", error);
      });
  });
  initMap({ lat: 22.3193, lng: 114.1694 }); // Initialize the map with Hong Kong coordinates
};