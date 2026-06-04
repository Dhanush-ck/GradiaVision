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

var dataHolder = document.getElementById('data-holder');

var departmentDropdown = document.getElementById('department');
var courseDropdown = document.getElementById('course');
var yearDropdown = document.getElementById('year');
let updateBtn = document.getElementById('updateFilter');

var date = document.getElementById('date');
var hour = document.getElementById('hour');
var subjectDropdown = document.getElementById('subject');
var submitBtn = document.getElementById('submitBtn');

var students = document.getElementById('students');

//////// Department Dropdown Change ////////

departmentDropdown.addEventListener('change', function() {
    // console.log("Department: " + this.value);
    handleCourse();
})

//////// Dynamic Course Handle ////////
const handleCourse = ()=> {
    courseDropdown.innerHTML = "";
    const currentCourse = courses[departmentDropdown.value];
    for(i in currentCourse) {
        courseDropdown.innerHTML += `<option value='${i}'> ${currentCourse[i]} </option>`;
        // console.log(`<option value='${i}'> ${currentCourse[i]} <option>`);
    }
}
handleCourse();

//////// Course Dropdown Change ////////

courseDropdown.addEventListener('change', ()=> {
    yearDropdown.innerHTML = "";
    handleYear();
})

//////// Dynamic Year Handle ////////

function handleYear() {
    const n = courseDropdown.value == "MScCS" ? 2: 4;
    for(i=1; i<=n; i++) {
        yearDropdown.innerHTML += `<option value=${i}>${i}</option>`
    }
}
handleYear();

//////// Teachers Class Details Assignment ////////

if(dataHolder != null){
    for( key in courses) {
        if(courses[key][dataHolder.dataset.course]) {
            departmentDropdown.value = key;
        }
    }
    
    courseDropdown.value = dataHolder.dataset.course;
    
    yearDropdown.value = dataHolder.dataset.year;
}

//////// Class Filter Button ////////

updateBtn.addEventListener('click', ()=> {
    getStudentList();
})

//////// Today's Date Assignment ////////

const today = new Date();
date.value = today.toISOString().slice(0, 10);

//////// Hour Validation ////////

hour.addEventListener('change', ()=> {
    // console.log(hour.value);
    if(hour.value >= 1 && hour.value <= 5) {
        submitBtn.disabled = false;
    }
    else {
        alert("Enter a value from 1 to 5");
        submitBtn.disabled = true;
    }
})

//////// Dynamic Student List Update ////////

function getStudentList() {
    current_class = courseDropdown.value + yearDropdown.value;
    // console.log(current_class);

    fetch('/attendance/getStudents/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({current_class: current_class})
    })
    .then(response => response.json())
    .then(students_data => {
        student_data = students_data.data;
        if(student_data != null) {
            students.innerHTML = "";
            student_data.forEach((data)=> {
                const tr = document.createElement('tr');
                
                const rollno = document.createElement('td');
                rollno.innerText = data.rollno;
                
                const name = document.createElement('td');
                name.innerText = data.name;
                
                const checkBoxHolder = document.createElement('td');
                const checkBox = document.createElement('input');
                checkBox.type = "checkbox";
                checkBox.name = "present_students";
                checkBox.className = "present_students";
                checkBox.value = data.regno;
                
                tr.append(rollno);
                tr.append(name);
                checkBoxHolder.append(checkBox);
                tr.append(checkBoxHolder);
                
                students.append(tr);
            })
        }
        else {
            students.innerHTML = " No records";
        }

        const subjects = students_data.subjects;
        subjectDropdown.innerHTML = " ";
        subjects.forEach(subject=> {
            subjectDropdown.innerHTML += `<option value=${subject.code}>${subject.name}</option>`
        })
    })
}
getStudentList();

//////// Attendance Submit Button ////////

submitBtn.addEventListener('click', ()=> {
    var attendance = [];

    document.querySelectorAll(".present_students").forEach(checkbox => {
        attendance.push({
            regno: checkbox.value,
            status: checkbox.checked ? "P": "A",
        })
    })

    current_class = courseDropdown.value + yearDropdown.value;

    // console.log(attendance);

    fetch("/attendance/markAttendance/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            attendance: attendance,
            date: date.value,
            hour: hour.value,
            subject: subjectDropdown.value,
            current_class: current_class,
        }),
    })
    .then(response => response.json())
    .then(data => { 
        alert(data.message);
    })
})