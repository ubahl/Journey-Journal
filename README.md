# Journey Journal
> "Its about journaling the journey; not destining your destination"

**A COMS W4111 Project by Uma Bahl & Abram Kremer**

When Uma and Abram first arrived in New York City, they were astounded by the complicated, yet beautiful, subway system. So when the opportunity arose to model such a system to track their fun subway adventures, they jumped to the task. We present *Journey Journal,* a web application where commuters can add and view subway journeys.

## PostgreSQL Account
The database resides on `ank2177`.

## URL of Web Application
The web application is hosted on _.

## Implementation
We implemented everything from the original proposal, as well as some new features. Below they are briefly described.

### Viewing Journeys
As scoped in the proposal, the home page displays all the journeys submitted by commuters. Each journey contains the commuter's name, the date of the journey, the start and end station, the subway line, and the rating.

![homepage](../static/home_page.png)

### Posting Journeys
As scoped in the proposal, we created a page where commuters can submit data about their journey, which can then be viewed on the home page upon submission. The page is accessible from the home page "Add Your Journey!" button.

The user first inputs information about the journey itself. This includes the subway line, the start station, the end station, and the train ID. Next, they input information about themself, which includes their rating, ssn, date of trip, name, age, and whether they are a CS student.

After all inputs are filled in, they can then post the journey.

![postjourney](../static/post_journey.png)

### (New Feature) Filtering Journeys
To demonstrate the fun queries that can be performed in our system, we implemented two filtering buttons on the home screen.

The first is to sort the journeys by date. This allows users to then see how journeys may have changed over time, especially as stations are renovated or added.

The second is to filter journeys by rating. This way, users can find out which trips to avoid, or maybe even discover a very fun trip!

![filterjourney](../static/filter_journey.png)

### (New Feature) Rat Mode
Our most exciting feature is an Easter Egg created with our non-human commuters in mind. In the top right corner of the home page, the user may click the rat to enter "Rat Mode."

The page instantly changes to "rat colors," and it displays information that is more relevant to our rat users. The journeys now show a rat that lives at the start station (along with their favorite food), and a rat that lives at the end station (with their favorite food). Now, even our rat customers can be well equipped for their journeys. 

![ratmode](../static/rat_mode.png)

## Two Web Pages
### Index.html
Viewing journeys required a query

### Journey.html

input validation
