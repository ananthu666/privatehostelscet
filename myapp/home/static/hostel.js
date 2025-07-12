console.log("🏠 Hostel App Loaded!");

// Initialize the Leaflet map
L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  subdomains: "abcd",
  maxZoom: 20,
}).addTo(map);

// CET Marker
const cetMarker = L.marker([8.54311, 76.90335]).addTo(map);
cetMarker.bindPopup(
  "<div class='custom-popup'><h4>🏛️ CET Campus</h4><p>College of Engineering Trivandrum</p></div>"
);

const cardContainer = document.getElementById("right");
const markers = {}; // Store map markers

// Show loading
function showLoading() {
  cardContainer.innerHTML = `
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <p>Finding amazing hostels for you...</p>
    </div>
  `;
}

// Render hostels
function renderHostels(list) {
  cardContainer.innerHTML = "";
  list.forEach((data) => {
    const card = document.createElement("div");
    card.classList.add("hostel-card-modern");

    let genderIcon = "🏠";
    let genderText = "Mixed";
    let genderBadgeClass = "badge-mixed";

    if (data.mens_or_ladies === "Men") {
      genderIcon = "👨";
      genderText = "Men's Hostel";
      genderBadgeClass = "badge-men";
    } else if (data.mens_or_ladies === "Women") {
      genderIcon = "👩";
      genderText = "Ladies Hostel";
      genderBadgeClass = "badge-women";
    }

    const vacancy = data.current_vacancy || 0;
    const vacancyClass = vacancy > 0 ? "vacancy-available" : "vacancy-full";
    const vacancyIcon = vacancy > 0 ? "✅" : "❌";
    const vacancyText = vacancy > 0 ? `${vacancy} beds available` : "Full";

    const rating = data.rating || "N/A";
    const stars = "⭐".repeat(Math.round(parseFloat(rating)));

    const rentText = data.average_rent
      ? `₹${data.average_rent}/mo`
      : "Contact for price";
    const distanceText = data.distance || "Nearby";

    const amenities = [];
    if (data.mess === "Yes" || data.mess === true) amenities.push("🍽️ Mess");
    if (data.curfew && data.curfew !== "No Curfew") amenities.push("🕐 Curfew");
    if (data.current_vacancy > 0) amenities.push("🛏️ Available");

    // Card inner HTML
    card.innerHTML = `
      <div class="card-ribbon ${genderBadgeClass}">
        ${genderIcon} ${genderText}
      </div>
      <div class="card-header-modern">
        <div class="hostel-image-container">
          <img src="/static/assets/hostel.jpg" alt="${
            data.name
          }" class="hostel-image-modern" />
          <div class="image-overlay">
            <div class="price-tag">${rentText}</div>
            <div class="rating-badge">${stars} ${rating}</div>
          </div>
        </div>
      </div>
      <div class="card-content-modern">
        <div class="hostel-header">
          <h3 class="hostel-title">${data.name}</h3>
          <div class="vacancy-status ${vacancyClass}">
            ${vacancyIcon} ${vacancyText}
          </div>
        </div>
        <div class="hostel-info-grid">
          <div class="info-tile">
            <div class="info-icon">📍</div>
            <div class="info-content">
              <span class="info-label">Location</span>
              <span class="info-value">${distanceText}</span>
            </div>
          </div>
          <div class="info-tile">
            <div class="info-icon">👥</div>
            <div class="info-content">
              <span class="info-label">Capacity</span>
              <span class="info-value">${
                data.total_capacity || "N/A"
              } beds</span>
            </div>
          </div>
          <div class="info-tile">
            <div class="info-icon">🏠</div>
            <div class="info-content">
              <span class="info-label">Type</span>
              <span class="info-value">${
                data.accommodation_type || "Standard"
              }</span>
            </div>
          </div>
        </div>
        <div class="amenities-row">
          ${amenities
            .map((amenity) => `<span class="amenity-tag">${amenity}</span>`)
            .join("")}
        </div>
        <div class="card-details-section" style="display: none;">
          <div class="detail-grid">
            <div class="detail-item"><strong>📍 Full Address:</strong><p>${
              data.address || "Contact for address details"
            }</p></div>
            <div class="detail-item"><strong>👤 Owner:</strong><p>${
              data.owner_name || "Information available on contact"
            }</p></div>
            <div class="detail-item"><strong>📞 Contact:</strong><p>${
              data.contact_details || "Contact details available on inquiry"
            }</p></div>
            <div class="detail-item"><strong>⏰ Timings:</strong><p>Curfew: ${
              data.curfew || "No specific curfew"
            }</p></div>
          </div>
        </div>
        <div class="card-actions-modern">
          <button class="btn-modern btn-details" onclick="toggleDetails(this)">
            <span class="btn-icon">📋</span>
            <span class="btn-text">View Details</span>
          </button>
          <button class="btn-modern btn-location" onclick="showOnMap(${
            data.latitude
          }, ${data.longitude}, '${data.name}')">
            <span class="btn-icon">🗺️</span>
            <span class="btn-text">Show on Map</span>
          </button>
          <button class="btn-modern btn-contact" onclick="contactHostel('${
            data.contact_details
          }', '${data.name}')">
            <span class="btn-icon">📞</span>
            <span class="btn-text">Contact</span>
          </button>
        </div>
      </div>
    `;

    cardContainer.appendChild(card);

    // Add map marker
    markers[data.id] = L.marker([data.latitude, data.longitude]).addTo(map);
    markers[data.id].bindPopup(`
      <div class="map-popup-modern">
        <h4>🏠 ${data.name}</h4>
        <div class="popup-info">
          <p><strong>Type:</strong> ${genderIcon} ${genderText}</p>
          <p><strong>Availability:</strong> ${vacancyIcon} ${vacancyText}</p>
          <p><strong>Rent:</strong> 💰 ${rentText}</p>
          <p><strong>Rating:</strong> ${stars} ${rating}</p>
        </div>
        <button class="popup-btn" onclick="contactHostel('${data.contact_details}', '${data.name}')">
          Contact Now
        </button>
      </div>
    `);
  });
}

// Show/hide extra hostel info
function toggleDetails(button) {
  const card = button.closest(".hostel-card-modern");
  const detailsSection = card.querySelector(".card-details-section");
  const isHidden = detailsSection.style.display === "none";

  detailsSection.style.display = isHidden ? "block" : "none";
  button.querySelector(".btn-text").textContent = isHidden
    ? "Hide Details"
    : "View Details";
}

// Move map to marker
function showOnMap(lat, lng, name) {
  map.setView([lat, lng], 18);
  Object.values(markers).forEach((marker) => {
    if (marker.getLatLng().lat === lat && marker.getLatLng().lng === lng) {
      marker.openPopup();
    }
  });
  document
    .querySelector(".map-section")
    .scrollIntoView({ behavior: "smooth", block: "center" });
}

// Trigger call or alert for contact
function contactHostel(contact, name) {
  if (
    contact &&
    contact !== "Contact not available" &&
    contact !== "Contact details available on inquiry"
  ) {
    const phoneRegex = /[\d\s\-\+\(\)]{10,}/;
    if (phoneRegex.test(contact)) {
      window.open(`tel:${contact.replace(/[^\d]/g, "")}`, "_self");
    } else {
      alert(`Contact ${name}:\n${contact}`);
    }
  } else {
    alert(
      `Contact information for ${name} is not available. Please visit the hostel directly.`
    );
  }
}

// Reset filters
function resetFilters() {
  document.getElementById("searchInput").value = "";
  document.getElementById("genderFilter").value = "all";
  renderHostels(myList);
}

// Text search + gender filter
function filterHostels() {
  const searchInput = document
    .getElementById("searchInput")
    .value.toLowerCase()
    .trim();
  const genderFilter = document.getElementById("genderFilter").value || "all";

  let filteredHostels = myList;

  if (searchInput) {
    filteredHostels = filteredHostels.filter(
      (hostel) =>
        hostel.name.toLowerCase().includes(searchInput) ||
        hostel.address.toLowerCase().includes(searchInput) ||
        hostel.owner_name.toLowerCase().includes(searchInput) ||
        hostel.mens_or_ladies.toLowerCase().includes(searchInput) ||
        hostel.average_rent.toString().includes(searchInput)
    );
  }

  if (genderFilter !== "all") {
    filteredHostels = filteredHostels.filter((hostel) => {
      if (genderFilter === "mens") return hostel.mens_or_ladies === "Men";
      if (genderFilter === "ladies") return hostel.mens_or_ladies === "Women";
      if (genderFilter === "mixed") return hostel.mens_or_ladies === "Mixed";
      return true;
    });
  }

  renderHostels(filteredHostels);
}

function clearSearch() {
  document.getElementById("searchInput").value = "";
  document.getElementById("genderFilter").value = "all";
  renderHostels(myList);
}

// Legacy alias
function searchHostels() {
  filterHostels();
}

// Initial load
renderHostels(myList);
