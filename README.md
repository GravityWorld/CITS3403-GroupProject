# CITS3403-GroupProject

## Next steps:

Finalise theme for entire website. (Bootstrap)

Group members:

|Name|Github Username|UWA student number|
|----------------|---------------|-----------------|
|Arnav Dangmali|GravityWorld|23408841|
|Dheya Chiha|normalusername|23720753|
|Devarsh Jayendrabhai Patel|devarshp1523|23614429|
|Susheel Utagi|sush-utagi|22502356|

*Note: Arnav Dangmali had their local and global `user.email` variable in `git config` not linked to their GitHub account but their work account hence many commits did **not** show using GravityWorld and the github email. 
This was fixed eventually by linking the alternate account with their account and now all commits appear correctly. 


# About the Website

  SpyderWeb is a live HTML/CSS editor site where users from all around can upload their creative HTML and CSS designs to compete for a spot in the Hall of Fame! 

  **Users can create posts using HTML/CSS using live rendering and view other people's posts too!!  Like a post you see? Just press the heart button and show your appreciation!**



# How to run

  # Setup
  
    This web-app was developed on MAC-OS and the following commands should work on Linux, MacOs and WSL.
    create a virtual environment with the command: python3 -m venv "name of virtual environmnet"
    activate virtual enviornment with the command: source "name of virtual environmnet"/bin/activate

    For Windows:
      python -m venv myenv
      or
      py -m venv myenv
      May need to run the following from Powershell admin to activate the env
      set-executionpolicy remotesigned
      Then to activate the virtual environment run the following:
      myenv\Scripts\activate
      
    The following commands are OS independent.
    install necessary libraries with the command: pip install -r requirements
    run the command export FLASK_APP=appLaunch.py



  # To run

    run the command: flask run
    open localhost link

    NOTE: if `no module error` after installing the dependencies, please deactivate virtual environment with
          `deactivate` and reactivate with `source "name of virtual environmnet"/bin/activate`
  
  # To populate

    to populate database with test data run:
      `python populate_db_fake_data.py`

# How to Use

  1. Start on the homepage for a quick tutorial to the site
  2. Create an account and login, login and signup buttons can be found on the bottom of the side bar in the signup
  3. Navigate to Gallery from the sidebar to see posts by other users. You can also sort by Most Recent, Most Liked, Oldest to Recent. You can like the posts and unlike them too!
  4. **OR** Try and upload your own code for users to view. You will find this on the Upload page form the sidebar. Upload code in two separate text booxes from html and css
  5. **OR** If you are an existing user, view your own posts or download them or even create even better ones!



# How to test

  # For j-unit tests:
    
    run the command:  python3 -m unittest discover tests
    will return number of failed tests
    So far, testing is for accessing pages (with/without athenticaiton), getting the right message when opening a page, basic database commands such as adding, editing Users/Posts

  # For Selenium testing:

    run the command: python -m unittest tests/test_selenium.py

    After running selenium tests please run the following commands to relaunch the app:
        rm -f app.db
        flask db init
        flask db migrate -m "Initial migration."
        flask db upgrade
    
    Then run the app with the following command:
        flask run


## References

Assets from:  
UIVerse:&emsp;&emsp;&emsp;&emsp;&emsp;https://uiverse.io  
MegaTutorials:&emsp;&emsp;https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world  
Chat-GPT:&emsp;&emsp;&emsp;&emsp;&nbsp;https://openai.com/chatgpt/  