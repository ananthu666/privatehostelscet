console.log("hello_world");
console.log("Hostel data loaded:", myList);
console.log("Number of hostels:", myList.length);

const markers = [];
const map = L.map("map");
map.setView([8.5445, 76.9041], 17);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
}).addTo(map);
var marker = L.marker([8.54311, 76.90335]).addTo(map);
marker.bindPopup("<b>Mens Hostel, CET</b>");

var cardContainer = document.getElementById("right");

function renderHostels(hostels) {
  // Clear existing content and markers
  cardContainer.innerHTML = "";

  // Clear existing hostel markers (keep the CET marker)
  Object.keys(markers).forEach((key) => {
    if (markers[key]) {
      map.removeLayer(markers[key]);
      delete markers[key];
    }
  });

  if (hostels.length === 0) {
    cardContainer.innerHTML = `
      <div style="text-align: center; padding: 3rem; color: #6c757d; grid-column: 1 / -1;">
        <h3>No hostels found</h3>
        <p>Try adjusting your search criteria or filters.</p>
      </div>
    `;
    return;
  }

  hostels.forEach((data) => {
    // Since Django view already filters for approved hostels, no need to filter again
    var card = document.createElement("div");
    card.className = "hostel-card-standardized";

    // Format vacancy display
    const vacancyClass =
      data.current_vacancy > 0 ? "vacancy-available" : "vacancy-full";
    const vacancyText =
      data.current_vacancy > 0 ? `${data.current_vacancy} Available` : "Full";

    card.innerHTML = `
                <div class='hostel'>
                    <img src="/static/assets/hostel.jpg" alt="Hostel Image" />
                </div>
                <div class='details'>
                    <h3>${data.name}</h3>
                    <p class="${
                      data.mens_or_ladies === "Men"
                        ? "gender-badge-mens"
                        : data.mens_or_ladies === "Women"
                        ? "gender-badge-ladies"
                        : "gender-badge-mixed"
                    }">
                        ${data.mens_or_ladies} Hostel
                    </p>
                    <div class="vacancy-highlight ${vacancyClass}">
                        Vacancy: ${vacancyText}
                    </div>
                    <div class='additional-info' style='display:none;'>
                        <p><strong>Address:</strong> ${
                          data.address || "Not specified"
                        }</p>
                        <p><strong>Monthly Rent:</strong> ₹${
                          data.average_rent || "Contact for details"
                        }</p>
                        <p><strong>Owner:</strong> ${
                          data.owner_name || "Not specified"
                        }</p>
                        <p><strong>Contact:</strong> ${
                          data.contact_details || "Not available"
                        }</p>
                        <p><strong>Curfew Time:</strong> ${
                          data.curfew || "Not specified"
                        }</p>
                        <p><strong>Mess Available:</strong> ${
                          data.mess === "Yes" ? "✅ Yes" : "❌ No"
                        }</p>
                        <p><strong>Distance from College:</strong> ${
                          data.distance || "Not specified"
                        } km</p>
                        <p><strong>Type:</strong> ${
                          data.accommodation_type || "Hostel"
                        }</p>
                    </div>
                    <button class='btn-standardized btn-primary-standardized view-more-btn'>View More Details</button>
                </div>
            `;
    cardContainer.appendChild(card);

    markers[data.id] = L.marker([data.latitude, data.longitude]).addTo(map);
    markers[data.id].bindPopup(`
      <div style="text-align: center; padding: 0.5rem;">
        <b>${data.name}</b><br>
        <small>${data.mens_or_ladies} Hostel</small><br>
        <small>Vacancy: ${data.current_vacancy}</small>
      </div>
    `);

    card.querySelector(".view-more-btn").addEventListener("click", (event) => {
      // Toggle the visibility of additional information
      const additionalInfo = card.querySelector(".additional-info");
      const isHidden = additionalInfo.style.display === "none";

      additionalInfo.style.display = isHidden ? "block" : "none";
      card.querySelector(".view-more-btn").innerText = isHidden
        ? "View Less"
        : "View More Details";

      // Add smooth animation
      if (isHidden) {
        additionalInfo.style.opacity = "0";
        additionalInfo.style.transform = "translateY(-10px)";
        setTimeout(() => {
          additionalInfo.style.transition = "all 0.3s ease";
          additionalInfo.style.opacity = "1";
          additionalInfo.style.transform = "translateY(0)";
        }, 10);
      }

      // Prevent the card click event from being triggered
      event.stopPropagation();
    });

    card.addEventListener("click", () => {
      // Set the view of the map to the clicked card's location
      map.setView([data.latitude, data.longitude], 17);
      markers[data.id].openPopup();
    });

    markers[data.id].on("click", () => {
      // Open Google Maps with the marker's location
      const googleMapsUrl = `https://www.google.com/maps?q=${data.latitude},${data.longitude}`;
      window.open(googleMapsUrl, "_blank");
    });
  });
}

function filterHostels() {
  console.log("Filter function called");

  var searchInput = document
    .getElementById("searchInput")
    .value.toLowerCase()
    .trim();

  var genderFilterElement = document.getElementById("genderFilter");
  var genderFilter = genderFilterElement ? genderFilterElement.value : "all";

  console.log("Search Input:", searchInput);
  console.log("Gender Filter:", genderFilter);
  console.log("Total hostels:", myList.length);

  // Start with all hostels
  var filteredHostels = myList;

  // Apply text search filter
  if (searchInput !== "") {
    filteredHostels = filteredHostels.filter(function (hostel) {
      return (
        hostel.name.toLowerCase().includes(searchInput) ||
        hostel.address.toLowerCase().includes(searchInput) ||
        hostel.owner_name.toLowerCase().includes(searchInput) ||
        hostel.mens_or_ladies.toLowerCase().includes(searchInput) ||
        hostel.average_rent.toString().includes(searchInput)
      );
    });
  }

  // Apply gender filter
  if (genderFilter !== "all") {
    filteredHostels = filteredHostels.filter(function (hostel) {
      var hostelGender = hostel.mens_or_ladies; // Use the standardized values
      console.log(
        "Checking hostel:",
        hostel.name,
        "Gender:",
        hostel.mens_or_ladies,
        "Filter:",
        genderFilter
      );

      if (genderFilter === "mens") {
        return hostelGender === "Men";
      } else if (genderFilter === "ladies") {
        return hostelGender === "Women";
      } else if (genderFilter === "mixed") {
        return hostelGender === "Mixed";
      }
      return true;
    });
  }

  console.log("Search Input:", searchInput);
  console.log("Gender Filter:", genderFilter);
  console.log(
    "Filtered Results:",
    filteredHostels.length,
    "out of",
    myList.length
  );

  renderHostels(filteredHostels);
}

function clearSearch() {
  document.getElementById("searchInput").value = "";
  document.getElementById("genderFilter").value = "all";
  renderHostels(myList);
}

// Legacy function for backward compatibility
function searchHostels() {
  filterHostels();
}

renderHostels(myList);
