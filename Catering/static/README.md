# So You Think You Can Cater -- <Replace with your name>Joe Reidell

Name: <Full Name>Joseph Reidell

Pitt ID: <ID>JMR240

## Installation

Instructions to get your code up and running.
  1. Start up a virtual enviroment
  2. run "pip install -r requirements.txt"
  3. run "export FLASK_APP=catering.py"
  4. run "flask initdb"
  5. run "flask run"
  6. Go to localhost:5000

## Running the App

Instructions to run your application.
  1. On the login page, enter in username: owner, and in password: pass.
  2. Upon entering the owner page, you can either look at a list of events, or create a staff account. There should be no        event list displayed for now. A message should say there isn't any at this time.
  3. If you want to create a staff account, click the link and enter in a username and password. After hitting enter, you        will be taken back to the owner page.
  4. In the top right there is a log out button that will take you back to the login screen.
  5. On the login page, below username and password, you can create a customer account.
  6. If you want to create a customer account, click the link and enter in a username and password. After hitting enter, you      will be taken back to the login page.
  7. You can either then enter in the staff account username and password or the customer account username and password and      go to those pages.
  8. On the customer page, there is two entries to enter in an Event Title and an Event Date. You can enter whatever you          want there. Below that is a link to cancel an event. If you try to cancel something that isn't there, it will throw an      error. If you create an event, refresh the page and you will see the event appear on the customer page.
  9. Once you are done their, if you haven't already, look at the staffer account login. One bug here, it will not display        the events that the staffer can apply for. I've tried all sorts of things but, I can't get it to show up. Usually a          radio button of the event should pop up and the staffer can pick that and register for the event. 
  10. You can log out from there and log back into the owner page. On the owner page the list of events should display with       the Event Title and the Event date it was registered on. 

## Note

  If the same username(like using "owner" twice) is used, the query breaks and the whole program stops working.
