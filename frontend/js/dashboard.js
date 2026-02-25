document.addEventListener('DOMContentLoaded', async function() {
    try {
        const session = await checkSession();
        document.getElementById('hospitalName').textContent = session.hospital_name;
        
        // Load dashboard stats
        loadDashboardStats();
    } catch (error) {
        window.location.href = '/login.html';
    }
});

async function loadDashboardStats() {
    try {
        // Load inventory count
        const inventory = await getInventory();
        document.getElementById('inventoryCount').textContent = inventory.length;
        
        // Load incoming requests count
        const incoming = await getIncomingRequests();
        document.getElementById('incomingCount').textContent = incoming.length;
        
        // Load outgoing requests count
        const outgoing = await getOutgoingRequests();
        document.getElementById('outgoingCount').textContent = outgoing.length;
    } catch (error) {
        console.error('Error loading dashboard stats:', error);
    }
}