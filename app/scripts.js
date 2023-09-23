function displayFields() {
    var type = document.getElementById("assetType").value;

    // Hide all fields first (Assuming all can be hidden)
    document.getElementById("ipField").style.display = 'none';
    

    // Show fields based on selection
    if (type === "Server") {
        document.getElementById("ipField").style.display = 'block';
        // ... other related fields ...
    } else if (type === "Phone") {
        // ... handle Phone related fields ...
    }
    // ... other conditions ...
}