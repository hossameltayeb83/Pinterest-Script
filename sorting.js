
let mainTable= document.querySelector('table')




function sortTable(table,column,asc = true) {
    const dirModifier = asc ? 1:-1
    const tBody = table.tBodies[0]
    const rows = Array.from(tBody.querySelectorAll('tr'))
    const sortedRows = rows.sort((a,b)=>{
        const aColText = parseInt(a.querySelector(`td:nth-child(${column+1})`).textContent)
        const bColText = parseInt(b.querySelector(`td:nth-child(${column+1})`).textContent)    
        return aColText > bColText ? (1*dirModifier): (-1*dirModifier)
    })
    while (tBody.firstChild) {
        tBody.removeChild(tBody.firstChild)     
    }
    tBody.append(...sortedRows)

}
sortTable(mainTable,1,false)
