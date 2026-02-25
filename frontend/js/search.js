document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const params = {
                organ_type: document.getElementById('organ_type').value,
                blood_group: document.getElementById('blood_group').value,
                city: document.getElementById('city').value,
                district: document.getElementById('district').value,
                state: document.getElementById('state').value
            };
            
            // Remove empty params
            Object.keys(params).forEach(key => {
                if (!params[key]) delete params[key];
            });
            
            try {
                const results = await searchOrgans(params);
                displaySearchResults(results);
            } catch (error) {
                alert('Error searching: ' + error.message);
            }
        });
    }
    
    // Setup modal close
    const modal = document.getElementById('requestModal');
    const span = document.getElementsByClassName('close')[0];
    
    if (span) {
        span.onclick = function() {
            modal.style.display = 'none';
        }
    }
    
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
    
    // Request form submission
    const requestForm = document.getElementById('requestForm');
    if (requestForm) {
        requestForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const requestData = {
                to_hospital_id: document.getElementById('to_hospital_id').value,
                organ_type: document.getElementById('organ_type_req').value,
                blood_group: document.getElementById('blood_group_req').value,
                quantity_requested: parseInt(document.getElementById('quantity_requested').value),
                urgency_level: document.getElementById('urgency_level').value
            };
            
            try {
                await createRequest(requestData);
                alert('Request sent successfully!');
                document.getElementById('requestModal').style.display = 'none';
                requestForm.reset();
            } catch (error) {
                document.getElementById('modalError').style.display = 'block';
                document.getElementById('modalError').textContent = error.message;
            }
        });
    }
});

function displaySearchResults(results) {
    const container = document.getElementById('resultsContainer');
    
    if (results.length === 0) {
        container.innerHTML = '<p class="text-center">No organs found matching your criteria.</p>';
        return;
    }
    
    container.innerHTML = results.map(result => `
        <div class="result-card">
            <div class="result-header">
                <h4>${result.name}</h4>
                <span class="status-badge status-accepted">${result.available_units} units available</span>
            </div>
            <div class="result-details">
                <p><strong>Location:</strong> ${result.city}, ${result.state}</p>
                <p><strong>Organ:</strong> ${result.organ_type} (${result.blood_group})</p>
                <p><strong>Last Updated:</strong> ${new Date(result.last_updated).toLocaleString()}</p>
            </div>
            <button class="btn btn-primary btn-small" onclick="openRequestModal(${result.hospital_id}, '${result.organ_type}', '${result.blood_group}', '${result.name}')">
                Request Organ
            </button>
        </div>
    `).join('');
}

function openRequestModal(hospitalId, organType, bloodGroup, hospitalName) {
    document.getElementById('to_hospital_id').value = hospitalId;
    document.getElementById('organ_type_req').value = organType;
    document.getElementById('blood_group_req').value = bloodGroup;
    document.getElementById('hospitalNameDisplay').textContent = hospitalName;
    document.getElementById('organDisplay').textContent = `${organType} (${bloodGroup})`;
    document.getElementById('modalError').style.display = 'none';
    document.getElementById('requestModal').style.display = 'block';
}