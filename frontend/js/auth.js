document.addEventListener('DOMContentLoaded', function() {
    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('errorMessage');
            
            try {
                const result = await login(email, password);
                window.location.href = '/dashboard.html';
            } catch (error) {
                errorDiv.style.display = 'block';
                errorDiv.textContent = error.message;
            }
        });
    }

    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Check password match
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm_password').value;
            
            if (password !== confirmPassword) {
                const errorDiv = document.getElementById('errorMessage');
                errorDiv.style.display = 'block';
                errorDiv.textContent = 'Passwords do not match';
                return;
            }
            
            const formData = {
                name: document.getElementById('name').value,
                license_no: document.getElementById('license_no').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                address: document.getElementById('address').value,
                city: document.getElementById('city').value,
                district: document.getElementById('district').value,
                state: document.getElementById('state').value,
                pincode: document.getElementById('pincode').value,
                contact_person_name: document.getElementById('contact_person_name').value,
                contact_person_phone: document.getElementById('contact_person_phone').value,
                password: password
            };
            
            try {
                const result = await register(formData);
                const successDiv = document.getElementById('successMessage');
                successDiv.style.display = 'block';
                successDiv.textContent = 'Registration successful! Redirecting to login...';
                
                setTimeout(() => {
                    window.location.href = '/login.html';
                }, 2000);
            } catch (error) {
                const errorDiv = document.getElementById('errorMessage');
                errorDiv.style.display = 'block';
                errorDiv.textContent = error.message;
            }
        });
    }

    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async function(e) {
            e.preventDefault();
            try {
                await logout();
                window.location.href = '/';
            } catch (error) {
                alert('Error logging out');
            }
        });
    }

    // Check authentication on protected pages
    const protectedPages = ['dashboard.html', 'my-inventory.html', 'search-organs.html', 
                           'outgoing-requests.html', 'incoming-requests.html'];
    const currentPage = window.location.pathname.split('/').pop();
    
    if (protectedPages.includes(currentPage)) {
        checkSession().catch(() => {
            window.location.href = '/login.html';
        });
    }
});