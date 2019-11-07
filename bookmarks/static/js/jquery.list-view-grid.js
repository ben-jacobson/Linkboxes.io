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

function populate_bookmark_form(bookmark_data) {
    // console.log('updating the form to include the bookmark data');
    // console.log(bookmark_data);
    $('#edit-title').attr('placeholder', bookmark_data['title']);
    $('#edit-url').attr('placeholder', bookmark_data['url']);
    $('#edit-thumbnail').attr('placeholder', bookmark_data['thumbnail_url']);
}

function update_bookmark(id) {
    console.log('run the ajax request to the update endpoint')
}

$('.edit-icon').click(function(e) {
    var bookmark_id = $(e.target).attr('data-bookmark-id');
    var list_slug = $(e.target).attr('data-list-slug'); // should we change this to inherit from the parent? 

    // AJAX request to retrieve the bookmarks data from the api
    $.ajax({ 
        type: 'GET', 
        url: '/api/Lists/g8hjz',    // todo - get this data off the page somehow
        success: function (data) {
            bookmark_data = data['bookmarks'].filter(function(bookmark) {
                return bookmark['id'] == bookmark_id;
            })[0];
            populate_bookmark_form(bookmark_data);
        }
    });
    
    // register an event to listen to the edit icon button being pressed and trigger update_bookmark
    // $('#save-button')
    //console.log(list_slug);
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