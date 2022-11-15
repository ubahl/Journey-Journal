# Journey Journal
> "Its about journaling the journey; not destining your destination"

**A COMS W4111 Project by Uma Bahl & Abram Kremer**

When Uma and Abram first arrived in New York City, they were astounded by the complicated, yet beautiful, subway system. So when the opportunity arose to model such a system to track their fun subway adventures, they jumped to the task. We present *Journey Journal,* a web application where commuters can add and view subway journeys.

## PostgreSQL Account
The database resides on `ank2177`.

## URL of Web Application
The web application is hosted on http://34.133.87.133:8111/.

## Implementation
We implemented everything from the original proposal, as well as some new features. Below they are briefly described.

### Viewing Journeys
As scoped in the proposal, the home page displays all the journeys submitted by commuters. Each journey contains the commuter's name, the date of the journey, the start and end station, the subway line, and the rating.

![homepage](../static/home_page.png)

### Posting Journeys
As scoped in the proposal, we created a page where commuters can submit data about their journey, which can then be viewed on the home page upon submission. The page is accessible from the home page "Add Your Journey!" button.

The user first inputs information about the journey itself. This includes the subway line, the start station, the end station, and the train ID. Next, they input information about themself, which includes their rating, ssn, date of trip, name, age, and whether they are a CS student.

After all inputs are filled in, the user can post the journey.

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
The main functionality of the database operations on this page is to display information about the journeys. The following queries are used.
* The default state of the home page is to show all the journeys. This is achieved by querying both the Journey and Commuter tables, and matching the Journey to the Commuter using ssn. Only the name, start station, end station, identifier, rating, and date are needed.
* In the case the commuter would like to see how journeys have changed over time, they may choose to sort the journeys by date. The query is then augmented with an ORDER BY statement.
* In the case the commuter would like to see journeys above a certain rating, they can filter by rating. This is especially helpful if you would like to find the best way to get somewhere, or just need some inspiration! The query adds an additional filter for rating.

The webpage also includes a “Rat Mode” Easter Egg to cater to **all** passengers of the subway. Rat mode involves the following additional query.
* The Lives_at relation is queried to find all the rats living at a given station. The rat name, station name, and favorite food are returned. The station names and ratings on the page are then converted to display the rats living at the stations and their favorite food, information that is more relevant to our rat users.


### Journey.html

When the user selects a value for a given input, the application then queries the database to return a new set of selections for the user to choose from. Our application guarantees that these selections are always compatible with all previous inputs. For example, after a user selects a line and start station, the application will return all the possible end stations compatible with that specific line and start station. Here is how such a query looks,

```
SELECT DISTINCT SA.train_id 
FROM Services S, Stops_At SA, Stops_At SA2 
WHERE 
  S.train_id = SA.train_id AND 
  S.train_id = SA2.train_id AND 
  S.identifier = identifier AND 
  SA.name != start_station AND 
  SA2.name != end_station
```

This is important since we have check constraints within the Journey schema and we want the user to be able to easily make selections that will not violate any of these constraints.

To further prevent any violations and/or SQL injections, we added input validation for all inputs in `server.py` before executing the query.
