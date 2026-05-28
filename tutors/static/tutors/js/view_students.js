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

var students = document.getElementById('students');
var student = document.querySelectorAll('.student');

var studentCard = document.getElementById('studentCard');
var studentCardName = document.getElementById('studentCardName');
var studentCardEmail = document.getElementById('studentCardEmail');
var studentCardRegno = document.getElementById('studentCardRegno');
var studentCardAadhaar = document.getElementById('studentCardAadhaar');
var studentCardGraph = document.getElementById('graph').getContext('2d');

var type = document.getElementById('type');
var semester = document.getElementById('semester');

var current_class = "";
var current_email = "";
var current_semester;
var semesters;
let graphChart = null;


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

for( key in courses) {
    if(courses[key][dataHolder.dataset.course]) {
        departmentDropdown.value = key;
    }
}

courseDropdown.value = dataHolder.dataset.course;

yearDropdown.value = dataHolder.dataset.year;

updateBtn.addEventListener('click', ()=> {
    // console.log(courseDropdown.value + yearDropdown.value);
    getStudents(courseDropdown.value + yearDropdown.value);
})

function getStudents(classInfo) {
    fetch("/tutor/filter/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({message: classInfo})
        })
        .then(respone => respone.json())
        .then(data => {
            students.innerHTML = "";
            const studentData = data.class_info;
            if(studentData.length == 0) {
                students.innerHTML = "No records found";
            }
            else {
                studentData.forEach((student)=> {
    
                    const studentDiv = document.createElement('div');
                    studentDiv.className = 'student';
                    studentDiv.dataset.email = student['email'];
    
                    const studentName = document.createElement('div');
                    studentName.className = 'studentName';
                    studentName.innerText = student['name'];
    
                    const studentRegno = document.createElement('div');
                    studentRegno.className = 'studentRegno';
                    studentRegno.innerText = student['regno'];
    
                    studentDiv.append(studentName);
                    studentDiv.append(studentRegno);
    
                    students.appendChild(studentDiv);
                })
            }
        })

}

students.addEventListener('click', (e)=> {
    const clickedStudent = e.target.closest('.student');
    current_email = clickedStudent.dataset.email;
    activateStudentCard(clickedStudent.dataset.email);
    document.getElementById('card-overlay').classList.add('active');
})

function activateStudentCard(email) {
    fetch("/tutor/studentCard/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({email: email})
    })
    .then(response => response.json())
    .then(data => {

        studentCardName.innerText = data.name;
        studentCardEmail.innerText = data.email;
        studentCardRegno.innerText = data.regno;
        studentCardAadhaar.innerText = data.aadhaar;

        current_semester = data.semester;
        setSemesters(data.semester_count)

        if(graphChart) {
            graphChart.destroy();
        }
        graphChart = new Chart(studentCardGraph, {
            type: 'line',
            data: {
                labels: data.semesters,
                datasets: [{
                    label: 'SGPA',
                    data: data.scores,
                    borderWidth: 2,
                    tension: 0.3,
                    // pointRadius: function(studentCardGraph) {
                    //     if(data.scores.length != 1) {
                    //         return studentCardGraph.dataIndex === data.scores.length - 1 ? 6 : 3;
                    //     }
                    //     else{
                    //         return studentCardGraph.dataIndex === 0 ? 6 : 3;   
                    //     }
                    // },
                    pointRadius: 3,

                    // pointBackgroundColor: function(studentCardGraph) {
                    //     if(data.scores.length != 1) {
                    //         return studentCardGraph.dataIndex === data.scores.length - 1 ? 'red' : '#36a2eb';
                    //     }
                    // },

                    // pointBorderColor: function(studentCardGraph) {
                    //     if(data.scores.length != 1) {
                    //         return studentCardGraph.dataIndex === data.scores.length - 1 ? 'red' : '#36a2eb';
                    //     }
                    // }
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        ticks: {
                            maxRotation: 0,
                            minRotation: 0
                        }
                    },
                    y: {
                        beginAtZero: true,
                        max: 10,
                    }
                }
            }
        });

    })
}

type.addEventListener('change', ()=> {
    showSem();
    setGraph();
})

semester.addEventListener('change', ()=> {
    setGraph();
})

function setGraph() {
    fetch('/tutor/graphType/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: current_email,
            graph_type: type.value,
            semester: semester.value,
        })
    })
    .then(response => response.json())
    .then(data => {

        if(type.value == "sem") {
            if(graphChart) {
                graphChart.destroy();
            }
            graphChart = new Chart(studentCardGraph, {
                type: 'bar',
                data: {
                    labels: data.subjects,
                    datasets: [{
                        label: 'Percentage',
                        data: data.percentages,
                        borderWidth: 2,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            ticks: {
                                display: false,
                                // maxRotation: 90,
                                // minRotation: 90,
                                font: {
                                    size: 10,
                                },
                                // callback: function(value) {
                                //     return data.subjects[value].split(" ");
                                // }
                            }
                        },
                        y: {
                            beginAtZero: true,
                            max: 100,
                        }
                    }
                }
            });
        }
        else {

            if(graphChart) {
                graphChart.destroy();
            }
            graphChart = new Chart(studentCardGraph, {
                type: 'line',
                data: {
                    labels: data.semesters,
                    datasets: [{
                        label: 'SGPA',
                        data: data.scores,
                        borderWidth: 2,
                        tension: 0.3,
                        // pointRadius: function(studentCardGraph) {
                        //     if(data.scores.length != 1) {
                        //         return studentCardGraph.dataIndex === data.scores.length - 1 ? 6 : 3;
                        //     }
                        //     else{
                        //         return studentCardGraph.dataIndex === 0 ? 6 : 3;   
                        //     }
                        // },
                        pointRadius: 3,

                        // pointBackgroundColor: function(studentCardGraph) {
                        //     if(data.scores.length != 1) {
                        //         return studentCardGraph.dataIndex === data.scores.length - 1 ? 'red' : '#36a2eb';
                        //     }
                        // },

                        // pointBorderColor: function(studentCardGraph) {
                        //     if(data.scores.length != 1) {
                        //         return studentCardGraph.dataIndex === data.scores.length - 1 ? 'red' : '#36a2eb';
                        //     }
                        // }
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            ticks: {
                                maxRotation: 0,
                                minRotation: 0
                            }
                        },
                        y: {
                            beginAtZero: true,
                            max: 10,
                        }
                    }
                }
            });
        }

    })
}

function showSem() {
    if(type.value == "sem") {
        semester.style.display = "block";
    }
    else {
        semester.style.display = "none";
    }
}
showSem();

function setSemesters(semesters) {
    semester.innerHTML = "";
    for(let i=0; i < semesters.length; i++) {
        semester.innerHTML += `<option value=${semesters[i]}>Semester ${semesters[i]}</option>`;
    }
}

document.getElementById('close').addEventListener('click', () => {
  document.getElementById('card-overlay').classList.remove('active');
  type.value = "course";
  showSem();
});

document.getElementById('card-overlay').addEventListener('click', (e) => {
  if (e.target === document.getElementById('card-overlay')) {
    document.getElementById('card-overlay').classList.remove('active');
  }
});