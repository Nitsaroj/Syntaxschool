let lesson_menu = document.getElementById('lesson_menu');
let lesson_list = document.getElementById('lesson_list');

lesson_menu.addEventListener('click',()=>{
    if(lesson_list.classList == 'hidden'){
        lesson_list.classList.add('block')
        lesson_list.classList.remove('hidden')
        lesson_menu.innerHTML ="⇧";
    }
    else{
        lesson_list.classList.add('hidden')
        lesson_list.classList.remove('block')
        lesson_menu.innerHTML="⇩";
    }
})
  
