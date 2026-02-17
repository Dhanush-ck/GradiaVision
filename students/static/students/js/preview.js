const currentSemester = document.getElementById('semester');
const tbody = document.getElementById('table-body');

var subjects;

getData(currentSemester.value);

currentSemester.addEventListener('change', ()=> {
    getData(currentSemester.value);
})

function getData(message) {
    fetch("/student/preview/manage/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data.reply);
        updateData(data.reply)
    });
}

function updateData(data) {
    subjects = Object.values(data);
    tbody.innerHTML = "";

    subjects.forEach((s,i)=>{

        tbody.innerHTML += `
        <tr data-index="${i}">
        <td>${s.code}</td>
        <td>${s.name}</td>
        <td>${s.credits}</td>
        <td>${s.type}</td>

        <td>
        <input class="cca" value="${s.cca_score}">
        </td>
        <td>
            <span class='cca-max' data-value="${s.cca_max}">${s.cca_max}</span>
            </td>

        <td>
        <input class="ese" value="${s.ese_score}">
        </td>
        
        <td>
            <span class='ese-max' data-value="${s.ese_max}">${s.ese_max}</span>
        </td>

        <td class="total">${s.total}</td>

        <td>${s.total_max}</td>

        <td class="grade">-</td>
        </tr>
        `;

    });

    calculateAll();
}

tbody.addEventListener("input", e=>{

    const row = e.target.closest("tr");
    const i = row.dataset.index;

    let cca = Number(row.querySelector(".cca").value || 0);
    let ese = Number(row.querySelector(".ese").value || 0);
    const ese_max = Number(row.querySelector(".ese-max").dataset.value);
    const cca_max = Number(row.querySelector(".cca-max").dataset.value);
    
    if(ese > ese_max) {
        row.querySelector('.ese').value = 0;
        alert(`Enter score less than ${ese_max}`);
        return;
    }

    if(cca > cca_max) {
        row.querySelector('.cca').value = 0;
        alert(`Enter score less than ${cca_max}`);
        return;
    }

    // update JSON
    subjects[i].cca_score = cca;
    subjects[i].ese_score = ese;
    subjects[i].total = cca + ese;

    // update row total
    row.querySelector(".total").innerText = subjects[i].total;

    calculateAll();

});

function getGrade(p){
    if(p>=95) return "O";
    if(p>=85) return "A+";
    if(p>=75) return "A";
    if(p>=65) return "B+";
    if(p>=55) return "B";
    if(p>=45) return "C";
    if(p>=35) return "P";
    return "F";
}

function gp(g){
    return {
        'O':10,
        'A+':9,
        'A':8,
        'B+':7,
        'B':6,
        'C':5,
        'P':4,
        'F':0
    }[g];
}

function calculateAll(){

    const grouped = {};

    subjects.forEach(s=>{

    if(!grouped[s.code]){
        grouped[s.code]={
            total:0,
            total_max:0,
            credits:s.credits
        };
    }

    grouped[s.code].total += s.total;
    grouped[s.code].total_max += s.total_max;

    });

    // grade per subject code
    Object.keys(grouped).forEach(code=>{

    const s = grouped[code];
    const percent = (s.total/s.total_max)*100;
    s.grade = getGrade(percent);

    // show grade only in TH row
    document.querySelectorAll("#table-body tr").forEach(r=>{
        // console.log(r.children[3].innerText)
    if(r.children[0]?.innerText===code && r.children[3].innerText==="TH"){
        r.querySelector(".grade").innerText = s.grade;
        // console.log(r);
    }
    });

    });

    calculateSGPA(grouped);
}

function calculateSGPA(grouped){

    let sum=0, credits=0;

    Object.values(grouped).forEach(s=>{
    sum += gp(s.grade)*s.credits;
    credits += s.credits;
    });

    document.getElementById("sgpa").innerText = (sum/credits || 0).toFixed(2);
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}