// Fetch district and soil color options dynamically from the server
window.onload = function() {
    fetch('/getDistricts')
        .then(response => response.json())
        .then(data => {
            let districtSelect = document.getElementById('district');
            data.districts.forEach(district => {
                let option = document.createElement('option');
                option.value = district;
                option.text = district;
                districtSelect.appendChild(option);
            });
        });

    document.getElementById('district').onchange = function() {
        let district = this.value;
        fetch(`/getSoilColors?district=${district}`)
            .then(response => response.json())
            .then(data => {
                let soilColorSelect = document.getElementById('soilColor');
                soilColorSelect.innerHTML = ''; // Clear previous options
                data.soilColors.forEach(color => {
                    let option = document.createElement('option');
                    option.value = color;
                    option.text = color;
                    soilColorSelect.appendChild(option);
                });
            });
    }
}

// Function to send data to the Flask backend for crop recommendation
function recommendCrop() {
    let district = document.getElementById('district').value;
    let soilColor = document.getElementById('soilColor').value;
    let nitrogen = document.getElementById('nitrogen').value;
    let phosphorus = document.getElementById('phosphorus').value;
    let potassium = document.getElementById('potassium').value;
    let ph = document.getElementById('ph').value;
    let rainfall = document.getElementById('rainfall').value;
    let temperature = document.getElementById('temperature').value;

    let data = {
        district: district,
        soilColor: soilColor,
        nitrogen: nitrogen,
        phosphorus: phosphorus,
        potassium: potassium,
        ph: ph,
        rainfall: rainfall,
        temperature: temperature
    };

    fetch('/recommendCrop', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById('recommendedCrop').innerText = result.crop;
        document.getElementById('recommendedFertilizer').innerText = result.fertilizer;
    });
}
