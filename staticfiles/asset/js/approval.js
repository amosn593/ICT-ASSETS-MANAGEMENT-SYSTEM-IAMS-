
const user = document.getElementById('client');
const user_value = user.innerHTML;

const hod = document.getElementById('hod');
const hod_value = hod.innerHTML;

const ict = document.getElementById('ict');
const ict_value = ict.value;

console.log(user_value);



if(user_value == 'Pending'){
    user.setAttribute("bgcolor","red");
    user.style.color = 'black';

}

if(hod_value == 'Pending'){
    hod.setAttribute("bgcolor","red");
    hod.style.color = 'black';
    
}