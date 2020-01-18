/*
    Create linkboard events
*/



/*
    Edit linkboard events
*/

// user clicks the edit icon next to their linkboard
$('.link-board-edit-icon').click(function(event) {
    // when clicking the edit icon, populate the placeholer
    var list_name = $(event.target).closest('tr').attr('data-list-name');
    $('#rename-linkboard-form').trigger("reset");
    $('#edit-board-title').attr('value', list_name);

    // populate a data field so that the modal save knows list it is operating on
    var list_slug = $(event.target).closest('tr').attr('data-list-slug');
    $('#editLinkBoardModal').attr('data-list-slug', list_slug);
});

// In the edit modal, user clicks the save button
function rename_bookmark() {
    // get the list slug
    var list_slug = $("#editLinkBoardModal").attr('data-list-slug');    

    // Read the form data and put the data into a JSON obj
    var json_data = {
        'title':         $('#edit-board-title').val(), 
    };    

    // set up the AJAX header, with the CSRF token
    var csrfToken =  $('input[name="csrfmiddlewaretoken"]').attr('value');

    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }
    });     

    // run the AJAX request to save the data
    $.ajax({ 
        type: 'PATCH',        
        url: '/api/Lists/' + list_slug + '/',    
        data: json_data,
        success: function (data) {
            // update the page and close the modal. 
            $('#editLinkBoardModal').modal('toggle');

            // update the page
            var linkboard_title_elem = $('tr[data-list-slug="' + list_slug + '"]');
            linkboard_title_elem.attr('data-list-name', json_data['title']);
            linkboard_title_elem.find('a').html(json_data['title']);
        }
    }); 
    
    return false; // to stop the browser from redirecting.
}

// on the rename modal, if the user clicks the save button, or presses enter, trigger the rename_bookmark event
$('#edit-modal-save').click(rename_bookmark);   
$('#rename-linkboard-form').submit(rename_bookmark);

/*
    Delete linkboard events
*/

// when the user clicks the delete icon, the modal is activated and populated
$('.link-board-delete-icon').click(function(event) {
    // find which list we are deleting
    var list_slug = $(event.target).closest('tr').attr('data-list-slug');
    $('#confirmDeleteLinkBoardModal').attr('data-list-slug', list_slug);

    // populate the modal title
    var list_name = $(event.target).closest('tr').attr('data-list-name');
    $('h5.delete-modal-title').html("Are your sure you want to delete '" + list_name + "'");
}); 


// when the confirm delete modal is on screen, if the user clicks confirm or presses enter, delete the bookmark
$('#delete-modal-confirm').click(function() {
    // find which list we are deleting
    var list_slug = $("#confirmDeleteLinkBoardModal").attr('data-list-slug');    

    // set up the AJAX request, inject the CSRF token
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').attr('value');
    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }
    });   

    // AJAX request to delete the bookmarks data from the api
    $.ajax({ 
        type: 'DELETE', 
        url: '/api/Lists/' + list_slug + '/',    
        success: function () {
            // update the page remove the element from the screen
            $('tr[data-list-slug="' + list_slug + '"]').remove();
        }
    });
}); 

// if the user presses the enter key when the modal is active
$('#confirmDeleteLinkBoardModal').on('keypress', function (event) {  
    var keycode = (event.keyCode ? event.keyCode : event.which);
    var keycode_enter = 13; 

    if (keycode == keycode_enter) {
        $('#delete-modal-confirm').click();   
    }
});

