const tableBody = document.getElementById('table-body');
const currentSem = document.getElementById('current-sem')
const type = document.getElementById('type');
const semester = document.getElementById('semester');

const graph = document.getElementById('graph').getContext('2d');

var notifications;
getNotification();

function getNotification() {
    fetch("/student/notification/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        // body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data.reply);
        // console.log(data);
        notifications = data.data;
        tableBody.innerHTML = '';
        notifications.forEach(noti=> {
            tableBody.innerHTML += `
                <tr>
                    <td>${noti.message}</td>
                    <td>${noti.tutor}</td>
                    <td>${noti.date}</td>
                    <td>${noti.time}</td>
                </tr>
            `;
        })
    }); 
}

function showSem() {
    setSemesters();
    if(type.value == "sem") {
        semester.style.display = "block";
    }
    else {
        semester.style.display = "none";
    }
}
showSem();

function setSemesters() {
    semester.innerHTML = "";
    for(let i=1; i <= currentSem.value; i++) {
        semester.innerHTML += `<option value=${i}>Semester ${i}</option>`;
    }
}

type.addEventListener('change', ()=> {
    showSem();
    setGraph();
});

semester.addEventListener('change', setGraph);

let graphChart = null;

function setGraph() {
    var data = {}

    if(type.value == "sem") {
        data = {
            type: type.value,
            sem: semester.value,
        }
    }
    else {
        data = {
            type: type.value,
        }
    }

    fetch("/student/graph/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if(type.value == "sem") {
            if(graphChart) {
                graphChart.destroy();
            }
            graphChart = new Chart(graph, {
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
            console.log(data.scores)
            console.log(data.semesters)
            graphChart = new Chart(graph, {
                type: 'line',
                data: {
                    labels: data.semesters,
                    datasets: [{
                        label: 'SGPA',
                        data: data.scores,
                        borderWidth: 2,
                        tension: 0.3,
                        pointRadius: function(graph) {
                            if(data.scores.length != 1) {
                                return graph.dataIndex === data.scores.length - 1 ? 6 : 3;
                            }
                            else{
                                return graph.dataIndex === 0 ? 6 : 3;   
                            }
                        },

                        pointBackgroundColor: function(graph) {
                            if(data.scores.length != 1) {
                                return graph.dataIndex === data.scores.length - 1 ? 'red' : '#36a2eb';
                            }
                        },

                        pointBorderColor: function(graph) {
                            if(data.scores.length != 1) {
                                return graph.dataIndex === data.scores.length - 1 ? 'red' : '#36a2eb';
                            }
                        }
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
    }); 
}

setGraph();

const toggle = document.getElementById('menu-toggle');
const sidebar = document.querySelector('.sidebar');
const overlay = document.getElementById('sidebar-overlay');
toggle?.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    overlay.classList.toggle('active');
});
overlay?.addEventListener('click', () => {
    sidebar.classList.remove('open');
    overlay.classList.remove('active');
});