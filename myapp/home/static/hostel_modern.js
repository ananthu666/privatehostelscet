console.log("🏠 Modern Hostel App Loaded!");
console.log("Hostel data loaded:", myList);

const markers = {};
const map = L.map("map");
map.setView([8.5445, 76.9041], 15);

// Modern dark map theme
L.tileLayer("https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png", {
  attribution: "© OpenStreetMap contributors © CARTO",
  subdomains: "abcd",
  maxZoom: 20,
}).addTo(map);

// CET Campus marker
var cetMarker = L.marker([8.54311, 76.90335]).addTo(map);
cetMarker.bindPopup(
  "<div class='custom-popup'><h4>🏛️ CET Campus</h4><p>College of Engineering Trivandrum</p></div>"
);

var cardContainer = document.getElementById("right");

function renderHostels(hostels) {
  cardContainer.innerHTML = "";

  // Clear existing markers
  Object.keys(markers).forEach((key) => {
    if (markers[key]) {
      map.removeLayer(markers[key]);
      delete markers[key];
    }
  });

  if (hostels.length === 0) {
    cardContainer.innerHTML = `
      <div class="no-results">
        <div class="no-results-icon">🏠</div>
        <h3>No hostels found</h3>
        <p>Try adjusting your search filters</p>
        <button class="btn-reset" onclick="resetFilters()">Reset Filters</button>
      </div>
    `;
    return;
  }

  // Stats header
  const availableHostels = hostels.filter((h) => h.current_vacancy > 0).length;
  const minRent = Math.min(...hostels.map((h) => h.average_rent || 0));

  const statsDiv = document.createElement("div");
  statsDiv.className = "results-stats";
  statsDiv.innerHTML = `
    <div class="stats-item">
      <span class="stats-number">${hostels.length}</span>
      <span class="stats-label">Hostels Found</span>
    </div>
    <div class="stats-item">
      <span class="stats-number">${availableHostels}</span>
      <span class="stats-label">Available</span>
    </div>
    <div class="stats-item">
      <span class="stats-number">₹${minRent.toLocaleString()}</span>
      <span class="stats-label">Starting From</span>
    </div>
  `;
  cardContainer.appendChild(statsDiv);

  hostels.forEach((data, index) => {
    const card = document.createElement("div");
    card.className = "hostel-card-modern";
    card.style.animationDelay = `${index * 0.1}s`;

    // Status and gender styling
    const isAvailable = data.current_vacancy > 0;
    const vacancyClass = isAvailable ? "available" : "full";
    const vacancyIcon = isAvailable ? "🟢" : "🔴";
    const vacancyText = isAvailable
      ? `${data.current_vacancy} beds available`
      : "Fully occupied";

    let genderClass = "mixed";
    let genderIcon = "👥";
    let genderText = "Mixed";

    if (data.mens_or_ladies === "Men") {
      genderClass = "mens";
      genderIcon = "👨‍🎓";
      genderText = "Men's Hostel";
    } else if (data.mens_or_ladies === "Women") {
      genderClass = "ladies";
      genderIcon = "👩‍🎓";
      genderText = "Women's Hostel";
    }

    // Formatting
    const rating = (4.0 + Math.random()).toFixed(1);
    const stars = "⭐".repeat(Math.floor(rating));
    const rentText = data.average_rent
      ? `₹${data.average_rent.toLocaleString()}/month`
      : "Contact for pricing";
    const distanceText = data.distance
      ? `${data.distance}km from CET`
      : "Distance not specified";

    // Amenities
    const amenities = [];
    if (data.mess === "Yes") amenities.push("🍽️ Mess");
    if (data.curfew && data.curfew !== "No Curfew") amenities.push("🕐 Curfew");
    if (isAvailable) amenities.push("🛏️ Available");

    card.innerHTML = `
      <div class="card-ribbon ${genderClass}">
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
            <div class="detail-item">
              <strong>📍 Address:</strong>
              <p>${data.address || "Contact for address"}</p>
            </div>
            <div class="detail-item">
              <strong>👤 Owner:</strong>
              <p>${data.owner_name || "Contact for details"}</p>
            </div>
            <div class="detail-item">
              <strong>📞 Contact:</strong>
              <p>${data.contact_details || "Contact available on inquiry"}</p>
            </div>
            <div class="detail-item">
              <strong>⏰ Curfew:</strong>
              <p>${data.curfew || "No specific curfew"}</p>
            </div>
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
          <p><strong>Vacancy:</strong> ${vacancyIcon} ${vacancyText}</p>
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

// Helper functions
function toggleDetails(button) {
  const card = button.closest(".hostel-card-modern");
  const detailsSection = card.querySelector(".card-details-section");
  const isHidden = detailsSection.style.display === "none";

  detailsSection.style.display = isHidden ? "block" : "none";
  button.querySelector(".btn-text").textContent = isHidden
    ? "Hide Details"
    : "View Details";
}

function showOnMap(lat, lng, name) {
  map.setView([lat, lng], 18);
  Object.values(markers).forEach((marker) => {
    if (
      Math.abs(marker.getLatLng().lat - lat) < 0.0001 &&
      Math.abs(marker.getLatLng().lng - lng) < 0.0001
    ) {
      marker.openPopup();
    }
  });

  document.querySelector(".map-section").scrollIntoView({
    behavior: "smooth",
    block: "center",
  });
}

function contactHostel(contact, name) {
  if (
    contact &&
    contact !== "Contact not available" &&
    contact !== "Contact available on inquiry"
  ) {
    if (/[\d\s\-\+\(\)]{10,}/.test(contact)) {
      window.open(`tel:${contact.replace(/[^\d]/g, "")}`, "_self");
    } else {
      alert(`Contact ${name}:\n${contact}`);
    }
  } else {
    alert(
      `Contact information for ${name} will be provided on inquiry. Please visit the hostel for details.`
    );
  }
}

function resetFilters() {
  document.getElementById("searchInput").value = "";
  document.getElementById("genderFilter").value = "all";
  renderHostels(myList);
}

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
        hostel.name.toLowerCase().includes(searchInput) ||
        hostel.address.toLowerCase().includes(searchInput) ||
        hostel.owner_name.toLowerCase().includes(searchInput) ||
        hostel.mens_or_ladies.toLowerCase().includes(searchInput) ||
        hostel.average_rent.toString().includes(searchInput)
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

function clearSearch() {
  resetFilters();
}

// Initialize
renderHostels(myList);
