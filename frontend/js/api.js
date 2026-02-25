const API_BASE_URL = 'http://localhost:5000/api';

async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method,
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Something went wrong');
        }

        return result;
    } catch (error) {
        throw error;
    }
}

// Auth APIs
async function register(hospitalData) {
    return apiRequest('/register', 'POST', hospitalData);
}

async function login(email, password) {
    return apiRequest('/login', 'POST', { email, password });
}

async function logout() {
    return apiRequest('/logout', 'GET');
}

async function checkSession() {
    return apiRequest('/session', 'GET');
}

// Inventory APIs
async function getInventory() {
    return apiRequest('/inventory', 'GET');
}

async function addInventory(inventoryData) {
    return apiRequest('/inventory/add', 'POST', inventoryData);
}

// Search APIs
async function searchOrgans(params) {
    const queryString = new URLSearchParams(params).toString();
    return apiRequest(`/search?${queryString}`, 'GET');
}

// Request APIs
async function createRequest(requestData) {
    return apiRequest('/request/create', 'POST', requestData);
}

async function getIncomingRequests() {
    return apiRequest('/request/incoming', 'GET');
}

async function getOutgoingRequests() {
    return apiRequest('/request/outgoing', 'GET');
}

async function acceptRequest(requestId) {
    return apiRequest(`/request/accept/${requestId}`, 'POST');
}

async function rejectRequest(requestId) {
    return apiRequest(`/request/reject/${requestId}`, 'POST');
}

async function completeRequest(requestId) {
    return apiRequest(`/request/complete/${requestId}`, 'POST');
}