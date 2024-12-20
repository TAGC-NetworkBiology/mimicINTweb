
$(document).ready(function(){
    // Showing and hiding tooltip with same speed
    $(".tooltip-tiny").tooltip({
        delay: 500 // show tooltip after 500 milliseconds
    });
    
    // Showing and hiding tooltip with different speed
    $(".tooltip-large").tooltip({
        delay: {show: 500, hide: 500}
    }); 
});