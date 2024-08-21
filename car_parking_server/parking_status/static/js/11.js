const parking_pos = [
    [1,  2,  25, 26, 47,  0],       // row 1
    [3,  4,  27, 28, 49, 48],      // row 2
    [5,  6,  29, 30, 51, 50],      // row 3
    [7,  8,  31, 32, 53, 52],      // row 4
    [9,  10, 33, 34, 55, 54],     // row 5
    [11, 12, 35, 36, 57, 56],    // row 6
    [13, 14, 37, 38, 59, 58],    // row 7
    [15, 16, 39, 40, 61, 60],    // row 8
    [17, 18, 0 , 0 , 63, 62],    // row 9
    [19, 20, 41, 42, 65, 64],    // row 10
    [21, 22, 43, 44, 67, 66],    // row 11
    [23, 24, 45, 46, 69, 68],    // row 12
]

const TOTAL_SLOT = 69;

const parkingEle = document.getElementById('parking');

document.addEventListener("DOMContentLoaded", function(){
    console.log('Page loaded');
    // load parking slots to UI
    parking_pos.forEach(row =>{
        console.log(row);
        newRowDiv = document.createElement('div');
        newRowDiv.className = 'row mb-2';
        row.forEach((col, i) => {
            const slotId = 'Slot' + String(col);
            newColEle = document.createElement('div');
            className = i % 2 == 0 ? 'col-2 text-end' : 'col-2'
            newColEle.className = className;
            btnEle = document.createElement('button');

            className = col == 0 ? 'btn btn-outline-secondary disabled' : 'btn btn-primary'

            btnEle.setAttribute("class", className);
            btnEle.setAttribute("type", "button");
            btnEle.setAttribute("id", slotId);
            btnText = col == 0 ? 'X' : slotId;
            btnEle.innerHTML = btnText;

            newColEle.appendChild(btnEle);
            newRowDiv.appendChild(newColEle)
            
        })
        parkingEle.appendChild(newRowDiv);
    })

    // <div class="row">
    //     <div class="col-2 text-end">
    //         <button type="button" class="btn btn-primary">Slot1</button>
    //     </div>
    //     <div class="col-2">
    //         <button type="button" class="btn btn-primary">Slot2</button>
    //     </div>
    //     <div class="col-2 text-end">
    //         <button type="button" class="btn btn-primary">Slot3</button>
    //     </div>
    //     <div class="col-2">
    //         <button type="button" class="btn btn-primary">Slot4</button>
    //     </div>
    //     <div class="col-2 text-end">
    //         <button type="button" class="btn btn-primary">Slot5</button>
    //     </div>
    //     <div class="col-2">
    //         <button type="button" class="btn btn-primary">Slot6</button>
    //     </div>
    // </div>

})

function fetch_data(url = '/parking/lastest'){
    console.log(url);
    return new Promise((resolve, reject) => {
        fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
            mode: 'no-cors',
            })
            .then(res => res.json()).then(res => {
                resolve(res);
            });
    });
}

function convertData2Array(strData){
    let sTemp = strData.replace('[', '').replace(']', '');
    let strArr = sTemp.split(',');
    let intArr = strArr.map(s => Number(s));
    return intArr;
}

async function cyclic_request(){
    console.log("request to server");
    const get_url = 'http://127.0.0.1:8000/parking/lastest/';
    data = await fetch_data(get_url);
    if (data.length == 0 ) return;
    const freeSlots = convertData2Array(data[0].freeSlots);

    console.log(freeSlots, typeof(freeSlots));

    for(let i = 0; i < TOTAL_SLOT; i++){
        const id = 'Slot' + String(i+1);
        slotEle = document.getElementById(id);
        className = freeSlots.indexOf(i+1) !== -1 ? 'btn btn-primary' : 'btn btn-danger';
        slotEle.className = className;
    }
}

setInterval(cyclic_request, 500);