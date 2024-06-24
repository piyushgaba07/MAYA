// LOGIN.JS
document.addEventListener('DOMContentLoaded',()=>{
    let email_p = document.getElementById('floating_placeholder');
    let password_p = document.getElementById('floating_placeholder-1');

    let email = document.querySelector('.input-email input');
    let password = document.querySelector('.input-password input');

    let cont = document.querySelector('.continue button');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    //EMAIL
    email.addEventListener('focus',()=>{
        at_focus(email,email_p);
        let error_email = document.querySelector('.invalid_email');
        email.addEventListener('keypress',(event)=>{
            if(event.key==='Enter' && email.value.trim().length === 0){
                error_email.innerHTML="<p><i class='fa-solid fa-circle-exclamation'></i> Enter an email address!</p>";
                error_email.style.display='flex';
            }
            else if(event.key==='Enter' && !emailRegex.test(email.value.trim())) {
                error_email.innerHTML="<p><i class='fa-solid fa-circle-exclamation'></i> Email is not valid!</p>";
                error_email.style.display='flex';
            }
            else if(event.key==='Enter' && emailRegex.test(email.value.trim()) && password.value.trim().length>=12){
                cont.click();
            } 
            else error_email.style.display='none';
        })
    })
    email.addEventListener('blur',()=>{
        at_blur(email,email_p,'Email Address');
    })

    //PASSWORD
    password.addEventListener('focus',()=>{
        at_focus(password,password_p);
        password.addEventListener('keypress',(event)=>{
            let error_password = document.querySelector('.empty_password');
            if(event.key==='Enter' && emailRegex.test(email.value.trim()) && password.value.trim().length>=12){
                cont.click();
            }
            else if(event.key==='Enter' && password.value.trim()===''){
                error_password.style.display='flex';
            }
            else{
                error_password.style.display='none';
            }
        })
    })
    password.addEventListener('blur',()=>{
        at_blur(password,password_p,'Password');
    })

    document.addEventListener('keypress',(event)=>{
        if(event.key==='Enter' && email.value.trim()!=='' && emailRegex.test(email.value.trim())){
            cont.click();
        }
    })

    let hide = document.getElementById('hide');
    hide.addEventListener('click',()=>{
        hide.classList.toggle('fa-eye');
        hide.classList.toggle('fa-eye-slash');

        if(hide.classList.contains('fa-eye-slash')) password.setAttribute('type','password');
        else password.setAttribute('type','text');
    })
});
function at_focus(element,element_p){
    element.setAttribute('placeholder','');
    element_p.style.display='inline-block';
}   
function at_blur(element,element_p,text){
    element.setAttribute('placeholder',text);
    element_p.style.display='none';
}