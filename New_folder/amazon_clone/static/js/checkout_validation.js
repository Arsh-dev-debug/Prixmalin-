document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('checkout-form');
    
    if (!form) {
        console.error('Checkout form not found');
        return;
    }
    
    // Get existing message container or create a new one
    let messageContainer = document.getElementById('checkout-message');
    if (!messageContainer) {
        messageContainer = document.createElement('div');
        messageContainer.id = 'checkout-message';
        messageContainer.className = 'alert mt-3';
        messageContainer.style.display = 'none';
        // Insert at the beginning of the form
        form.insertBefore(messageContainer, form.firstChild);
    }
    
    // Validate PIN code (Indian format)
    function isValidZip(zip) {
        return /^\d{6}$/.test(zip);
    }

    // Validate expiration date (MM/YY format)
    function isValidExpiration(exp) {
        if (!/^(0[1-9]|1[0-2])\/([0-9]{2})$/.test(exp)) {
            return false;
        }
        const [month, year] = exp.split('/');
        const expDate = new Date(2000 + parseInt(year), parseInt(month) - 1);
        const today = new Date();
        return expDate > today;
    }

    // Credit card number validation (basic check)
    function isValidCreditCard(ccNum) {
        // Remove spaces and dashes
        ccNum = ccNum.replace(/[\s-]/g, '');
        // Check if it's numeric and has appropriate length (13-19 digits)
        return /^\d{13,19}$/.test(ccNum);
    }
    
    // CVV validation
    function isValidCVV(cvv) {
        return /^\d{3,4}$/.test(cvv);
    }

    // Get form fields
    const zipField = document.getElementById('zip');
    const ccNameField = document.getElementById('cc-name');
    const ccNumberField = document.getElementById('cc-number');
    const expirationField = document.getElementById('cc-expiration');
    const cvvField = document.getElementById('cc-cvv');
    const addressField = document.getElementById('address');
    const cityField = document.getElementById('city');
    
    // Add validation to PIN code field
    if (zipField) {
        zipField.addEventListener('input', function(e) {
            const isValid = isValidZip(e.target.value);
            this.classList.toggle('is-invalid', !isValid && e.target.value.length > 0);
            if (!isValid && e.target.value.length > 0) {
                this.setCustomValidity('Please enter a valid 6-digit PIN code');
            } else {
                this.setCustomValidity('');
            }
        });
    }

    // Add validation to credit card expiration
    if (expirationField) {
        expirationField.addEventListener('input', function(e) {
            // Format as user types (auto-add slash)
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 2) {
                value = value.substring(0, 2) + '/' + value.substring(2, 4);
            }
            e.target.value = value;
            
            const isValid = value.length >= 5 ? isValidExpiration(value) : true;
            this.classList.toggle('is-invalid', !isValid);
            if (!isValid) {
                this.setCustomValidity('Please enter a valid future date in MM/YY format');
            } else {
                this.setCustomValidity('');
            }
        });
    }
    
    // Form submission handler using fetch API instead of native form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Reset all validation states
        const formFields = form.querySelectorAll('input, select');
        formFields.forEach(field => {
            field.classList.remove('is-invalid');
            field.setCustomValidity('');
        });
        
        // Validate required fields
        let isValid = true;
        
        // Required fields validation
        if (addressField && !addressField.value.trim()) {
            addressField.classList.add('is-invalid');
            isValid = false;
        }
        
        if (cityField && !cityField.value.trim()) {
            cityField.classList.add('is-invalid');
            isValid = false;
        }
        
        // Check PIN code
        if (zipField) {
            if (!zipField.value.trim()) {
                zipField.classList.add('is-invalid');
                isValid = false;
            } else if (!isValidZip(zipField.value)) {
                zipField.classList.add('is-invalid');
                isValid = false;
            }
        }
        
        // Check credit card fields
        if (ccNameField && !ccNameField.value.trim()) {
            ccNameField.classList.add('is-invalid');
            isValid = false;
        }
        
        if (ccNumberField) {
            if (!ccNumberField.value.trim()) {
                ccNumberField.classList.add('is-invalid');
                isValid = false;
            } else if (!isValidCreditCard(ccNumberField.value)) {
                ccNumberField.classList.add('is-invalid');
                isValid = false;
            }
        }
        
        if (expirationField) {
            if (!expirationField.value.trim()) {
                expirationField.classList.add('is-invalid');
                isValid = false;
            } else if (!isValidExpiration(expirationField.value)) {
                expirationField.classList.add('is-invalid');
                isValid = false;
            }
        }
        
        if (cvvField) {
            if (!cvvField.value.trim()) {
                cvvField.classList.add('is-invalid');
                isValid = false;
            } else if (!isValidCVV(cvvField.value)) {
                cvvField.classList.add('is-invalid');
                isValid = false;
            }
        }
        
        if (!isValid) {
            // Show error message
            messageContainer.className = 'alert alert-danger mt-3';
            messageContainer.textContent = 'Please correct the errors in the form.';
            messageContainer.style.display = 'block';
            return;
        }
        
        // Show success message
        messageContainer.className = 'alert alert-success mt-3';
        messageContainer.textContent = 'Excitement is on the way!';
        messageContainer.style.display = 'block';
        
        setTimeout(() => {
            // Remove our submit handler to prevent infinite loop
            form.removeEventListener('submit', arguments.callee);
            
            // Allow the form to be submitted normally
            form.submit();
        },10000);
        
    });
});