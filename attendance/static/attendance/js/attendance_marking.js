const courses = {
    'Computer Science': {
        'BCA': 'BCA - Bachelor of Computer Application', 
        'MScCS': 'MSc Computer Science with Artificial Intelligence'
    },
    'Commerce': { 
        'BCom': 'BCom - Bachelor of Commerce'
    },
    'History': {
        'BAHistory': 'BA History - Bachelor of Arts in History'
    }
}

// var dataHolder = document.getElementById('data-holder');

var departmentDropdown = document.getElementById('department');
var courseDropdown = document.getElementById('course');
var yearDropdown = document.getElementById('year');

let updateBtn = document.getElementById('updateFilter');

departmentDropdown.addEventListener('change', function() {
    // console.log("Department: " + this.value);
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

courseDropdown.addEventListener('change', ()=> {
    yearDropdown.innerHTML = "";
    handleYear();
})

function handleYear() {
    const n = courseDropdown.value == "MScCS" ? 2: 4;
    for(i=1; i<=n; i++) {
        yearDropdown.innerHTML += `<option value=${i}>${i}</option>`
    }
}
handleYear();