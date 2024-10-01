# fms
COMP636 Assignment - Javier Ng Kok How (Student ID: 1161775)

## Project Report Part 1: Design Decisions
This web app has four pages: home page, mobs, paddocks and stock. The homepage contained an image with a blurb on the functionalities of the web app. 

### Mobs

The mobs' webpage lists all the details of the mob and the paddock it is assigned to and gives the user the ability to move mobs between available paddocks. 

#### Move Mobs

Instead of showing all paddocks in the dropdown, it is a better user experience only to show the available paddocks that the mob can be shifted to. This is achieved by using the ‘NOT IN’ SQL statement. When the user executes the ‘move mob’ function, it uses the POST method that retrieves the *mob_id* from the submitted form data by the user and retrieves the *paddock_id* of the new paddock that the mob is intending to be moved into. This then triggers an UPDATE query that updates the mobs' table and assigns the *paddock_id* to a new mob. Once the change has been implemented, it will redirect the user back to the mobs' webpage. 

### Stock 

The stock webpage displays the stocks grouped by mobs and assigned to their respective paddocks. It also shows the stock age and its associated birthdate in the table. There are no user actions on the webpage. 

### Paddocks

The paddocks webpage shows a table with paddock details, the mob that’s assigned to it and the stock numbers in the paddock. This webpage has three input functions. It allows the user to ‘add new paddocks’, ‘edit existing paddocks’ and ‘advance date by one day.’

#### Add Paddock

A user can add new paddocks by inputting the *name*, *area* and *dm_per_ha* into a form when they click on the ‘add paddock’ button. This POST method inserts new values into the database and calculates the *total_dm*. If the user inputs string values into the *area* and *dm_per_ha*, an error will be displayed and the user will have to correct it. The *add_paddock* functionality comes with error handling as it considers scenariors such as SQL errors in the event the new paddock name is not unique or connection issues or database capacity (unlikely). 

#### Edit Existing Paddocks

To edit details in the paddock’s table, the user can click on the paddock’s name and they will be directed to the paddock_details page for that specific paddock. A user template form will be displayed where the user can make changes to the *name*, *area*, and *dm_per_ha*. Three app routes have been created to achieve this. 
 
The paddocks_details is the route that leads to a landing page when user made changes to the paddock's details. It displays the *paddock_id*, *name*, *area*, *dm per ha* and *total_dm*.

The paddock_details/edit is the route that leads to a page where user can make changes to the paddock's details. Editable fields are the name, area dm per ha and total_dm. Even though the paddock_id is displayed, it cannot be edited. Essentially, this page displays a form that can return data. 

The paddock_details/edit/update is the route that updates the database with the new paddock fields. It utilises the POST method as it modifies existing values in the database and recalculates the *total_dm*. Once the change has been implemented, user will be redirected to a unique URL that included the *paddock_id*. 

#### Advance Date by One Day

A user can advance the current date by one day when this button is selected. The new date appears as a flash message and the *current date*, *total_dm* and *dm_per_ha* are recalculated and updated in the table.

To recalculate the new *total_dm* and *dm_per_ha* based on the stock numbers, the code considers the *pasture_growth_rate*, and *stock_consumption_rate* and updates the table in the paddocks table in the database. For a seamless user experience, the function redirects the user back to the paddock webpage after selecting the button.


## Project Report Part 2: 
1. What SQL statement creates the mobs table and defines its fields/columns? (Copy and paste the relevant lines of SQL.) 

```
CREATE TABLE mobs (
	id int NOT NULL AUTO_INCREMENT,
	name varchar(50) DEFAULT NULL,
	paddock_id int not null,
	PRIMARY KEY (id),
    	UNIQUE INDEX paddock_idx (paddock_id);
```
   
3. Which lines of SQL script sets up the relationship between the mobs and paddocks tables?
   
```
CONSTRAINT fk_paddock
	FOREIGN KEY (paddock_id)
	REFERENCES paddocks(id)
	ON DELETE NO ACTION
	ON UPDATE NO ACTION
```

5. The current FMS only works for one farm. Write SQL script to create a new table called farms, which includes a unique farm ID, the farm name, an optional short description and the owner’s name. The ID can be added automatically by the database. (Relationships to other tables not required.)
```   
CREATE TABLE farms (
    farm_id INT NOT NULL AUTO_INCREMENT,
    farm_name VARCHAR(100) NOT NULL,
    short_description TEXT DEFAULT NULL,
    owner_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (farm_id)
);
```

4. Write an SQL statement to add details for an example farm to your new farms table, which would be suitable to include in your web application for the users to add farms in a future version. (Type in actual values, don’t use %s markers.) 
```
INSERT INTO farms (farm_name, short_description, owner_name)
VALUES ('Happy Valley, 'A lovely small town farm', 'Javier Ng);
```
5. What changes would you need to make to other tables to incorporate the new farms table? (Describe the changes. SQL script not required.) 

To incorporate the new farms' table into the other existing tables, a relationship needs to be established between these tables. For instance, a farm can contain multiple paddocks, mobs and stock. To effectively link the tables together, a farm_id needs to be set up as a foreign key to the tables: paddocks, mobs and stock. It may not be necessary to link a stock directly to a farm as it is covered by the paddocks and mobs tables.


## References: 

Image Source: Image by <a href="https://pixabay.com/users/thedigitalartist-202249/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=2641195">Pete Linforth</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=2641195">Pixabay</a>
