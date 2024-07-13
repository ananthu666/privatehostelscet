console.log("hello_world");
console.log(myHostelApprovals);

var cardContainer = document.getElementById('box');

function renderHostels(hostels) {
    cardContainer.innerHTML = '';

    hostels.forEach(data => {
        console.log(data); // Log each hostel data to ensure iteration

        var lists = document.createElement('div');
        lists.className = 'list';

 
        lists.innerHTML = `
            <div class="host-name">
                <h1>${data.name}</h1>
                 <h5>Hostel: ${data.name}</h5>
                 <h5>Owner: ${data.owner_name}</h5>
                 <h5>Contact: ${data.contact_details}</h5>
                 <h5>Vacancy: ${data.current_vacancy}</h5>
                 <h5>Gender: ${data.mens_or_ladies}</h5>
                 <h5>Rent: ${data.average_rent}</h5>
                 <h5>Type: ${data.accommodation_type}</h5>
                 <h5>Curfew: ${data.curfew}</h5>
                 <h5>Longitude: ${data.longitude}</h5>
                 <h5>Latitude: ${data.latitude}</h5                 
                 <h5>Mess: ${data.mess}</h5>
                 <h5>Distance: ${data.distance}</h5>
                 <h5 class="hostel_status-text" >Status:${data.approval_hostel_status}</h5>
            </div>
        `;
        cardContainer.insertBefore(lists, cardContainer.firstChild);       
        
        const hostelstatusText = lists.querySelector('.hostel_status-text');
        const status = data.approval_hostel_status.trim().toLowerCase();

            if (status === 'approved') {
                hostelstatusText.style.color = 'green';
            } else if (status === 'pending') {
                hostelstatusText.style.color = 'red';
            } else {
                hostelstatusText.style.color = 'black'; // Default color or any other color you prefer
            }

            hostelstatusText.style.cursor = 'pointer';
            // //////////////////////////////
            hostelstatusText.addEventListener('click', () => {
                // Assuming you have a URL to redirect to
                const redirectUrl = `hostel_status/url?id=${data.id}`; // Change this to your actual redirect URL
                // Log the redirectUrl to the console for verification
                // console.log(redirectUrl);
                // Uncomment the line below to actually redirect the user
                window.location.href = redirectUrl;
            });
        });

        
    
}

renderHostels(myHostelApprovals);

// -----------------------------------------------------------------------------------------------------------------------------
         // first trial  dint work but for code!!

// var jsonData = myHostelApprovals;
// console.log("hello_world");
// console.log(jsonData)
// var jsonData1 = [
//     {
//         id: 1,
//         "name": "Hostel A",
//         "owner_name": "John Doe",
//         "contact_details": "123-456-7890",
//         "current_vacancy": 5,
//         "mens_or_ladies": "Ladies",
//         "average_rent": 500,
//         "accommodation_type": "hostel",
//         "curfew": '10:00' ,
//         "longitude": -73.9857,
//         "latitude": 40.7484,
//         "mess": "Available",
//         "distance": 1 
//     },
//     {
//         id: 2,
//         "name": "Hostel B",
//         "owner_name": "Jane Smith",
//         "contact_details": "987-654-3210",
//         "current_vacancy": 3,
//         "mens_or_ladies": "Mens",
//         "average_rent": 450,
//         "accommodation_type": "hostel",
//         "curfew": '11:00' ,
//         "longitude": -74.0059,
//         "latitude": 40.7128,
//         "mess": "Not available",
//         "distance": 2
//     }
//     // Add more hostel objects as needed
// ];

// var cardContainer = document.getElementById('box');

// function renderHostels(hostels) {
//     cardContainer.innerHTML = '';

//     hostels.forEach(data => {
//         var lists = document.createElement('div');
//         lists.className = 'list';

//         var curfewParts = data.curfew.split(':');
//         var curfewDate = new Date();
//         curfewDate.setHours(curfewParts[0]);
//         curfewDate.setMinutes(curfewParts[1]);

//         lists.innerHTML = `
//             <div class="host-name">
//                 <h1>${data.name}</h1>
//                 <h5>Hostel: ${data.name}</h5>
//                 <h5>Owner: ${data.owner_name}</h5>
//                 <h5>Contact: ${data.contact_details}</h5>
//                 <h5>Vacancy: ${data.current_vacancy}</h5>
//                 <h5>Gender: ${data.mens_or_ladies}</h5>
//                 <h5>Rent: ${data.average_rent}</h5>
//                 <h5>Type: ${data.accommodation_type}</h5>
//                 <h5>Curfew: ${data.curfew}</h5>
//                 <h5>Longitude: ${data.longitude}</h5>
//                 <h5>Latitude: ${data.latitude}</h5>
//                 <h5>Mess: ${data.mess}</h5>
//                 <h5>Distance: ${data.distance}</h5>
//             </div>
//         `;
//         cardContainer.appendChild(lists);

//         lists.addEventListener('click', (event) => {
//             const description = lists.querySelector('.description');
           
//             if (description.style.display === 'none' || description.style.display === '') {
//                 description.style.display = 'block';
//                 lists.style.height = '15.5rem';
//             } else {
//                 description.style.display = 'none';
//                 lists.style.height = '12rem';
//             }
            
//             event.stopPropagation();
//         });

//         const statusText = lists.querySelector('.status-text');
//         const status = data.approval_status.trim().toLowerCase(); 

//         if (status === 'approved') {
//             statusText.style.color = 'green';
//         } else if (status === 'pending') {
//             statusText.style.color = 'red';
//         } else {
//             statusText.style.color = 'black'; // Default color or any other color you prefer
//         }

//         statusText.style.cursor = 'pointer';
        
//         statusText.addEventListener('click', () => {
//             // Assuming you have a URL to redirect to
//             const redirectUrl = `status/url?id=${data.id}`; // Change this to your actual redirect URL
//             // Uncomment the line below to actually redirect the user
//             // window.location.href = redirectUrl;
//         });
//     });
// }

// renderHostels(jsonData);


    
