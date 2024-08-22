# ASRJC WA2 Flask Project
## Inspiration
I've been inspired from some websites that are dashboard-like, frequently one screen wide and full of collated data in the home page. I took that approach as I feel that it improves accessibility throughout the page where people do not need to scroll up and down to find the function they would like to use. However, I can't really achieve this functionality yet as if there are too many notes, the screen becomes more than one screen wide, so I hope I can fix the CSS to achieve my intended outcome.

## What it does
The main page is a dashboard which displays data like the Notes / Work Reminders function and buttons that link to other useful functionalities of the website.

### Functionalities
It adds some new functionalities that are currently not in the School Portal which I think may be helpful to students. This includes:
- Notes / Work Reminders
They are essentially the same thing except the former can be for more general use while the latter is to help students set reminders for themselves so that they can keep up with their school work.
- Weather
The weather part uses an API which retrieves Singapore's weather. The first part is for the current weather and the second part shows the weather conditions for the next four days.
- Useful Links
Display hyperlinks that students frequently use to add as convenience for students.

There are also some existing functionalities that are already present in the portal:
- Profile
Not as extensive as the Portal one. Just shows the Name and Email of the person that signed up.
- Calendar
To be honest, this barely does not do much at the time of writing. I was planning to sync the Notes / Work Reminders functionality into the calendar but have not done that yet. The portal already has existing events imported into the calendar so it would be great if I can incorporate that and the Notes / Work Reminders functionality into my calendar.
- Timetable
Currently allows user to attach only on htm file. Can be improved.

## How it's built
Uses Flask from Python alongside HTML, CSS and JavaScript to create the website. You need to install the following for it to work, from requirements.py:
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.32
Flask-Login==0.6.3
requests==2.32.3
Werkzeug==3.0.
gunicorn==20.1.0

## Challenges encountered
Throughout this project, I encountered a few issues and it was not easy to get everything to work. This includes:

1. **Familiarising with Python Modules** - The first main challenge that I had was getting accustomised to Python modules which I had not used before. This mainly includes SQLAlchemy and os Python modules. I took quite a bit of time to understand how they work and how to effectively use them in achieving certain functionalities in my code.

2. **Debugging** - I spent slightly more than an hour trying to get the timetable functionality to work and I was getting unhappy the longer I took trying to get it to work. The issue was that the attached file by the user was going to a folder 'static/uploads' that was **OUTSIDE** my 'website' folder (instead of the actual 'static/uploads' folder inside the 'website' folder that Flask was using) which kept on causing the webpage to not be able to find the uploaded document. By the way, I was using the os Python module for this timetable functionality which I basically knew nothing about before embarking on this project so it was probably why I committed such a rookie mistake.

3. **CSS** - As mentioned earlier, I am aiming to make the home page of my website dashboard-like, so that it only occupies one screen. Even after asking AI countless amount of times (as it takes a lot of time just learning much of CSS and even more typing hundreds of lines for this project), I still could not get a favourable answer for it to limit the screen accordingly after adding multiple notes in the 'Notes / Work Reminders' route. The screen just extends downwards after the notes take up too much space and this also affects the buttons so hopefully I can get it to work in the near future. 

4. **Deploying** - I have never deployed a website before so I had initially had issues setting it up. I am using railway and it was a rather smooth process until I kept on getting an application error on the next day. It was working the night before but stopped working the day when I needed to submit it to my teacher for reviewing so I was frantic and it took me over 2 hours to realise that it was deployed on another port which was why I could not access it.

## Accomplishments that I'm proud of
I am definitely proud of successfully getting the main features that I wanted to implement in the first place work, though some definitely can be optimised. I am also proud that I was able to learn and apply new concepts that I have learnt into this project.

## What I learned
Just like the saying goes along the lines of how failures makes one stronger, the challenges that I have encountered have definitely taught me an invaluable lesson. I have learnt to use other common Python modules like datetime, os, requests and SQLAlchemy. The debugging processes that took me over an hour to fix which even AI could not help me with would definitely still remain in my mind in the near future. Learning how to use APIs would also be another benefit and since I do not use Visual Studio Code (VSC) in school, I also learnt more about how VSC works and its various functions (No wonder it is so many peoples' go-to!).

## What's next for this Student's Portal Extension project?
I made this as an extension to my school's portal, taking a more personalised approach to it where students can create notes, reminders for themselves that will be displayed once they log in and other features that others may find useful. I planned to add much more Quality-of-life features but was not able to do so and only created the most basic features. Here are some features that I may add in the future (from easy to hard):
1. Add descriptions for relevant functionalities
2. Include more useful links (Could also limit based on student's subjects)
3. Create a password reset route
4. Include two timetables for odd / even weeks
5. /notes/<id> allows students to open the whole note
6. Note deletion by id
7. Include machine learning to predict weather
8. Make the calendar more useful by incorporating deadlines and school events

## Credits
I would like to thank Tech with Tim, a considerable chunk of my code actually comes from his two hour long Flask youtube video which was both informative and helpful.
I would also like to thank my teacher for opening up my horizons about full stack development with such a project.
