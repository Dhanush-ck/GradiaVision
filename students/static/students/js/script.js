const courses = {
    'Computer Science': {
        'BCA': 'BCA - Bachelor of Computer Application', 
        'MSc CS': 'MSc Computer Science with Artificial Intelligence'
    },
    'Commerce': { 
        'BCom': 'BCom - Bachelor of Commerce'
    },
    'History': {
        'BA History': 'BA History - Bachelor of Arts in History'
    }
}

var departmentDropdown = document.getElementById('department');
var courseDropdown = document.getElementById('course');
var semester = document.getElementById('semester');
var password = document.getElementById('password');
var email = document.getElementById('email');
var confirmPassword = document.getElementById('confirm-password');
var signUpForm = document.getElementById('signUpForm');
var submitBtn = document.getElementById('submit-button');

var semesterError = document.getElementById('semester-error');
var passwordError = document.getElementById('password-error');
var emailError = document.getElementById('email-error');

departmentDropdown.addEventListener('change', function() {
    console.log("Department: " + this.value);
    handleCourse();
})

const handleCourse = ()=> {
    courseDropdown.innerHTML = "";
    const currentCourse = courses[departmentDropdown.value];
    for(i in currentCourse) {
        courseDropdown.innerHTML += `<option value='${i}'> ${currentCourse[i]} </option>`;
        // console.log(`<option value='${i}'> ${currentCourse[i]} <option>`);
    }
}
handleCourse();

semester.addEventListener('change', ()=> {
    const val = semester.value;
    if(val) {
        if(val < 1 || val > 8 ) {
            semesterError.innerHTML = 'Enter a valid semester';
            submitBtn.disabled = true;
        }
        else {
            semesterError.innerHTML = "";
            submitBtn.disabled = false;
        }
    }
    else {
        semesterError.innerHTML = ""; 
        submitBtn.disabled = false;
    }
})

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