// ---------horizontal-navbar-menu-----------
var tabsNewAnim = $('#navbar-animmenu');
var selectorNewAnim = $('#navbar-animmenu').find('li').length;
//var selectorNewAnim = $(".tabs").find(".selector");
var activeItemNewAnim = tabsNewAnim.find('.active');
var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
var itemPosNewAnimLeft = activeItemNewAnim.position();
$(".hori-selector").css({
    "left":itemPosNewAnimLeft.left + "px",
    "width": activeWidthNewAnimWidth + "px"
});
$("#navbar-animmenu").on("click","li",function(e){
    $('#navbar-animmenu ul li').removeClass("active");
    $(this).addClass('active');
    var activeWidthNewAnimWidth = $(this).innerWidth();
    var itemPosNewAnimLeft = $(this).position();
    $(".hori-selector").css({
        "left":itemPosNewAnimLeft.left + "px",
        "width": activeWidthNewAnimWidth + "px"
    });
});

// navbar.js
$(document).ready(function() {
    // ... your existing navbar animation code ...

    // Handle tab switching
    $("#navbar-animmenu li").on("click", function() {
        // 1. Remove 'active' class from all navbar items and content sections
        $("#navbar-animmenu li").removeClass("active");
        $(".content").removeClass("active");

        // 2. Add 'active' class to the clicked navbar item and its target content
        $(this).addClass("active"); 
        $($(this).data("target")).addClass("active"); 
    });
});