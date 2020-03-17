# Known Bugs
	- If you manually alter the content of the image url or the title, then copy and paste new content into the url field, it won't auto update, just need to reset the form 	

# Features to implement in future releases
	- Make it so that the deploy script can deploy to a staging server run only within the house. E.g a raspberry pi
	- publicize the repo, change the settings.py file to read from secrets, tighten up our repo to ensure nothing secret is on there and then change to public
	- When signing in as a new user, needs to generate a confirmation email
	- set up a confirmation box for deleting bookmarks, not just for entire linkboxes
	- Set up private linkboxes that require authentication to view
	- Google Analytics tags should not be loaded on linkboxes
	- If an image throws a 404 or 500 error, it should replace with placeholder by the JS
	- Mobile friendly (Looks good so far, but there is an issue with the hover effect not working on mobile device (no such thing as hover?		). Also login/logout 	button shouldn't collapse into the hamburger menu)
	- Give users a slider to change the size of their thumbnails, e.g have 2,3,4,5 links per row
	- Can we create any automated testing for our JQuery code? What about the GUI aspect such as drag and drop, etc.
	- Create a set of functional tests	
	- Shows 'signed in as' identifier in right hand corner of screen
	- Edit button for linkboard name in bookmarks listview
	- Copy button should put the url on the clipboard
	- Probably a good idea to use a Captcha to ensure people can't just use a bot to create their own pages. We have space for 60M bookmark lists
	- Re-Look at our list save method for the url_id hashing function, can we catch other exceptions and maybe do some logging? How can we test this a bit more 		for robustness 
	- Test to see what injection someone can do with our input. E.g could they input some javascript into the page title? Django has autoescaping to resolve this
	- Refactor all code to make use of the new LinkBoxes terminology
	- Change Gunicorn and NGINX allowed hosts to only accept requests from linboxes.io, not from the aws
	- We'll need an SSL, a privacy policy and a GDPR popup