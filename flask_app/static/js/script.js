// ==================================== 
// USER SETTINGS PAGE
// ====================================
function toggle_hidden(event){
    var activeInfo = document.querySelector('.info-content.active')
    if(activeInfo){
        document.querySelector('.info-content.active').classList.remove('active');
    }
    event.target.parentElement.classList.toggle("active");
}

// ==================================== 
// SEARCH PAGE
// ====================================
function alterSearch(event){
    var selected = document.querySelector(".search_by").value;
    if(selected == ""){
        removeAll();
        removeSingle();
        removeActives();
    }else if(selected == "all"){
        removeSingle();
        removeActives();
        document.querySelector(".search_by_wrp").classList.add('all')
        all_inputs = document.querySelectorAll('.search_by_wrp .hide');
        for(i=0;i < all_inputs.length; i++){
            all_inputs[i].classList.add('active')
        }
    }else{
        removeAll();
        removeActives();
        all_selects = document.querySelector(".search_by_wrp");
        all_selects.classList.add('single')
        document.querySelector('.search_by_wrp .' + selected).classList.add('active');
    }
}

function removeAll(){
    var hasAll = document.querySelector(".search_by_wrp.all")
    if(hasAll){   
        hasAll.classList.remove('all')
    }
}

function removeSingle(){
    var hasSingle = document.querySelector(".search_by_wrp.single")
    if(hasSingle){   
        hasSingle.classList.remove('single')
    }
}

function removeActives(){
    var allActives = document.querySelectorAll(".search_by_wrp .active")
    for(i = 0; i < allActives.length; i++){
        allActives[i].classList.remove('active')
    }
}