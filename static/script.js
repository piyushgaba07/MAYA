// SCRIPT.JS
document.addEventListener('DOMContentLoaded',()=>{
    let message = document.querySelector('.content__footer-input_div input');
    let message_i = document.getElementById('message_i');
    let grid = document.querySelector('.content__footer-grid');
    let sidebar=document.querySelector('.sidebar');
    let new_chat = document.querySelectorAll('.sidebar__new-chat, #content__logo-i');
    let heading = document.querySelector('.content__main-heading');
    let new_message = document.querySelector('.content__messages');
    let username_div = document.querySelector('.sidebar__footer-user');
    let username = document.querySelector('.sidebar__footer-user_name');
    let logout_menu = document.querySelector('.sidebar__footer-user_logout');

    new_message.scrollTop=new_message.scrollHeight;
    // let sidebar__chats = document.querySelector('.sidebar__chats');

    // ENTER MESSAGE
    message.addEventListener('input',()=>{
        if(message.value.trim().length>0){
            message_i.style.backgroundColor="white";
            message_i.style.color="black";
        }
        else{
            message_i.style.backgroundColor="#373636";
            message_i.style.color="#aba9a9";
        }
        message.addEventListener('keypress',(event)=>{
            if(event.key==='Enter'){
                message_i.click();
            }
        });
    });
    username_div.addEventListener('mouseenter',()=>{
        logout_menu.style.display='block';
        username.style.display='none';
    })
    username_div.addEventListener('mouseleave',()=>{
        logout_menu.style.display='none';
        username.style.display='block';
    })

    // MESSAGE BUTTON
    // message_i.addEventListener('click',()=>{
        // if(message.value.trim().length>0){
        //     grid.style.display='none';
        //     heading.style.display='none';
        //     new_message.style.display='flex';
        //     document.querySelector('.content__main').style.justifyContent='flex-start';
                // new_message.scrollTop=new_message.scrollHeight;

            // if(new_message.innerHTML===''){
            //     let new_sidebar_chat = document.createElement('div');
            //     new_sidebar_chat.classList.add('sidebar__chat');
            //     new_sidebar_chat.innerHTML = `
            //         <p>${(message.value).substring(0, 20)}</p>
            //         <i class="fa-solid fa-trash"></i>
            //     `;
            //     new_sidebar_chat.addEventListener('mouseenter', () => {
            //         new_sidebar_chat.querySelector('i').style.display = 'inline-block';
            //     });
            //     new_sidebar_chat.addEventListener('mouseleave', () => {
            //         new_sidebar_chat.querySelector('i').style.display = 'none';
            //     });
            //     sidebar__chats.appendChild(new_sidebar_chat);
            //     new_sidebar_chat.querySelector('i').addEventListener('click',()=>{
            //         new_sidebar_chat.style.display='none';  
            //     })
            // }
            
            // new_message.innerHTML+=`
            // <div class="content__message">
            //     <div class='message__header'>
            //         <div class='message__header_logo'>${(username.innerHTML).substring(0, 2).toUpperCase()}</div>
            //         <div class='message__header_name'>You</div>
            //     </div>
            //     <div class="message__text">${message.value}</div>
            // </div>
            // <div class="content__message" style="margin:1.5rem 0rem;">
            //     <div class='message__header'>
            //         <div class='message__header_img'><img src="https://static-00.iconduck.com/assets.00/openai-icon-2021x2048-4rpe5x7n.png"></div>
            //         <div class='message__header_name'>Therapist AI</div>
            //     </div>
            //     <div class="message__text">${message.value}</div>
            // </div>
            // `
        // }
    //     message_i.style.backgroundColor="#373636";
    //     message_i.style.color="#aba9a9";
    //     message.value='';
    // });

    // NEW CHAT
    new_chat.forEach(element=>{
        element.addEventListener('click',()=>{
            grid.style.display='grid';
            heading.style.display='flex';
            document.querySelector('.content__main').style.justifyContent='center';
            new_message.style.display='none';
            new_message.innerHTML='';
        })  
    })

    // SHOW/HIDE SIDEBAR
    let arrow = document.querySelector('.arrow div');
    let sidebar_style = window.getComputedStyle(document.querySelector('.sidebar'));
    let content_newchat = document.getElementById('content__logo-i');
    arrow.addEventListener('click',()=>{
        if (sidebar_style.getPropertyValue('display') === 'flex'){
            sidebar.style.display="none";
            arrow.innerHTML='<i class="fa-solid fa-chevron-right"></i>';
            content_newchat.style.display='block';
        }
        else{
            sidebar.style.display="flex";
            arrow.innerHTML='<i class="fa-solid fa-chevron-left"></i>';
            content_newchat.style.display='none';
        }
    });

    // GRID HOVER
    let grid_div = document.querySelectorAll('.content__footer-grid_div');
    grid_div.forEach(grid_element=>{
        let grid_i= grid_element.querySelector('i');
        grid_element.addEventListener('mouseenter',()=>{
            grid_i.style.display="block";
        });
        grid_element.addEventListener('mouseleave',()=>{
            grid_i.style.display="none";
        });
        grid_element.addEventListener('click',()=>{
            let string1 = grid_element.querySelector('.content__footer-grid_div-1').innerHTML;
            let string2 = grid_element.querySelector('.content__footer-grid_div-2').innerHTML;
            message.value = string1+" " +string2;
            message_i.click();
        });
    });

    // USER IMAGE
    (document.querySelectorAll('.sidebar__footer-user_logo,.message__header_logo')).forEach(element=>{
        element.innerHTML=((username.innerHTML).substring(0, 2).toUpperCase());
    })
});

