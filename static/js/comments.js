let bottomdiv = document.querySelector('.bottom-div');
let downarrow = document.getElementById('downarrow');
let viewcomments = document.getElementById('viewcomments');
let submitcomment = document.getElementById('submitcomment');

bottomdiv.style.display = 'none';

downarrow.addEventListener('click', function() {
    bottomdiv.style.display = 'none';
});

viewcomments.addEventListener('click', function(){
    bottomdiv.style.display = 'block';
})

submitcomment.addEventListener('click', function(){
    bottomdiv.style.display = 'block';
})