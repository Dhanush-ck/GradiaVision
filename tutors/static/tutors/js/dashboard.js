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

const alertBtn = document.getElementById('risk');
const riskType = document.getElementById('type');
const tableHead = document.getElementById('table-head');
const tableBody = document.getElementById('table-body');

var departmentDropdown = document.getElementById('department');
var courseDropdown = document.getElementById('course');
var year = document.getElementById('year');
const classUpdate = document.getElementById('class-update');

alertBtn.addEventListener('click', ()=>{
    getAlerts(type.value);
});
riskType.addEventListener('change', ()=> {
    getAlerts(type.value);
});

function getAlerts(alertType) {
    fetch("/tutor/risk/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({message: alertType})
    })
    .then(respone => respone.json())
    .then(data => {
        if(data.attendance) {
            // console.log(data.attendance);
            tableHead.innerHTML = `
                <tr>
                    <th>Reg no</th>
                    <th>Name</th>
                    <th>Attendance</th>
                </tr>
            `;
            tableBody.innerHTML = "";
            data.attendance.forEach(e=> {
                tableBody.innerHTML += `
                    <tr>
                        <td>${e.regno}</td>
                        <td>${e.name}</td>
                        <td>${e.attendance}</td>
                    </tr>
                `;
            })
        }
        else {
            // console.log(data.academic);
            tableHead.innerHTML = `
                <tr>
                    <th>Reg no</th>
                    <th>Name</th>
                    <th>SGPA</th>
                    <th>SGPA Trend</th>
                </tr>
            `;
            tableBody.innerHTML = "";
            data.academic.forEach(e=> {
                tableBody.innerHTML += `
                    <tr>
                        <td>${e.regno}</td>
                        <td>${e.name}</td>
                        <td>${e.sgpa}</td>
                        <td>${e.sgpa_trend}</td>
                    </tr>
                `;
            })
        }
    })
}

getAlerts(type.value)

departmentDropdown.addEventListener('change', function() {
    console.log("Department: " + this.value);
    handleCourse();
})

const handleCourse = ()=> {
    courseDropdown.innerHTML = "";
    const currentCourse = courses[departmentDropdown.value];
    for(i in currentCourse) {
        courseDropdown.innerHTML += `<option value='${i}'> ${currentCourse[i]} </option>`;
    }
}
handleCourse();

classUpdate.addEventListener('click', updateClass);

function updateClass() {
    const current_class = `${courseDropdown.value}${year.value}`;

    fetch("/tutor/update/class/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({message: current_class})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
}