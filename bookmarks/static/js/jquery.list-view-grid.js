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



/* 
    Our modal dialog box for editing bookmarks requires us to modify the submit button on the fly
*/

$('.edit-icon').click(function(e) {
    var bookmark_id = $(e.target).attr('data-bookmark-id');
    
    // test code for testing json ajax - returns a JSON obj with the bookmarks data
    $.ajax({ 
        type: 'GET', 
        url: '/api/Lists/g8hjz', 
        // data:  { get_param: '' }, 
        success: function (data) {
            console.log(data); 
        }
    });          
});

/*
    Init code
*/

// set up our sortable and start up in disabled mode
$(function () {
    $('.thumbnail-sortable').sortable({
        placeholderClass: 'col-sm-6 col-md-6' // tells us how big the placeholder blank needs to be
    });

    $('.thumbnail-sortable').sortable('disable'); // start in disabled state   
    
});