/* 
    Helper functions
*/ 

function ajax_request_set_new_list_order(list_id, new_order) {
    var csrfToken =  $('input[name="csrfmiddlewaretoken"]').attr('value');
    var json_data = JSON.stringify({'new_order': new_order});

    // set up the AJAX request, inject the CSRF token
    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }   
    });    

    // run the AJAX request to save the data
    $.ajax({ 
        type: 'PATCH',        
        url: '/api/Lists/' + list_id + '/reorder/',    
        data: json_data,
    }); 
}

// debounce lifted from underscore
function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
}

/*
    Global Variables
*/
var sortable_js = null;
const DEFAULT_THUMBNAIL_IMAGE_HREF = 'https://bookmark-static.s3.amazonaws.com/no_thumbnail.jpg';

/*
    For enabling the list view drag and drop
*/

$(document).ready(function() { 
    // set up our sortable thumbnails
    sortable_js = new Sortable($('#thumbnail-container')[0], {
        disabled: true,         // start disabled, we use the move icons to make this work 
        animation: 150,
        ghostClass: 'sortable-drop-placeholder',
        onUpdate: function() {
            // get a list of bookmarks and extract the IDs
            var new_order = [];
            $('.bookmark-card').filter(function(e) {
                //console.log(e.attr('data-bookmark-id'));
                order = $(this).attr('data-bookmark-id');
                new_order.push(parseInt(order));
            });
            ajax_request_set_new_list_order($('#thumbnail-container').attr('data-list-slug'), new_order);
        },
    });
});

/*
    UI events
*/

// set an event - when you hover over the move icon, enables dragging and dropping
$('.move-icon').mouseenter(function () {
    //console.log('enable sorting');
    sortable_js.option("disabled", false);
});

// set an event - when you leave the move icon, disables dragging and dropping
$('.move-icon').mouseleave(function () {
    // TODO - we only want to disable sorting if we are actually finished sorting.
    //console.log('disable sorting');
    sortable_js.option("disabled", true);      
});

// event when the user clicks the + button to add a new link

$('#create-new-bookmark-button').click(function() {
    // reset the image
    $('#create-thumb-preview').attr('src', DEFAULT_THUMBNAIL_IMAGE_HREF);
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
            //$('#edit-title').attr('value', bookmark_data['title']);
            //$('#edit-url').attr('value', bookmark_data['url']);
            //$('#edit-thumbnail').attr('value', bookmark_data['thumbnail_url']);   
            
            $('#edit-title').val(bookmark_data['title']);
            $('#edit-url').val(bookmark_data['url']);
            $('#edit-thumbnail').val(bookmark_data['thumbnail_url']);               
            
            // update the thumbnail while there
            update_thumbnail_in_modal_by_src($('#edit-thumbnail'), bookmark_data['thumbnail_url']);
        }
    });
});

function update_bookmark_card_details(bookmark_id) {
    // Reads bookmark data from the server via a GET request
    $.ajax({ 
        type: 'GET',        
        url: '/api/Bookmark/' + bookmark_id + '/',    
        success: function (data) {
            var bookmark_elem = $('div[class*="bookmark-card"][data-bookmark-id="' + bookmark_id + '"]'); // find the element        
            bookmark_elem.find('h3').html(data['title']); // update the title
            bookmark_elem.find('a').attr('href', data['url']); // update all hyperlinks found on page (normally 2)
            bookmark_elem.find('img.bookmark-thumbnail').attr('src', data['thumbnail_url']); // update the image thumbnail 
        }
    }); 
}

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
            update_bookmark_card_details(bookmark_id);
        }
    });   

    return false; // to stop the browser from redirecting.
}); 

// if the user presses the enter key when the modal is active
$('#editBookmarkModal').on('keypress', function (event) {  
    var keycode = (event.keyCode ? event.keyCode : event.which);
    var keycode_enter = 13; 

    if (keycode == keycode_enter) {
        $('#edit-modal-save').click();   
    }
});

// event when user clicks the delete button
$('.delete-icon').click(function(e) {
    var bookmark_elem = $(e.target).closest('.bookmark-card');
    var bookmark_id = bookmark_elem.attr('data-bookmark-id');
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').attr('value');

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

    console.log('Feature coming soon');
    // get the data from the element on page, not from the server - this is a resource saving exercise
});


// event when user updates the url field
var get_thumbnail_of_url = debounce(function (elem) {
    var target_url = $(elem.target).val();
    
    $.ajax({
        url: '/get_preview?url=' + target_url,
        success: function (response) {
            if (response) {
                // update the title and thumbnail url fields 
                $(elem.target).closest('div.modal').find('.form-title').val(response.title);
                $(elem.target).closest('div.modal').find('.form-thumb').val(response.image);
                                            
                // update the image thumbnail
                update_thumbnail_in_modal_by_src(elem.target, response.image);
            }            
        },
    });
}, 500);

$('input[id=edit-url]').on('change paste keyup', get_thumbnail_of_url);
$('input[id=create-url]').on('change paste keyup', get_thumbnail_of_url);

// event when user updates the thumbnail field

function update_thumbnail_on_modal_update(elem) {
    var image_src = $(elem.target).val();
    update_thumbnail_in_modal_by_src(elem.target, image_src);
}

function update_thumbnail_in_modal_by_src(elem, img_src) {   
    var modal_elem = $(elem).closest('div.modal');
    var thumbnail_img_elem = $(modal_elem).find('.link-preview-thumb');  
    thumbnail_img_elem.attr('src', img_src);
}

$('input[id=edit-thumbnail]').on('change paste keyup', update_thumbnail_on_modal_update);
$('input[id=create-thumbnail]').on('change paste keyup', update_thumbnail_on_modal_update);
