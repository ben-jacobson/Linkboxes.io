$(document).ready(function() { 

});


// user clicks the edit icon next to their linkboard
$('.link-board-edit-icon').click(function(e) {
    // when clicking the edit icon, we just need to populate the placeholer
    var list_name = $(e.target).closest('tr').attr('data-list-name');
    $('#rename-linkboard-form').trigger("reset");
    $('#board-title').attr('value', list_name);

    // TODO - create an AJAX request for editing
});

$('.link-board-delete-icon').click(function(e) {
    var list_slug = $(e.target).closest('tr').attr('data-list-slug');
    console.log('deleting ' + list_slug);

    // TODO - create an AJAX request for deleting
});