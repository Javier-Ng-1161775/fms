# fms
 COMP636 Assignment - Javier Ng Kok How

## Project Report Part 1: 
1. Discuss design decisions (min 1 per task) and detailed assumptions


## Project Report Part 2: 
1. What SQL statement creates the mobs table and defines its fields/columns? (Copy and paste the relevant lines of SQL.) 

> CREATE TABLE mobs (
	id int NOT NULL AUTO_INCREMENT,
	name varchar(50) DEFAULT NULL,
	paddock_id int not null,
	PRIMARY KEY (id),
    UNIQUE INDEX paddock_idx (paddock_id);
   
3. Which lines of SQL script sets up the relationship between the mobs and paddocks tables?
   
	> CONSTRAINT fk_paddock
		FOREIGN KEY (paddock_id)
		REFERENCES paddocks(id)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION

5. The current FMS only works for one farm. Write SQL script to create a new table called farms, which includes a unique farm ID, the farm name, an optional short description and the owner’s name. The ID can be added automatically by the database. (Relationships to other tables not required.)
   
> CREATE TABLE farms (
    farm_id INT NOT NULL AUTO_INCREMENT,
    farm_name VARCHAR(100) NOT NULL,
    short_description TEXT DEFAULT NULL,
    owner_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (farm_id)
);

4. Write an SQL statement to add details for an example farm to your new farms table, which would be suitable to include in your web application for the users to add farms in a future version. (Type in actual values, don’t use %s markers.) 

> INSERT INTO farms (farm_name, short_description, owner_name)
VALUES ('Happy Valley, 'A lovely small town farm', 'Javier Ng);

5. What changes would you need to make to other tables to incorporate the new farms table? (Describe the changes. SQL script not required.) 

To incorporate the new farms' table into the other existing tables, a relationship needs to be established between these tables. For instance, a farm can contain multiple paddocks, mobs and stock. To effectively link the tables together, a farm_id needs to be set up as a foreign key to the tables: paddocks, mobs and stock. It may not be necessary to link a stock directly to a farm as it is covered by the paddocks and mobs tables.


## References: 

Image Source: Image by <a href="https://pixabay.com/users/thedigitalartist-202249/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=2641195">Pete Linforth</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=2641195">Pixabay</a>
