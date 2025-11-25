var email = document.getElementById('email');
var emailError = document.getElementById('email-error');
var submitBtn = document.getElementById('submit-button');

email.addEventListener('change', ()=> {
    if(email.value) {
        let flag = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value);

        if(!flag) {
            submitBtn.disabled = true;
            emailError.innerHTML = 'Enter a valid email';
        }
        else {
            submitBtn.disabled = false;
            emailError.innerHTML = '';
        }
    }
    else {
        submitBtn.disabled = false;
        emailError.innerHTML = '';
    }
})