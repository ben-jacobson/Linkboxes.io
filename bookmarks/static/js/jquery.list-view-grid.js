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
    UI events
*/

// event when the user has finished re-arranging their icons
$('.thumbnail-sortable').sortable().bind('sortupdate', function() {  // for some reason, binding something to sortupdate, makes the click and drag feature really clunky
    console.log('trigger drop');
    // get the order of the elements

    // get their ID's

    // Make the AJAX call for the update
});


// event when user clicks the edit button
$('.edit-icon').click(function(e) {
    var bookmark_id = $(e.target).closest('.bookmark-card').attr('data-bookmark-id');
    var list_slug = $(e.target).closest('.bookmark-card').attr('data-list-slug');

    // First thing is that the DOM on Chrome and Firefox won't allow you to overwrite form values after user entry. This is a a workaround
    $('#edit-form').trigger("reset");

    // put the bookmark id and list slug data into the modal so that the save method can read it
    $('#editBookmarkModal').attr('data-bookmark-id', bookmark_id);
    $('#editBookmarkModal').attr('data-list-slug', list_slug);

    // AJAX request to retrieve the bookmarks data from the api
    $.ajax({ 
        type: 'GET', 
        url: '/api/Lists/' + list_slug + '/',
        success: function (data) {
            bookmark_data = data['bookmarks'].filter(function(bookmark) {
                return bookmark['id'] == bookmark_id;  // return True/False
            })[0];

            // update the modal form data
            $('#edit-title').attr('value', bookmark_data['title']);
            $('#edit-url').attr('value', bookmark_data['url']);
            $('#edit-thumbnail').attr('value', bookmark_data['thumbnail_url']);            
        }
    });
});

// event when user clicks the save button in the edit modal.
$('#edit-modal-save').click(function(e) {
    var bookmark_id = $(e.target).closest('#editBookmarkModal').attr('data-bookmark-id');
    var csrfToken =  $('input[name="csrfmiddlewaretoken"]').attr('value');

    // Read the form data and put the data into a JSON obj
    var json_data = {
        'title':         $('#edit-title').val(), 
        'url':           $('#edit-url').val(),
        'thumbnail_url': $('#edit-thumbnail').val(),
    };

    // set up the AJAX request, inject the CSRF token
    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }
    });    

    // run the AJAX request to save the data
    $.ajax({ 
        type: 'PATCH',        
        url: '/api/Bookmark/' + bookmark_id + '/',    
        data: json_data,
        success: function (data) {
            // update the page and close the modal. 
            $('#editBookmarkModal').modal('toggle');

            // we still have the json data available, use that to update the page element itself, rather than force a refresh. 
            var bookmark_elem = $('div[class*="bookmark-card"][data-bookmark-id="' + bookmark_id + '"]'); // find the element
            bookmark_elem.find('h3').html(json_data['title']); // update the title
            bookmark_elem.find('a').attr('href', json_data['url']); // update all hyperlinks found on page (normally 2)
            bookmark_elem.find('img.bookmark-thumbnail').attr('src', json_data['thumbnail_url']); // update the image thumbnail 
        }
    });   
}); 

// event when user clicks the delete button
$('.delete-icon').click(function(e) {
    var bookmark_elem = $(e.target).closest('.bookmark-card');
    var bookmark_id = bookmark_elem.attr('data-bookmark-id');
    var csrfToken =  $('input[name="csrfmiddlewaretoken"]').attr('value');

    // set up the AJAX request, inject the CSRF token
    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }
    });   

    // AJAX request to delete the bookmarks data from the api
    $.ajax({ 
        type: 'DELETE', 
        url: '/api/Bookmark/' + bookmark_id + '/',    
        success: function () {
            // update the page remove the element from the screen
            $(bookmark_elem).remove();
        }
    });

});

// event when user clicks the copy icon
$('.copy-icon').click(function(e) {
    //var bookmark_id = $(e.target).closest('.bookmark-card').attr('data-bookmark-id');
    //var bookmark_url = $(e.target).closest('.bookmark-card').find('a')[0].attr('href', json_data['url']); // update all hyperlinks found on page (normally 2)

    alert('Feature coming soon');
    // get the data from the element on page, not from the server - this is a resource saving exercise
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