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
  cardContainer.innerHTML = "";

  // Clear existing hostel markers
  Object.keys(markers).forEach((key) => {
    if (markers[key]) {
      map.removeLayer(markers[key]);
      delete markers[key];
    }
  });

  if (hostels.length === 0) {
    cardContainer.innerHTML = `
      <div style="text-align: center; padding: 2rem; color: #666;">
        <h3>No hostels found</h3>
        <p>Try adjusting your search.</p>
      </div>
    `;
    return;
  }

  hostels.forEach((data) => {
    var card = document.createElement("div");
    card.className = "hostel-card-standardized";

    const vacancyClass =
      data.current_vacancy > 0 ? "vacancy-available" : "vacancy-full";
    const vacancyText =
      data.current_vacancy > 0 ? `${data.current_vacancy} Available` : "Full";

    // Determine gender badge class based on hostel type
    let genderBadgeClass = "gender-badge-mixed";
    if (data.mens_or_ladies === "Men") {
      genderBadgeClass = "gender-badge-mens";
    } else if (data.mens_or_ladies === "Women") {
      genderBadgeClass = "gender-badge-ladies";
    }

    card.innerHTML = `
      <div class='hostel'>
        <img src="/static/assets/hostel.jpg" alt="Hostel" />
      </div>
      <div class='details'>
        <h3>${data.name}</h3>
        <p class="${genderBadgeClass}">${data.mens_or_ladies} Hostel</p>
        <div class="vacancy-highlight ${vacancyClass}">
          Vacancy: ${vacancyText}
        </div>
        <div class='additional-info' style='display:none;'>
          <p><strong>Address:</strong> ${data.address || "Not specified"}</p>
          <p><strong>Rent:</strong> ₹${
            data.average_rent || "Contact for details"
          }</p>
          <p><strong>Owner:</strong> ${data.owner_name || "Not specified"}</p>
          <p><strong>Contact:</strong> ${
            data.contact_details || "Not available"
          }</p>
          <p><strong>Curfew:</strong> ${data.curfew || "Not specified"}</p>
          <p><strong>Mess:</strong> ${data.mess === "Yes" ? "Yes" : "No"}</p>
          <p><strong>Distance:</strong> ${
            data.distance || "Not specified"
          } km</p>
        </div>
        <button class='btn-standardized view-more-btn'>View Details</button>
      </div>
    `;

    cardContainer.appendChild(card);

    // Add map marker
    markers[data.id] = L.marker([data.latitude, data.longitude]).addTo(map);
    markers[data.id].bindPopup(
      `<b>${data.name}</b><br>Vacancy: ${data.current_vacancy}`
    );

    // Add click events
    card.querySelector(".view-more-btn").addEventListener("click", (event) => {
      const additionalInfo = card.querySelector(".additional-info");
      const isHidden = additionalInfo.style.display === "none";

      additionalInfo.style.display = isHidden ? "block" : "none";
      card.querySelector(".view-more-btn").innerText = isHidden
        ? "Hide Details"
        : "View Details";

      event.stopPropagation();
    });

    card.addEventListener("click", () => {
      map.setView([data.latitude, data.longitude], 17);
      markers[data.id].openPopup();
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
