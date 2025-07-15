// Authentication System
class AuthSystem {
    constructor() {
        this.currentUser = null;
        this.sessionToken = localStorage.getItem('sessionToken');
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkSession();
    }

    setupEventListeners() {
        // Form switching
        document.getElementById('showRegister').addEventListener('click', () => {
            this.switchForm('register');
        });

        document.getElementById('showLogin').addEventListener('click', () => {
            this.switchForm('login');
        });

        // Form submissions
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        document.getElementById('registerForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleRegister();
        });

        // Password visibility toggles
        document.querySelectorAll('.toggle-password').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.togglePasswordVisibility(e.target);
            });
        });

        // Input validation
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('blur', () => {
                this.validateField(input);
            });
        });
    }

    switchForm(formType) {
        const loginForm = document.getElementById('loginForm');
        const registerForm = document.getElementById('registerForm');

        if (formType === 'register') {
            loginForm.classList.remove('active');
            registerForm.classList.add('active');
        } else {
            registerForm.classList.remove('active');
            loginForm.classList.add('active');
        }
    }

    async handleLogin() {
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        if (!this.validateLoginForm()) {
            return;
        }

        const loginBtn = document.querySelector('#loginForm .auth-btn');
        this.setLoadingState(loginBtn, true);

        try {
            const response = await this.loginUser(username, password);
            
            if (response.success) {
                this.showNotification('Login successful! Redirecting...', 'success');
                this.currentUser = response;
                this.sessionToken = response.session_token;
                localStorage.setItem('sessionToken', response.session_token);
                localStorage.setItem('userData', JSON.stringify(response));
                
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1500);
            } else {
                this.showNotification(response.message, 'error');
            }
        } catch (error) {
            this.showNotification('Network error. Please try again.', 'error');
        } finally {
            this.setLoadingState(loginBtn, false);
        }
    }

    async handleRegister() {
        const firstName = document.getElementById('registerFirstName').value;
        const lastName = document.getElementById('registerLastName').value;
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('registerConfirmPassword').value;
        const agreeTerms = document.getElementById('agreeTerms').checked;

        if (!this.validateRegisterForm()) {
            return;
        }

        if (password !== confirmPassword) {
            this.showNotification('Passwords do not match', 'error');
            return;
        }

        if (!agreeTerms) {
            this.showNotification('Please agree to the terms and conditions', 'error');
            return;
        }

        const registerBtn = document.querySelector('#registerForm .auth-btn');
        this.setLoadingState(registerBtn, true);

        try {
            const response = await this.registerUser(firstName, lastName, username, email, password);
            
            if (response.success) {
                this.showNotification('Account created successfully! Please sign in.', 'success');
                this.switchForm('login');
                document.getElementById('loginUsername').value = username;
            } else {
                this.showNotification(response.message, 'error');
            }
        } catch (error) {
            this.showNotification('Network error. Please try again.', 'error');
        } finally {
            this.setLoadingState(registerBtn, false);
        }
    }

    validateLoginForm() {
        const username = document.getElementById('loginUsername');
        const password = document.getElementById('loginPassword');
        
        let isValid = true;

        if (!username.value.trim()) {
            this.showFieldError(username, 'Username is required');
            isValid = false;
        } else {
            this.clearFieldError(username);
        }

        if (!password.value.trim()) {
            this.showFieldError(password, 'Password is required');
            isValid = false;
        } else {
            this.clearFieldError(password);
        }

        return isValid;
    }

    validateRegisterForm() {
        const firstName = document.getElementById('registerFirstName');
        const lastName = document.getElementById('registerLastName');
        const username = document.getElementById('registerUsername');
        const email = document.getElementById('registerEmail');
        const password = document.getElementById('registerPassword');
        const confirmPassword = document.getElementById('registerConfirmPassword');
        
        let isValid = true;

        // First Name
        if (!firstName.value.trim()) {
            this.showFieldError(firstName, 'First name is required');
            isValid = false;
        } else {
            this.clearFieldError(firstName);
        }

        // Last Name
        if (!lastName.value.trim()) {
            this.showFieldError(lastName, 'Last name is required');
            isValid = false;
        } else {
            this.clearFieldError(lastName);
        }

        // Username
        if (!username.value.trim()) {
            this.showFieldError(username, 'Username is required');
            isValid = false;
        } else if (username.value.length < 3) {
            this.showFieldError(username, 'Username must be at least 3 characters');
            isValid = false;
        } else {
            this.clearFieldError(username);
        }

        // Email
        if (!email.value.trim()) {
            this.showFieldError(email, 'Email is required');
            isValid = false;
        } else if (!this.isValidEmail(email.value)) {
            this.showFieldError(email, 'Please enter a valid email');
            isValid = false;
        } else {
            this.clearFieldError(email);
        }

        // Password
        if (!password.value.trim()) {
            this.showFieldError(password, 'Password is required');
            isValid = false;
        } else if (password.value.length < 6) {
            this.showFieldError(password, 'Password must be at least 6 characters');
            isValid = false;
        } else {
            this.clearFieldError(password);
        }

        // Confirm Password
        if (!confirmPassword.value.trim()) {
            this.showFieldError(confirmPassword, 'Please confirm your password');
            isValid = false;
        } else if (password.value !== confirmPassword.value) {
            this.showFieldError(confirmPassword, 'Passwords do not match');
            isValid = false;
        } else {
            this.clearFieldError(confirmPassword);
        }

        return isValid;
    }

    validateField(input) {
        const value = input.value.trim();
        let isValid = true;
        let errorMessage = '';

        switch (input.id) {
            case 'loginUsername':
            case 'registerUsername':
                if (!value) {
                    errorMessage = 'Username is required';
                    isValid = false;
                } else if (value.length < 3) {
                    errorMessage = 'Username must be at least 3 characters';
                    isValid = false;
                }
                break;

            case 'registerEmail':
                if (!value) {
                    errorMessage = 'Email is required';
                    isValid = false;
                } else if (!this.isValidEmail(value)) {
                    errorMessage = 'Please enter a valid email';
                    isValid = false;
                }
                break;

            case 'registerPassword':
            case 'loginPassword':
                if (!value) {
                    errorMessage = 'Password is required';
                    isValid = false;
                } else if (value.length < 6) {
                    errorMessage = 'Password must be at least 6 characters';
                    isValid = false;
                }
                break;

            case 'registerFirstName':
            case 'registerLastName':
                if (!value) {
                    errorMessage = 'This field is required';
                    isValid = false;
                }
                break;
        }

        if (!isValid) {
            this.showFieldError(input, errorMessage);
        } else {
            this.clearFieldError(input);
        }
    }

    showFieldError(input, message) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.add('error');
        inputGroup.classList.remove('success');

        // Remove existing error message
        const existingError = inputGroup.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Add new error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-circle"></i>${message}`;
        inputGroup.parentNode.appendChild(errorDiv);
    }

    clearFieldError(input) {
        const inputGroup = input.closest('.input-group');
        inputGroup.classList.remove('error');
        inputGroup.classList.add('success');

        const errorMessage = inputGroup.parentNode.querySelector('.error-message');
        if (errorMessage) {
            errorMessage.remove();
        }
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    togglePasswordVisibility(button) {
        const input = button.parentNode.querySelector('input');
        const icon = button.querySelector('i');

        if (input.type === 'password') {
            input.type = 'text';
            icon.className = 'fas fa-eye-slash';
        } else {
            input.type = 'password';
            icon.className = 'fas fa-eye';
        }
    }

    setLoadingState(button, loading) {
        if (loading) {
            button.classList.add('loading');
            button.disabled = true;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
        }
    }

    async loginUser(username, password) {
        // Simulate API call - replace with actual backend endpoint
        return new Promise((resolve) => {
            setTimeout(() => {
                // Mock authentication
                if (username === 'demo' && password === 'password') {
                    resolve({
                        success: true,
                        user_id: 1,
                        username: username,
                        first_name: 'Demo',
                        last_name: 'User',
                        email: 'demo@example.com',
                        session_token: 'demo_session_token_' + Date.now()
                    });
                } else {
                    resolve({
                        success: false,
                        message: 'Invalid username or password'
                    });
                }
            }, 1000);
        });
    }

    async registerUser(firstName, lastName, username, email, password) {
        // Simulate API call - replace with actual backend endpoint
        return new Promise((resolve) => {
            setTimeout(() => {
                // Mock registration
                if (username === 'demo') {
                    resolve({
                        success: false,
                        message: 'Username already exists'
                    });
                } else {
                    resolve({
                        success: true,
                        user_id: Date.now(),
                        message: 'User registered successfully'
                    });
                }
            }, 1000);
        });
    }

    async checkSession() {
        if (this.sessionToken) {
            try {
                const response = await this.validateSession(this.sessionToken);
                if (response.success) {
                    this.currentUser = response;
                    // Redirect to main app if already logged in
                    if (window.location.pathname.includes('auth.html')) {
                        window.location.href = 'index.html';
                    }
                } else {
                    this.logout();
                }
            } catch (error) {
                this.logout();
            }
        }
    }

    async validateSession(token) {
        // Simulate session validation - replace with actual backend endpoint
        return new Promise((resolve) => {
            setTimeout(() => {
                if (token && token.startsWith('demo_session_token_')) {
                    resolve({
                        success: true,
                        user_id: 1,
                        username: 'demo',
                        first_name: 'Demo',
                        last_name: 'User',
                        email: 'demo@example.com'
                    });
                } else {
                    resolve({
                        success: false,
                        message: 'Invalid session'
                    });
                }
            }, 500);
        });
    }

    logout() {
        this.currentUser = null;
        this.sessionToken = null;
        localStorage.removeItem('sessionToken');
        localStorage.removeItem('userData');
        
        if (!window.location.pathname.includes('auth.html')) {
            window.location.href = 'auth.html';
        }
    }

    showNotification(message, type = 'info') {
        const notifications = document.getElementById('notifications');
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        notifications.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    // Public methods for other parts of the app
    getCurrentUser() {
        return this.currentUser;
    }

    isAuthenticated() {
        return this.currentUser !== null;
    }

    getSessionToken() {
        return this.sessionToken;
    }
}

// Initialize authentication system
const auth = new AuthSystem();

// Export for use in other files
window.auth = auth; 
