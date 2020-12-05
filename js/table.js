const table = document.querySelector(".table")

const API = "https://sharkhacks.herokuapp.com/leaderboard"

function getData () {
    fetch(`${API}`).then(response => response.json()).then(displayData);
    
}
 
displayData =(res) =>{
    let data = res;
    for (key in data){
    console.log(key, data[key]);
    const tableData = document.createElement("tr")
    tableData.innerHTML = `
    <td>${key}</td>
    <td>${data[key]} 🦈</td>`
    table.appendChild(tableData)    
}
}

window.onload = getData()