/*
For enabling the list view drag and drop
*/

// set an event - when you hover over the move icon, enables dragging and dropping
$('.move-icon').mouseenter(function () {
    $('.thumbnail-sortable').sortable('enable');
});

// set an event - when you leave the move icon, disables dragging and dropping
$('.move-icon').mouseleave(function () {
    $('.thumbnail-sortable').sortable('disable');
});

// set up our sortable and start up in disabled mode
$(function () {
    $('.thumbnail-sortable').sortable({
        placeholderClass: 'col-sm-6 col-md-6' // tells us how big the placeholder blank needs to be
    });

    $('.thumbnail-sortable').sortable('disable'); // start in disabled state   
});

/*
For displaying and hiding the edit lightbox
*/

$('.open-button').click(function () {
    if ($('.edit-form').css('display') == 'none') {
        $('.edit-form').css('display', 'block');
    }
    else {
        $('.edit-form').css('display', 'none');
    }
});