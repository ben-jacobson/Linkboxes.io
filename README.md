# Features to implement in future releases
	P - App should automatically source a thumbnail for the user
	- Mobile friendly (Looks good so far, but there is an issue with the hover effect not working on mobile device (no such thing as hover?). Also login/logout button shouldn't collapse into the hamburger menu)
	- Give users a slider to change the size of their thumbnails, e.g have 2,3,4,5 links per row
	- Can we create any automated testing for our JQuery code? What about the GUI aspect such as drag and drop, etc.
	- Create a set of functional tests	
	/ - LinkBoard page should prompt login if not authenticated
	- Shows 'signed in as' identifier in right hand corner
	- Edit button for linkboard name in bookmarks listview
	- Copy button should put the url on the clipboard
	- Probably a good idea to use a Captcha to ensure people can't just use a bot to create their own pages. We have space for 60M bookmark lists
	- Re-Look at our list save method for the url_id hashing function, can we catch other exceptions and maybe do some logging? How can we test this a bit more for robustness 
	/ - On Sign up, the verify password field has not yet been set up
	- Test to see what injection someone can do with our input. E.g could they input some javascript into the page title? Django has autoescaping to resolve this
	- Refactor the code to make use of the new LinkBoxes terminology
	- Change Gunicorn and NGINX allowed hosts to only accept requests from linboxes.io
	- When signing in as a new user, needs to generate a confirmation email
	- We'll need an SSL, a privacy policy and a GDPR popup

# Known Bugs
	- our opengraph parse package doesn't include the dependancies, also it can't just be accessed like from opengraph_parse import parse_page. instead you have to type opengraph_parse.opengraph_parse import parse_page
	-Too easy to exceed rate limited on linkpreview.net
	-GA tags should not be loaded on linkboxes
	- When you click add new, something in sortable.js throws an error in the console. 
	-If an image can't load, it should replace with placeholder
	-attempting to load the page without a WWW doesn't load.
	-Should get an SSL set up
	-Grid view needs to letter box/crop images if they are not big enough vertically / too large
	- Site throws an error if you include a trailing '/' in front of URLs	
	- Putting in a new link will not overwrite thumbnail unless blank. This is odd because it works with titles fine. 
	- Thumbnail generator will only allow for 60 per hour. Need to find a service that doesn't have this limitation, or even stand up our own server for this. 	
	- FIXED - Bookmarks Listview doesn't care who you are logged in as, login as another user and you can modify other peoples links.
	- FIXED - Signup page does not log user in
	- FIXED - Bookmarks without a HTTP prefix does not hyperlink correctly. A check should happen server side
	- FIXED - The Backend doesn't care what user you are, creating a new linkboard for any user is possible no matter who you are logged in as.
	- FIXED - After you edit a page, it seems to update all A hrefs on the page? Or at least when clicking on another edit icon it shows there. How come? 
	- FIXED - when editing a bookmark, pressing enter does nothing
	- FIXED - pressing enter when editing a linkboard has some strange behaviour
