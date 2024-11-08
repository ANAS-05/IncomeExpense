const searchField = document.querySelector('#searchField');
const appTable = document.querySelector('.app-table');
const noResultContainer = document.querySelector('.noresult-container');
const paginationContainer = document.querySelector('.pagination-container');
const tableOutput = document.querySelector('.output-table');

tableOutput.style.display = "none";
noResultContainer.style.display = "none";


searchField.addEventListener('keyup',(e)=>{

    const searchValue = e.target.value;

    if (searchValue.trim().length > 0){
        paginationContainer.style.display = "none";
        tableOutput.innerHTML = "";
        console.log("DEBUG");
        fetch("/search-expenses", {
            method: "POST",
            body: JSON.stringify({ searchText: searchValue })
          })
          .then(res => {
            if (!res.ok) {
                throw new Error('Network response was not ok');
            }
            return res.json();
        })
            .then((data) => {

             tableOutput.style.display = "block";
             appTable.style.display = "none";

             if(data.length === 0){
                noResultContainer.style.display = "block";
                tableOutput.style.display = "none";
             }
             else{
                noResultContainer.style.display = "none";
            
                data.forEach(expense => {
                
                tableOutput.innerHTML += `
                
                <tr>
                <td>${expense.amount}</td>
                <td>${expense.category}</td>
                <td>${expense.description}</td>
                <td>${expense.date}</td>
                </tr>`;
                
                });
             }
            });
        
    }

    else{
        appTable.style.display = "block";
        paginationContainer.style.display = "block";
        tableOutput.style.display = "none";
        noResultContainer.style.display = "none";
    }
});