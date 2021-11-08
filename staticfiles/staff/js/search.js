// Deployment Asset Serial live search

const searchField = document.querySelector('#searchField');

const exist = document.querySelector('#exist')

exist.style.display = 'none';

searchField.addEventListener('keyup', (e) => {

    const searchValue = e.target.value;

    if(searchValue.trim().length > 0){

        fetch('/live_search/', {
            body: JSON.stringify({searchText: searchValue}),
            method: 'POST',
        })

        .then((res) => res.json())
        .then((data) => {
            exist.style.display = 'block';
            
            if (data.length > 0){
                
                exist.innerHTML = 'Serial Number Already Registered';
                
            } else{

                exist.innerHTML = '';

            }

        }
        
        )
    }else{
        exist.style.display = 'none';
    }

});

