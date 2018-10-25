This is the second version of an application to set and deliver matching to sample trials with different options of delay, set of stimuli and participant.

Tkinter was used as GUI on Python 3.

The application retrives images from folders to set the trials. User will choose which categorie of images will be used for trials. A preset of images is offered in "images" folder. New categories and images can be added creating new folders and adding the images.
User must chose the participant for that session from a list in a combobox. Names on the list are the names of folders in "participants" folder. To add new participants, create a folder with his name in "participants" folder.
User has to pick the delay (0, 2, 5, 10, 20) he wants between an observation response on the sample and comparissons stimuli onset.

When user press "start" button, the application will generate a .csv file with randomized trials to be used in runtime. User can either chose the time delay  between observation response and onset of comparisson stimuli.

An observation response is required in the sample image to go forward and show the comparissons. User can respond either with the mouse or in a touch screen.

A .csv log file will register for each trial: the sample stimulus, the position of chosen comparisson, if it was a correct or incorrect response and totals of correct and incorrect responses. One log file will be created for each session for each partipant in his folder.