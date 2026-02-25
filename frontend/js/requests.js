document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop();
    
    if (currentPage === 'incoming-requests.html') {
        loadIncomingRequests();
    } else if (currentPage === 'outgoing-requests.html') {
        loadOutgoingRequests();
    }
});

async function loadIncomingRequests() {
    try {
        const requests = await getIncomingRequests();
        displayIncomingRequests(requests);
    } catch (error) {
        console.error('Error loading incoming requests:', error);
    }
}

async function loadOutgoingRequests() {
    try {
        const requests = await getOutgoingRequests();
        displayOutgoingRequests(requests);
    } catch (error) {
        console.error('Error loading outgoing requests:', error);
    }
}

function displayIncomingRequests(requests) {
    const tbody = document.getElementById('requestsBody');
    if (!tbody) return;
    
    if (requests.length === 0) {
        tbody.innerHTML = '<tr><td colspan="10" class="text-center">No incoming requests found</td></tr>';
        return;
    }
    
    tbody.innerHTML = requests.map(request => `
        <tr>
            <td>${request.request_id}</td>
            <td>${request.from_hospital_name}</td>
            <td>${request.city}, ${request.state}</td>
            <td>${request.organ_type}</td>
            <td>${request.blood_group}</td>
            <td>${request.quantity_requested}</td>
            <td>
                <span class="status-badge ${getUrgencyClass(request.urgency_level)}">
                    ${request.urgency_level}
                </span>
            </td>
            <td>
                <span class="status-badge ${getStatusClass(request.status)}">
                    ${request.status}
                </span>
            </td>
            <td>${new Date(request.requested_at).toLocaleString()}</td>
            <td>
                ${request.status === 'PENDING' ? `
                    <button class="btn btn-small btn-success" onclick="handleAccept(${request.request_id})">Accept</button>
                    <button class="btn btn-small btn-danger" onclick="handleReject(${request.request_id})">Reject</button>
                ` : ''}
            </td>
        </tr>
    `).join('');
}

function displayOutgoingRequests(requests) {
    const tbody = document.getElementById('requestsBody');
    if (!tbody) return;
    
    if (requests.length === 0) {
        tbody.innerHTML = '<tr><td colspan="11" class="text-center">No outgoing requests found</td></tr>';
        return;
    }
    
    tbody.innerHTML = requests.map(request => {
        let contactDetails = 'Hidden until accepted';
        if (request.status === 'ACCEPTED' && request.phone) {
            contactDetails = `
                <strong>Phone:</strong> ${request.phone}<br>
                <strong>Email:</strong> ${request.email}<br>
                <strong>Contact Person:</strong> ${request.contact_person_name} (${request.contact_person_phone})
            `;
        }
        
        return `
        <tr>
            <td>${request.request_id}</td>
            <td>${request.to_hospital_name}</td>
            <td>${request.city}, ${request.state}</td>
            <td>${request.organ_type}</td>
            <td>${request.blood_group}</td>
            <td>${request.quantity_requested}</td>
            <td>
                <span class="status-badge ${getUrgencyClass(request.urgency_level)}">
                    ${request.urgency_level}
                </span>
            </td>
            <td>
                <span class="status-badge ${getStatusClass(request.status)}">
                    ${request.status}
                </span>
            </td>
            <td>${new Date(request.requested_at).toLocaleString()}</td>
            <td>${contactDetails}</td>
            <td>
                ${request.status === 'ACCEPTED' ? `
                    <button class="btn btn-small btn-success" onclick="handleComplete(${request.request_id})">Mark Completed</button>
                ` : ''}
            </td>
        </tr>
    `}).join('');
}

function getUrgencyClass(urgency) {
    switch(urgency) {
        case 'HIGH': return 'status-danger';
        case 'MEDIUM': return 'status-warning';
        case 'LOW': return 'status-info';
        default: return '';
    }
}

function getStatusClass(status) {
    switch(status) {
        case 'PENDING': return 'status-pending';
        case 'ACCEPTED': return 'status-accepted';
        case 'REJECTED': return 'status-rejected';
        case 'COMPLETED': return 'status-completed';
        default: return '';
    }
}

async function handleAccept(requestId) {
    if (confirm('Accept this request? This will reduce your inventory.')) {
        try {
            await acceptRequest(requestId);
            alert('Request accepted successfully');
            loadIncomingRequests();
        } catch (error) {
            alert('Error accepting request: ' + error.message);
        }
    }
}

async function handleReject(requestId) {
    if (confirm('Reject this request?')) {
        try {
            await rejectRequest(requestId);
            alert('Request rejected successfully');
            loadIncomingRequests();
        } catch (error) {
            alert('Error rejecting request: ' + error.message);
        }
    }
}

async function handleComplete(requestId) {
    if (confirm('Mark this request as completed?')) {
        try {
            await completeRequest(requestId);
            alert('Request completed successfully');
            loadOutgoingRequests();
        } catch (error) {
            alert('Error completing request: ' + error.message);
        }
    }
}