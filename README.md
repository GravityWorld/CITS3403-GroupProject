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


# How to run

  # Setup
  
    create a virtual environment with the command: python3 -m venv "name of virtual environmnet"
    activate virtual enviornment with the command: source "name of virtual environmnet"/bin/activate
    install necessary libraries with the command: pip install -r requirements
    run the command export FLASK_APP=appLaunch.py

  # To run

    run the command: flask run
    open localhost link
  
  # To populate

    ////

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
