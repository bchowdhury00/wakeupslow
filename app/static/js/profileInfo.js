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


function confirmLocation() {
  var input = document.getElementById("pac-input").value;
  if (input == "") {
    input = "{latitude:" + currentPosition['latitude'] + ", " + "longitude: " + currentPosition['longitude'] + "}";
  }
  console.log(input);
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
    })
}
