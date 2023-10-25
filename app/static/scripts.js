function displayFields() {
    var type = document.getElementById("assetType").value;

    // List of all fields
    var allFields = ["nameField", "ipField", "serialNumberField", "serviceTagField", "locationField"];
    
    // Hide all fields first
    allFields.forEach(function(id) {
        document.getElementById(id).style.display = 'none';
    });

    if (type === "Server") {
        // Fields for the Server type
        var serverFields = ["nameField", "ipField", "serialNumberField", "serviceTagField", "locationField"];
        
        serverFields.forEach(function(id) {
            document.getElementById(id).style.display = 'block';
        });
    }
    
    // ... other conditions for other asset types...
}

document.addEventListener('DOMContentLoaded', function() {
    // Fetch all delete buttons
    const deleteButtons = document.querySelectorAll('.delete-asset-btn');

    // Add event listener to each button
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const assetName = e.target.getAttribute('data-asset-name');
            const assetId = e.target.getAttribute('data-asset-id');
            const companyId = e.target.getAttribute('data-company-id');

            // Confirm deletion
            const isConfirmed = confirm(`Are you sure you want to delete ${assetName}?`);

            if (isConfirmed) {
                // Send a POST request to the delete endpoint
                fetch(`/company/${companyId}/asset/${assetId}/delete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        // Include other necessary headers, such as CSRF tokens if you're using Flask-WTF
                    },
                    // body: JSON.stringify({ 'key': 'value' }) // if you need to send JSON data
                })
                .then(response => response.json()) // assuming server responds with json
                .then(data => {
                    // Handle server response here. Maybe refresh the page to show the asset has been deleted.
                    if (data.success) {
                        location.reload(); // this reloads the page
                    } else {
                        alert('Error deleting the asset.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while deleting the asset.');
                });
            }
        });
    });
});