window.addEventListener("scroll",function(){
    let header = document.querySelector('.navbar');
    let head = document.querySelector('.navbar');
    header.classList.toggle("sticky" , window.scrollY > 100);
    header.classList.remove("bg-transparent" , window.scrollY > 100);
})

const reply = document.querySelectorAll('.comments .container .comment .reply');
const replyForm = document.querySelectorAll('.comments .container .comment .replyForm ');

console.log(reply,replyForm)
for (let i=0;i<replyForm.length;i++){
    replyForm.item(i).style.display = 'none'
}



for(let i=0;i<reply.length;i++){
reply.item(i).addEventListener('click',()=>{
    if(replyForm.item(i).style.display === 'none'){
        replyForm.item(i).style.display = 'block';
    }
    else{
        replyForm.item(i).style.display = 'none';
    }
})
}