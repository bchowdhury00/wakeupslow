var currentPosition = {
  "latitude": 0,
  "longitude": 0
};

console.log('hello');

document.getElementById('infoButton').addEventListener('click', editContact);
document.getElementById('locationButton').addEventListener('click', editLocation);
document.getElementById('confirmLocationButton').addEventListener("click", confirmLocation);

function editContact() {
  console.log('info')
  document.getElementById('contactForm').removeAttribute('style');
  document.getElementById('locationForm').style.display = 'none';
  document.getElementById('locationButton').style.visibility = 'visible';
  document.getElementById('infoButton').style.visibility = 'hidden';
  document.getElementById('contactForm').scrollIntoView();
}

function editLocation() {
  console.log('location')
  document.getElementById('locationForm').removeAttribute('style');
  document.getElementById('contactForm').style.display = 'none';
  document.getElementById('infoButton').style.visibility = 'visible';
  document.getElementById('locationButton').style.visibility = 'hidden';
  document.getElementById('locationForm').scrollIntoView();
}

var promiseMade;
function confirmLocation() {
  var input = document.getElementById("pac-input").value;
  if (input == "") {
    input = "{lat:" + currentPosition['latitude'] + ", " + "lng: " + currentPosition['longitude'] + "}";
  }
  if (input.length < 2){
    window.location = "/profile?mType=3";
  }
  console.log(input);
  var validation = validateAddress(input);
  if (promiseMade) {
    validation.then(function(result) {
      console.log(result);

      if (result != false){
        input = "{lat:" + result[0] + ", lng:" + result[1] + "}";
        fetch("/profile", {
            method: "POST",
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(input)
          }).then(res => res.json())
          .then(data => {
            console.log(window.location);
            window.location = data.redirect;
          });
      } else {
        window.location = "/profile?mType=3";
      }
    });
  } else {
    console.log(input)
    if (validation){
      fetch("/profile", {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(input)
        }).then(res => res.json())
        .then(data => {
          console.log(window.location);
          window.location = data.redirect;
        });
      } else {
        window.location = "/profile?mType=3";
      }
  }
}


function validateAddress(address) {
  if (address[0] == "{") {
    return true;
  }
  promiseMade = true;
  return new Promise(function(resolve, reject) {
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({
      address: address
    }, function(results, error) {
      if (error != "OK") {
        return resolve(false);
      }
      //console.log(results);
      return resolve([results[0].geometry.location.lat(), results[0].geometry.location.lng()]);
    });
  });
}
