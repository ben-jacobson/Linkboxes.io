# Known Bugs
	FIXED - Attempting to load the page without a WWW doesn't load.
	FIXED - Grid view needs to letter box/crop images if they are not big enough vertically / too large
	FIXED - Site throws an error if you include a trailing '/' after URLs	

# Features to implement in future releases
	- What else can we do to reduce hosting costs?
	- Set up private linkboxes that require authentication to view
	- Google Analytics tags should not be loaded on linkboxes
	- If an image throws a 404 or 500 error, it should replace with placeholder by the JS
	- Make it so that the deploy script can deploy to a staging server run only within the house
	FIXED - App should automatically source a thumbnail for the user
	- Mobile friendly (Looks good so far, but there is an issue with the hover effect not working on mobile device (no such thing as hover?		). Also login/logout button shouldn't collapse into the hamburger menu)
	- Give users a slider to change the size of their thumbnails, e.g have 2,3,4,5 links per row
	- Can we create any automated testing for our JQuery code? What about the GUI aspect such as drag and drop, etc.
	- Create a set of functional tests	
	FIXED - LinkBoard page should prompt login if not authenticated
	- Shows 'signed in as' identifier in right hand corner
	- Edit button for linkboard name in bookmarks listview
	- Copy button should put the url on the clipboard
	- Probably a good idea to use a Captcha to ensure people can't just use a bot to create their own pages. We have space for 60M 			bookmark lists
	- Re-Look at our list save method for the url_id hashing function, can we catch other exceptions and maybe do some logging? How can we 		test this a bit more for robustness 
	FIXED - On Sign up, the verify password field has not yet been set up
	- Test to see what injection someone can do with our input. E.g could they input some javascript into the page title? Django has 		autoescaping to resolve this
	- Refactor the code to make use of the new LinkBoxes terminology
	- Change Gunicorn and NGINX allowed hosts to only accept requests from linboxes.io
	- When signing in as a new user, needs to generate a confirmation email
	- We'll need an SSL, a privacy policy and a GDPR popup