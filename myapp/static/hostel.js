var jsonData = myList

console.log("hi")
console.log(jsonData)
const markers =[];
const map = L.map('map');       
map.setView([8.5445,76.9041],17) 
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);
var marker = L.marker([8.54311,76.90335]).addTo(map);
marker.bindPopup("<b>Mens Hostel , CET <b>");


var cardContainer = document.getElementById('right');

function renderHostels(hostels) {
    cardContainer.innerHTML = '';

    hostels.forEach(data => {
        var card = document.createElement('div');
        card.className = 'card';

        card.innerHTML = `
        
            <div class='hostel' style="display:flex; justify-content:center;align-items:center;">
                <img style='height:2.5rem ;width:4rem;object-fit:cover;align-self:flex-start;margin-top:5px' src="/static/assets/hostel.jpg" alt="" />
            </div>
            <div class='details'>
                <h3>${data.name}</h3>
                <p>Vacancy: ${data.current_vacancy}</p>
                <div class='additional-info' style='display:none;'>
                <p>Address: ${data.address}</p>
                <p>Rent: ${data.average_rent}</p>
                <p>Owner: ${data.owner_name}</p>
                <p>Total Capacity: ${data.total_capacity}</p>
                <p>Contact details: ${data.contact_details}</p>
                <p>Curfew: ${data.curfew}</p>
                <p>Mens/Ladies: ${data.mens_or_ladies}</p>
                <p>Mess Availability: ${data.mess_availability ? 'Yes' : 'No'}</p>
                <p>Distance from College: ${data.distance_from_college} km</p>
                </div>
                <button class='view-more-btn'>View More</button>
            </div>
        `;
        cardContainer.appendChild(card);

        markers[data.id] = L.marker([data.latitude, data.longitude]).addTo(map);
        markers[data.id].bindPopup(`<b>${data.name}<b>`);

        card.querySelector('.view-more-btn').addEventListener('click', (event) => {
            // Toggle the visibility of additional information
            const additionalInfo = card.querySelector('.additional-info');
            additionalInfo.style.display = additionalInfo.style.display === 'none' ? 'block' : 'none';

            card.querySelector('.view-more-btn').innerText = additionalInfo.style.display === 'none' ? 'View More' : 'View Less';
            // Prevent the card click event from being triggered
            event.stopPropagation();
        });

        card.addEventListener('click', () => {
            // Set the view of the map to the clicked card's location
            map.setView([data.latitude, data.longitude], 17);
            markers[data.id].openPopup();
        });

        markers[data.id].on('click', () => {
            // Open Google Maps with the marker's location
            const googleMapsUrl = `https://www.google.com/maps?q=${data.latitude},${data.longitude}`;
            window.open(googleMapsUrl, '_blank');
        });
    });
}


function searchHostels() {
    var searchInput = document.getElementById("searchInput").value.toLowerCase();

    var filteredHostels = jsonData.filter(function (hostel) {
        return hostel.name.toLowerCase().includes(searchInput);
    });

    renderHostels(filteredHostels);
}
    renderHostels(jsonData);