// Clean Hostel App JavaScript
console.log("Hostel App Loaded Successfully");

// Initialize map
const map = L.map("map").setView([8.5445, 76.9041], 15);
const markers = {};

// Add map tiles
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors",
}).addTo(map);

// Add CET Campus marker
const cetMarker = L.marker([8.54311, 76.90335]).addTo(map);
cetMarker.bindPopup(
  "<h5>🏛️ CET Campus</h5><p>College of Engineering Trivandrum</p>"
);

// Get container element
const hostelsList = document.getElementById("hostelsList");

// Render hostels function
function renderHostels(hostels) {
  hostelsList.innerHTML = "";

  // Clear existing markers
  Object.keys(markers).forEach((key) => {
    if (markers[key]) {
      map.removeLayer(markers[key]);
      delete markers[key];
    }
  });

  if (hostels.length === 0) {
    hostelsList.innerHTML = `
      <div class="no-results">
        <div class="no-results-icon">🏠</div>
        <h3>No hostels found</h3>
        <p>Try adjusting your search filters</p>
      </div>
    `;
    return;
  }

  // Create hostel cards
  hostels.forEach((hostel) => {
    const card = document.createElement("div");
    card.className = "hostel-card";
    card.onclick = () => showOnMap(hostel);

    const isAvailable = hostel.current_vacancy > 0;
    const statusClass = isAvailable ? "status-available" : "status-full";
    const statusText = isAvailable
      ? `${hostel.current_vacancy} beds available`
      : "Fully occupied";

    card.innerHTML = `
      <div class="hostel-name">${hostel.name}</div>
      
      <div class="hostel-details">
        <div class="detail-item">
          <span class="detail-icon">👥</span>
          <span>${hostel.mens_or_ladies || "Mixed"}</span>
        </div>
        <div class="detail-item">
          <span class="detail-icon">💰</span>
          <span>₹${
            hostel.average_rent
              ? hostel.average_rent.toLocaleString()
              : "Contact for pricing"
          }</span>
        </div>
        <div class="detail-item">
          <span class="detail-icon">🏠</span>
          <span>${hostel.total_capacity || "N/A"} total beds</span>
        </div>
        <div class="detail-item">
          <span class="detail-icon">📍</span>
          <span>${
            hostel.distance
              ? hostel.distance + "km from CET"
              : "Distance not specified"
          }</span>
        </div>
      </div>

      <div style="margin-top: 1rem;">
        <span class="status-badge ${statusClass}">${statusText}</span>
      </div>

      ${
        hostel.address
          ? `<div style="margin-top: 1rem; color: #6c757d; font-size: 0.9rem;">📍 ${hostel.address}</div>`
          : ""
      }
      
      ${
        hostel.contact_details
          ? `<div style="margin-top: 0.5rem; color: #6c757d; font-size: 0.9rem;">📞 ${hostel.contact_details}</div>`
          : ""
      }
    `;

    hostelsList.appendChild(card);

    // Add map marker
    if (hostel.latitude && hostel.longitude) {
      const marker = L.marker([hostel.latitude, hostel.longitude]).addTo(map);
      marker.bindPopup(`
        <div style="text-align: center;">
          <h5>${hostel.name}</h5>
          <p><strong>Type:</strong> ${hostel.mens_or_ladies || "Mixed"}</p>
          <p><strong>Rent:</strong> ₹${
            hostel.average_rent
              ? hostel.average_rent.toLocaleString()
              : "Contact for pricing"
          }</p>
          <p><strong>Status:</strong> ${statusText}</p>
          ${
            hostel.contact_details
              ? `<p><strong>Contact:</strong> ${hostel.contact_details}</p>`
              : ""
          }
        </div>
      `);
      markers[hostel.id] = marker;
    }
  });
}

// Show hostel on map
function showOnMap(hostel) {
  if (hostel.latitude && hostel.longitude) {
    map.setView([hostel.latitude, hostel.longitude], 18);
    if (markers[hostel.id]) {
      markers[hostel.id].openPopup();
    }
  }
}

// Filter hostels
function filterHostels() {
  const searchInput = document
    .getElementById("searchInput")
    .value.toLowerCase()
    .trim();
  const genderFilter = document.getElementById("genderFilter").value;

  let filteredHostels = myList;

  // Apply search filter
  if (searchInput) {
    filteredHostels = filteredHostels.filter(
      (hostel) =>
        (hostel.name && hostel.name.toLowerCase().includes(searchInput)) ||
        (hostel.address &&
          hostel.address.toLowerCase().includes(searchInput)) ||
        (hostel.owner_name &&
          hostel.owner_name.toLowerCase().includes(searchInput)) ||
        (hostel.mens_or_ladies &&
          hostel.mens_or_ladies.toLowerCase().includes(searchInput)) ||
        (hostel.average_rent &&
          hostel.average_rent.toString().includes(searchInput))
    );
  }

  // Apply gender filter
  if (genderFilter !== "all") {
    filteredHostels = filteredHostels.filter((hostel) => {
      const gender = hostel.mens_or_ladies;
      if (genderFilter === "mens") return gender === "Men";
      if (genderFilter === "ladies") return gender === "Women";
      if (genderFilter === "mixed") return gender === "Mixed";
      return true;
    });
  }

  renderHostels(filteredHostels);
}

// Reset filters
function resetFilters() {
  document.getElementById("searchInput").value = "";
  document.getElementById("genderFilter").value = "all";
  renderHostels(myList);
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", function () {
  if (typeof myList !== "undefined" && myList) {
    renderHostels(myList);
  } else {
    console.log("No hostel data available");
    hostelsList.innerHTML = `
      <div class="no-results">
        <div class="no-results-icon">🏠</div>
        <h3>No hostel data available</h3>
        <p>Please check back later</p>
      </div>
    `;
  }
});
