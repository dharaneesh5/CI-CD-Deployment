document.addEventListener('DOMContentLoaded', function() {
    loadInventory();
    
    const inventoryForm = document.getElementById('inventoryForm');
    if (inventoryForm) {
        inventoryForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                organ_type: document.getElementById('organ_type').value,
                blood_group: document.getElementById('blood_group').value,
                available_units: parseInt(document.getElementById('available_units').value),
                status: document.getElementById('status').value
            };
            
            try {
                await addInventory(formData);
                document.getElementById('successMessage').style.display = 'block';
                document.getElementById('successMessage').textContent = 'Inventory updated successfully';
                document.getElementById('errorMessage').style.display = 'none';
                
                // Reset form
                inventoryForm.reset();
                
                // Reload inventory list
                loadInventory();
                
                setTimeout(() => {
                    document.getElementById('successMessage').style.display = 'none';
                }, 3000);
            } catch (error) {
                document.getElementById('errorMessage').style.display = 'block';
                document.getElementById('errorMessage').textContent = error.message;
                document.getElementById('successMessage').style.display = 'none';
            }
        });
    }
});

async function loadInventory() {
    try {
        const inventory = await getInventory();
        displayInventory(inventory);
    } catch (error) {
        console.error('Error loading inventory:', error);
    }
}

function displayInventory(inventory) {
    const tbody = document.getElementById('inventoryBody');
    if (!tbody) return;
    
    if (inventory.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No inventory items found</td></tr>';
        return;
    }
    
    tbody.innerHTML = inventory.map(item => `
        <tr>
            <td>${item.organ_type}</td>
            <td>${item.blood_group}</td>
            <td>${item.available_units}</td>
            <td>
                <span class="status-badge ${item.status === 'AVAILABLE' ? 'status-accepted' : 'status-pending'}">
                    ${item.status}
                </span>
            </td>
            <td>${new Date(item.last_updated).toLocaleString()}</td>
            <td>
                <button class="btn btn-small btn-secondary" onclick="editInventory(${item.inventory_id})">Edit</button>
            </td>
        </tr>
    `).join('');
}

function editInventory(inventoryId) {
    // Find the inventory item and populate the form
    // This is a simplified version - in production, you'd fetch the item data
    alert('Edit functionality - would populate form with item data');
}