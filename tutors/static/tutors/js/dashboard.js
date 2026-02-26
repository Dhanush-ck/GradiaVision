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

const modal = document.getElementById('notif-modal');
const notifBtn = document.getElementById('notif-btn');
const closeBtn = document.getElementById('modal-close');
const submitBtn = document.getElementById('notif-submit');
const notifInput = document.getElementById('notif-input');

var departmentDropdown = document.getElementById('department');
var courseDropdown = document.getElementById('course');
var year = document.getElementById('year');
const classUpdate = document.getElementById('class-update');

const graph = document.getElementById('graph').getContext('2d');
let graphChart = null;

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
                    <th>Risk</th>
                </tr>
            `;
            tableBody.innerHTML = "";
            data.academic.forEach(e=> {
                let temp;
                if(e.sgpa_trend <= -1.0) {
                    temp = `<td class=risk-high>High Risk</td>`;
                }
                else if(e.sgpa_trend <= -0.7) {
                    temp = `<td class=risk-medium>Medium Risk</td>`;
                }
                else {
                    temp = `<td class=risk-low>Low Risk</td>`;
                }
                tableBody.innerHTML += `
                    <tr>
                        <td>${e.regno}</td>
                        <td>${e.name}</td>
                        <td>${e.sgpa}</td>
                        <td>${e.sgpa_trend*10}%</td>
                        ${temp}
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

function setGraph(){

    fetch("/tutor/graph/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        // body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data.count)
        // console.log(data.grades)
        if(graphChart) {
            graphChart.destroy();
        }
        graphChart = new Chart(graph, {
            type: 'bar',
            data: {
                labels: data.grades,
                datasets: [{
                    label: 'Count',
                    data: data.count,
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
                            font: {
                                size: 10,
                            },
                        }
                    },
                    y: {
                        beginAtZero: true,
                    }
                }
            }
        });
    });
}

setGraph();

notifBtn.addEventListener('click', () => {
  modal.classList.add('active');
  notifInput.focus();
});

closeBtn.addEventListener('click', () => {
  modal.classList.remove('active');
  notifInput.value = '';
});

modal.addEventListener('click', (e) => {
  if (e.target === modal) {
    modal.classList.remove('active');
    notifInput.value = '';
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    modal.classList.remove('active');
    notifInput.value = '';
  }
});

submitBtn.addEventListener('click', () => {
  const message = notifInput.value.trim();
  if (!message) {
    notifInput.focus();
    return;
  }

  console.log('Notification:', message);

  fetch("/tutor/notification/add/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })

  modal.classList.remove('active');
  notifInput.value = '';
});