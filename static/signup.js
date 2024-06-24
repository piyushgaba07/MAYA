// SIGNUP.JS
document.addEventListener('DOMContentLoaded',()=>{
    let username_p = document.getElementById('floating_placeholder-user');
    let email_p = document.getElementById('floating_placeholder');
    let password_p = document.getElementById('floating_placeholder-1');
    
    let username = document.querySelector('.input-username input');
    let email = document.querySelector('.input-email input');
    let password = document.querySelector('.input-password input');
    
    let cont = document.querySelector('.continue button');
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // USERNAME
    username.addEventListener('focus',()=>{
        at_focus(username,username_p);
        username.addEventListener('keypress',(event)=>{
            let error_username = document.querySelector('.empty_user');

            if(event.key==="Enter" && username.value.trim()!=='' && emailRegex.test(email.value.trim()) && password.value.trim().length>=12) {
                cont.click();
            }
            else if(event.key==="Enter" && username.value.trim()!=='' && email.value.trim()===''){
                username.blur();
                email.focus();
            }
            else if(event.key==='Enter' && username.value.trim()===''){
                error_username.style.display='flex';
                username.style.marginBottom ='0rem';
            }
            else {
                error_username.style.display='none';
                username.style.marginBottom ='1rem';
            }
        })
    })
    username.addEventListener('blur',()=>{
        at_blur(username,username_p,'Username');
    })

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
            else if(event.key==='Enter' && emailRegex.test(email.value.trim()) && username.value.trim()===''){
                email.blur();
                username.focus();
            }
            else if(event.key==='Enter' && emailRegex.test(email.value.trim()) && username.value.trim()!==''  && password.value.trim()===''){
                email.blur();
                password.focus();
            }
            else if(event.key==='Enter' && emailRegex.test(email.value.trim()) && username.value.trim()!=='' && password.value.trim()!=''){
                cont.click();
            }
            else{
                error_email.style.display='none';
            }
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
            if(event.key==='Enter' && password.value.trim().length>=12 && emailRegex.test(email.value.trim()) && username.value.trim()!=='' ){
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
        if(event.key==='Enter' && username.value.trim()!=='' && email.value.trim()!=='' && emailRegex.test(email.value.trim()) && password.value.trim().length>12)
            cont.click();
    })

    let hide_password = document.getElementById('hide');
    hide_password.addEventListener('click',()=>{
        hide_password.classList.toggle('fa-eye');
        hide_password.classList.toggle('fa-eye-slash');

        if(hide_password.classList.contains('fa-eye-slash')) password.setAttribute('type','password');
        else password.setAttribute('type','text');
    })
    password.addEventListener('input',()=>{
        let password_check_i = document.querySelector('.green i');
        if(password.value.trim().length>=12) {
            document.querySelector('.green').style.color='var(--text-login)';
            password_check_i.classList.remove('fa-xmark');
            password_check_i.classList.add('fa-check');
        }
        else {
            document.querySelector('.green').style.color='red';
            password_check_i.classList.add('fa-xmark');
            password_check_i.classList.remove('fa-check');
        }
    })
})
function at_focus(element,element_p){
    element.setAttribute('placeholder','');
    element_p.style.display='inline-block';
}   
function at_blur(element,element_p,text){
    element.setAttribute('placeholder',text);
    element_p.style.display='none';
}