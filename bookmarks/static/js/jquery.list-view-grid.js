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

// Helper functions

function populate_bookmark_form(bookmark_data) {
    $('#edit-title').attr('value', bookmark_data['title']);
    $('#edit-url').attr('value', bookmark_data['url']);
    $('#edit-thumbnail').attr('value', bookmark_data['thumbnail_url']);
}

function update_bookmark(id) {
    console.log('run the ajax request to the update endpoint')
}

// Click the edit button
$('.edit-icon').click(function(e) {
    var bookmark_id = $(e.target).closest('.bookmark-card').attr('data-bookmark-id');
    var list_slug = $(e.target).closest('.bookmark-card').attr('data-list-slug');

    // put the bookmark id and list slug data into the modal so that the save method can read it
    $('#editBookmarkModal').attr('data-bookmark-id', bookmark_id);
    $('#editBookmarkModal').attr('data-list-slug', list_slug);

    // AJAX request to retrieve the bookmarks data from the api
    $.ajax({ 
        type: 'GET', 
        url: '/api/Lists/' + list_slug + '/',    // todo - get this data off the page somehow
        success: function (data) {
            bookmark_data = data['bookmarks'].filter(function(bookmark) {
                return bookmark['id'] == bookmark_id;  // return True/False
            })[0];
            populate_bookmark_form(bookmark_data);
        }
    });
});

// When the modal dialog box is open, click the save button
$('#edit-modal-save').click(function(e) {
    var bookmark_id = $(e.target).closest('#editBookmarkModal').attr('data-bookmark-id');
    var csrfToken =  $('input[name="csrfmiddlewaretoken"]').attr('value');

    // Read the form data and put the data into a JSON obj
    var json_data = {
        'title':         $('#edit-title').val(), 
        'url':           $('#edit-url').val(),
        'thumbnail_url': $('#edit-thumbnail').val(),
    };

    // set up the AJAX request
    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }
    });    

    // run the AJAX request to save the data
    $.ajax({ 
        type: 'PATCH',        
        url: '/api/Bookmark/' + bookmark_id + '/',    // todo - get this data off the page somehow
        data: json_data,
        success: function (data) {
            console.log('saved, close the window and update the page');
        }
    });    
}) 

// Click the delete button
$('.delete-icon').click(function(e) {
    var bookmark_elem = $(e.target).closest('.bookmark-card');
    var bookmark_id = bookmark_elem.attr('data-bookmark-id');
    var list_slug = $(e.target).closest('.bookmark-card').attr('data-list-slug');

    $(bookmark_elem).remove();

    // run ajax request
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