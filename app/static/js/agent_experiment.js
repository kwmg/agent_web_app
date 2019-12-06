var random_comedy_List = new Array(
  "../static/img/c1.gif",
  "../static/img/c2.gif",
  "../static/img/c3.gif"
)
var random_history_List = new Array(
  "../img/h1.gif",
  "../img/h2.gif",
  "../img/h3.gif"
)
var random_crime_List = new Array(
  "../img/d1.gif",
  "../img/d2.gif",
  "../img/d3.gif"
)

var num = Math.floor(Math.random() * random_comedy_List.length)
var random_comedy = '<img src="' + random_comedy_List[num] + '" alt="">'
document.getElementById("comedy").innerHTML = random_comedy
