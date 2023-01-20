# Final Project of Lucas Fremanger for CS50W

# Website to be used by a board game association

### Distinctiveness and Complexity

This project was built from scratch by me. I created it to provide support to the board game association I was creating at the same time.
It is distinct from all the course's projects because it is in no way similar to an e-commerce website, mail app, search engin or wiki website.

It does use some (granted not all) of the functionnalities I learned through this course and its projects.
For instance, it uses AJAX to automaticaly send email.

It was tricky (for me, at least) to implement as I had to do a lot of side research, using CS50W course as a fundation, in order to implement all the features I had in mind or that simply appeared during developpement.
For instance, I spend a bit of time understading how Django password reset feature works and the handling of image file through a Django form.
I do believe the number of features is enough to prove the complexity of it, even though I am still an amateur.

## Files and features description
### settings.py

Under MEDIA_ROOT you'll find and be able to configure the default route used for the games art.

At the end is the email server configuration. It will be emptied of all parameters before upload to Github.

### models.py

We start with the creation of a list of game categories. They will be used by the Game model defined below. This list can easily be modified without impact on the rest.

Then is a customisation of the base User model to add phone number and adress

Followed by the custom Game model. It will be used in the website to record and display the different games available in our association

Finaly we have the custom News model, used by the association staff to publish short texts on the index page. They will provide information about the association special events or whatever.

At the end are the four custom ModelForms used by users to interact with the website.

### urls.py

Contains all the path accessed when using the application

### views.py

**Index**
The GET method will display the index page
The POST method will allow staff to post news

**Register**
The GET method will display the registration form
The POST method will create a new account acording to the information provided bu the new user

**Logout**
Simply logs you out

**Login**
The GET method displays the login page. A link to reset your forgotten password is also provided.
The POST method logs you in if the credentials are correct. If not, an error message is displayed

**Profil**
The GET method will show the user profil page. As the user can switch between different sections inside this one page, it is provided with multiple informations through the view : the games the user has registered and the different categories of games. The user can switch between :
1. Personnal informations, from which they can :
    * Edit their info
    * Change their password
2. Add a game to the association catalog
3. View all the games they have registered
4. If they have a 'staff' status, write a news that will be display on the index page.

The POST method allows the user to register a new game.

**Catalog**
Displays a list of all games available.

**Game**
Displays the details of a specific game.

**Contact**
The GET method displays the contact form.
The POST method uses the ContactForm model to validate inputed data and then send an email to the association email. The receiver email adress is stored there.

**Modify**
Used to permit users to modify their information or their password

**Remove**
Used with AJAX to remove a game form the association catalog

**Modify Game**
The GET method displays a form prefilled with the game details to make it easy for the user to change what they want.
The POST method edits this game details.

**Game Request**
This view allows users to signal to the association staff that they'd like to request a particular game to be available at the association next meeting.


## Folders
### Media
Where the game art is stored

### Static
Where you'll find the css, javascript and images used by the application

**scripts.js**
A couple of functions are defined there :
1. Anonymous function to provide the animation of the navigation menu.
2. getCookie to retrieve the CSRF Token. Used in the AJAX calls.
3. pass to check password and confirmation are identical, client-side
4. remove_game, delete game from catalog with AJAX call to avoid reloading the whole page
5. game_request, automatically send an email to the association staff to request a game

### Templates
All the html templates used in this web app




