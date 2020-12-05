const table = document.querySelector(".table")

const data ={
'user1': 30,
'user2' : 20 ,
'user3' : 30
}

for (key in data){
    console.log(key, data[key]);
    const tableData = document.createElement("tr")
    tableData.innerHTML = `
    <td>${key}</td>
    <td>${data[key]} 🦈</td>`
    table.appendChild(tableData)    
}