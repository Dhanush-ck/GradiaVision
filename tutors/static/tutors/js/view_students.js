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

var departmentDropdown = document.getElementById('department');
var courseDropdown = document.getElementById('course');


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