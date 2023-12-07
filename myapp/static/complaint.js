
var jsonData = myList
console.log(jsonData)
var jsonData1 = [
    {

        "name": "Aswin",
        "hostel": "Ideal",
        "phone": "123-456-7890",
        "complaint": `There's a consistent issue with hot water in the showers. It's frustrating to have
        cold showers,
        especially during the winter months.`,
        "status": "Pending"
    },
    {

        "name": "Aswin",
        "hostel": "Ideal",
        "phone": "123-456-7890",
        "complaint": `There's a consistent issue with hot water in the showers. It's frustrating to have
        cold showers,
        especially during the winter months.`,
        "status": "Pending"
    },
    {

        "name": "Aswin",
        "hostel": "Ideal",
        "phone": "123-456-7890",
        "complaint": `There's a consistent issue with hot water in the showers. It's frustrating to have
        cold showers,
        especially during the winter months.`,
        "status": "Pending"
    },
    {

        "name": "Aswin",
        "hostel": "Ideal",
        "phone": "123-456-7890",
        "complaint": `There's a consistent issue with hot water in the showers. It's frustrating to have
        cold showers,
        especially during the winter months.`,
        "status": "Resolved"
    },

    {

        "name": "Aswin12",
        "hostel": "Ideal",
        "phone": "123-456-7890",
        "complaint": `There's a consistent issue with hot water in the showers. It's frustrating to have
        cold showers,
        especially during the winter months.`,
        "status": "Resolved"
    }

]


var cardContainer = document.getElementById('box');

function renderComplaints(complaints) {
    cardContainer.innerHTML = '';

    complaints.forEach(data => {
        var lists = document.createElement('div');
        lists.className = 'list';

        lists.innerHTML = `
        
        <div class="host-name" >
            <h1>${data.full_name}</h1>
            <h5>Hostel : ${data.hostel}</h5>
            <h5 class="status-text" >Status:${data.complaint_status}</h5>
            <h5>${data.phone}</h5>
        </div>
        <div class="description" style="display: none;">
        <p >${data.complaint_text}</p>
        </div>
        `;
        cardContainer.appendChild(lists);

        lists.addEventListener('click', (event) => {

            const description = lists.querySelector('.description');
           
            if (description.style.display === 'none' || description.style.display === '') {
                description.style.display = 'block';
                lists.style.height = '15.5rem';

            } else {
                description.style.display = 'none';
                lists.style.height = '12rem';
            }
            
            event.stopPropagation();
        });
        const statusText = lists.querySelector('.status-text');
        const status = data.complaint_status.trim().toLowerCase();

            if (status === 'resolved') {
                statusText.style.color = 'green';
            } else if (status === 'pending') {
                statusText.style.color = 'red';
            } else {
                statusText.style.color = 'black'; // Default color or any other color you prefer
            }

            
            // //////////////////////////////
            statusText.addEventListener('click', () => {
                // Assuming you have a URL to redirect to
                const redirectUrl = `admin_status/url?id=${data.id}`; 
                // Log the redirectUrl to the console for verification
                // console.log(redirectUrl);
                // Uncomment the line below to actually redirect the user
                window.location.href = redirectUrl;
            });
            
        });

    // //////////////////////////////
}


renderComplaints(jsonData);

