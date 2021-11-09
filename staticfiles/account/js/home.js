// Home tab Asset live search
const searchField = document.querySelector('#liveText');

const num = document.querySelector('#num');

const tbody = document.querySelector('.tabbody');

const tabLive = document.querySelector('.tab-live');

const tabData = document.querySelector('.tab-data');

const pag = document.querySelector('.pagination');

tabLive.style.display = 'none';

searchField.addEventListener('keyup', (e) => {

    const asset = e.target.value;

    if(asset.trim().length > 0){

        pag.style.display = 'none';

        tbody.innerHTML = '';

        fetch('/result_search/', {
            body: JSON.stringify({searchText: asset}),
            method: 'POST',
            })
    
            .then((res) => res.json())
            .then((data) => {

                    tabData.style.display = 'none';
                    tabLive.style.display = 'block';

                    console.log('data', data);

                    num.innerHTML = 'No. of Records:'+ ' ' + data.length;

                    if(data.length === 0){
                        tabLive.innerHTML = 'No Records Found!!!';
                    }else{
                        tabLive.innerHTML = '';

                        data.forEach((item) => {
                            tbody.innerHTML += `
                            <tr>
                                <td>${item.asset_type}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_model}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>
                                <td>${item.asset_serial}</td>

                            </tr>
                            `;
                        });

                    }
                       
            }
            
        )
               
    }else{
        tabLive.style.display = 'none';
        tabData.style.display = 'block';
        pag.style.display = 'block';

    }
}
);