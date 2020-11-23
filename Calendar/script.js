const date = new Date();

const renderCalendar = () => {
  date.setDate(1);

  const monthDays = document.querySelector(".days");

  const lastDay = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDate();

  const prevLastDay = new Date(
    date.getFullYear(),
    date.getMonth(),
    0
  ).getDate();

  const firstDayIndex = date.getDay();

  const lastDayIndex = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDay();

  const nextDays = 7 - lastDayIndex - 1;

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  document.querySelector(".date h1").innerHTML = months[date.getMonth()];

  document.querySelector(".date p").innerHTML = new Date().toDateString();

  let days = "";

  for (let x = firstDayIndex; x > 0; x--) {
    days += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
  }

  for (let i = 1; i <= lastDay; i++) {
    if (
      i === new Date().getDate() &&
      date.getMonth() === new Date().getMonth()
    ) {
      days += `<div class="today" id = ${i}>${i}</div>`;
    } else {
      days += `<div class = day id = ${i}>${i}</div>`;
    }
  }

  for (let j = 1; j <= nextDays; j++) {
    days += `<div class="next-date">${j}</div>`;
    monthDays.innerHTML = days;
  }
};

document.querySelector(".prev").addEventListener("click", () => {
  date.setMonth(date.getMonth() - 1);
  renderCalendar();
});

document.querySelector(".next").addEventListener("click", () => {
  date.setMonth(date.getMonth() + 1);
  renderCalendar();
});

var events_plan = Array(32);
for (i = 1; i <= 31; ++i){
  events_plan[i] = "";
}

let eventsForDate = ""
let lastDayClicked = -1;
let actualDayClicked;


document.querySelector(".days").addEventListener("click", () => {
  if (lastDayClicked != -1 && lastDayClicked != new Date().getDate() && document.getElementById(lastDayClicked).style.background != "rgb(77, 166, 255)"){
    document.getElementById(lastDayClicked).style.background = "#222227";
  }
  if (window.event.target.className === "days"){
    return;
  }
  if (window.event.target.className === "today") {
    lastDayClicked = window.event.target.textContent;
    document.querySelector(".listOfEvents").innerHTML = events_plan[lastDayClicked];
    return;
  }
  actualDayClicked = window.event.target.textContent
  if (lastDayClicked == -1){
    window.event.target.style.background = "#777";
  }
  else
    if(document.getElementById(actualDayClicked).style.background != "rgb(77, 166, 255)"){
      window.event.target.style.background = "#777";
    }
    console.log(actualDayClicked);
  document.querySelector(".listOfEvents").innerHTML = events_plan[actualDayClicked];
  lastDayClicked = window.event.target.textContent;
})

document.getElementById("btn").addEventListener("click", () => {
  if (document.getElementById("time").value === "" || document.getElementById("name").value === "" || lastDayClicked === -1) {
    return;
  }
  if (lastDayClicked != new Date().getDate()){
  document.getElementById(lastDayClicked).style.background = "#4da6ff"
  }
  console.log(events_plan[lastDayClicked]);
  events_plan[lastDayClicked] += document.getElementById("name").value + ": " + document.getElementById("time").value + "<br>";
  document.querySelector(".listOfEvents").innerHTML = events_plan[lastDayClicked];
})

document.getElementById("mail").addEventListener("click", () => {
   

  if (lastDayClicked != -1 && lastDayClicked != new Date().getDate() && document.getElementById(lastDayClicked).style.background != "rgb(77, 166, 255)"){
    document.getElementById(lastDayClicked).style.background = "#222227";
  }

    if (lastDayClicked != -1 && document.getElementById(lastDayClicked).style.background != "rgb(77, 166, 255"){
      document.getElementById(last) = "#777";
    }
  console.log(actualDayClicked);
  document.querySelector(".listOfEvents").innerHTML = events_plan[actualDayClicked];
  

  if (lastDayClicked != new Date().getDate()){
  document.getElementById(actualDayClicked).style.background = "#4da6ff"
  }
  events_plan[actualDayClicked] += document.getElementById("name").value + ": " + document.getElementById("time").value + "<br>";
  document.querySelector(".listOfEvents").innerHTML = events_plan[actualDayClicked];
  document.getElementById("mail").style.visibility = "hidden";
  
})

fetch("http://localhost:5000/index.html", {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify('{"grupa":"211/1"}')}).then( response => {
return response.json();
} ).then( res => {
  console.log(res);
  document.getElementById("mail").style.visibility = "visible";
  document.getElementById("name").value = res["platforma"]
  document.getElementById("time").value = res["ora"]
  actualDayClicked = res["zi"];
  console.log(actualDayClicked)
  

} )

var group;
document.getElementById("btnGrupa").addEventListener("click", () => {
    group = document.getElementById("grupa").value;
    functie()
})
const functie = () => {
fetch("http://localhost:5000/site.html", {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify( JSON.stringify({"grupa":group}) ) }).then( response => {
return response.json();
} ).then( res => {
  console.log(res);
  for (curs in res) {
    if (curs["zi"] === "Luni"){
      for (var i = 2; i <= 30; ++i) {
        events_plan[i] += curs["disc"] + " " + curs["ora"] + " " + curs["prof"] + "<br>" 
        document.querySelector(".listOfEvents").innerHTML = events_plan[lastDayClicked];
      }
    }
  }

} )
}

    //res -> ce iese din python

//console.log(window.event.target.textContent)
//document.querySelector(".listOfEvents").innerHTML = events_name[window.event.target.textContent] + ":" + events_hours[window.event.target.textContent]
//document.querySelector(".Events").style.visibility = "visible"
//events_name[window.event.target.textContent][events_name.length]
//events_hours[window.event.target.textContent][events_hours.length]
renderCalendar();

