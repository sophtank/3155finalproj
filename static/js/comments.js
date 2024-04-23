//element that is the div of the comment screen
let bottomdiv = document.querySelector('.bottom-div');

//element that is the arrow for the comment screen
let downarrow = document.getElementById('downarrow');

//button that shows all comments
let viewcomments = document.getElementById('viewcomments');

//button that submits the comment
let submitcomment = document.getElementById('submitcomment');


//when arrow element is clicked the comment div is hidden
downarrow.addEventListener('click', function() {
    bottomdiv.style.display = 'none';
});

//when the viewcomments button is clicked the comment div is shown
viewcomments.addEventListener('click', function(){
    bottomdiv.style.display = 'block';
})

//this
submitcomment.addEventListener('click', function(){
    bottomdiv.style.display = 'block';
})