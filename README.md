# Proof of Concept requirements - For first initial deployment
    - Has some sort of identifying brand which matches the domain name
    - Has a home page explaining how to use the service
    /- Can sign up and create a login/user id
    /- Can log in / log out
    - Can create lists when logged in, can't create lists when not logged in
        - LinkBoard page must have an add and delete function. When empty it have a message saying "add a page now"
    - Can modify their lists when logged in, can't modify lists when not logged in
        /- Edit button edits the link in real time
        /- Delete button deletes the link in real time
        /- Create button creates a new link, doesn't have to be real time
        / - User can drag and drop the items in the list to customise order, preference is stored in the database
        /- Simple text entry for link creation is fine
        - Creating a link without a thumbnail will insert a placeholder image
        - User can modify the name of their list by clicking the pencil icon next to the list title header
    - Mobile friendly (Looks good so far, but there is an issue with the hover effect not working on mobile device (no such thing as hover?). Also login/logout button shouldn't collapse into the hamburger menu)
    - Complete set of unit testing (do a quick audit even)
    - Complete set of functional tests (within reason)
    - In your deployment script, alter Debug=False and disable the admin registrations

# Known Bugs
    UNRESOLVED- try logging in after signing up, it can create an error. unless it has something to do with me being logged into admin page?
    UNRESOLVED - Links without a HTTP prefix does not hyperlink correctly. A check should happen server side
    FIXED - After you edit a page, it seems to update all A hrefs on the page? Or at least when clicking on another edit icon it shows there. How come? 
    UNRESOLVED - when editing a bookmark, pressing enter does nothing


# Features to implement in future releases
    - LinkBoard page should prompt login if not authenticated
    - Shows 'signed in as' identifier in right hand corner
    - Edit button for linkboard name
    - Copy button puts the url on the clipboard
    - Probably a good idea to use a Captcha to ensure people can't just use a bot to create their own pages. We have space for 60M bookmark lists
    - Re-Look at our list save method for the url_id hashing function, can we catch other exceptions and maybe do some logging? How can we test this a bit more for robustness 
    - On Sign up, the verify password field has not yet been set up
    - Can we create any automated testing for our JQuery code? What about the GUI aspect such as drag and drop, etc.
    - Test to see what injection someone can do with our input. E.g could they input some javascript into the page title? Django has autoescaping to resolve this
     - We should come up with better terminology for List. It's not user friendly
