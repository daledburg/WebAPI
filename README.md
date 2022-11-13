# T2A2 - API Webserver project

## Dale Dahlenburg

### R1 - Identification of the problem you are trying to solve by building this particular app

The problem that has been identified through user stories that have been shared has been the issue with knowing what is happening with ones money. Today there is such a big range of ways to spend moeny, most of the time we don't actually have a solid idea about how we are travelling financially and in what ways we could identify to improve our situations ourselves. This application is designed to help those who struggle keeping their finances in order. By developing this API Webserver it provides a solid database to be able to interact with the client side of the project. It will be able to create a user and login system that will not only be secure but also store all of the user information that is entered regarding income, expenses, savings accounts and debts and track these over time through updates. By tracking all of this information, the application can then provide a cleaner, simpler look at their own unique situation and develop their own goals for the future.

### R2 - Why is it a problem that needs solving

Its incredibly easy to let spending get out of hand in this day and age. With so many different streams of income and expenses that are coming out of our bank accounts, the opportunity to introduce an application that will store all of this information and not only provide the opportunity to view it in a simple manner but also update and change that information as our lives change. Helping people, especially those who may be financially struggling to keep on top of their situation is important as there isnt any way to do this simply. The main goal is to bring simplicity to peoples lives so that they can make informed decisions.

### R3 - Why have you chosen this database system. What are the drawbacks compared to others

For this project, PostgreSQL was chosen to be the database system. This was done because of a range of benefits that come from utlising this database system. One of the main benefits of this database system is that it has a robust and mature authentication, access control and privilege management systems that are extremely scalable. While it also has support for a huge amount of data types it also has the ability to define your own complex types to better represent the data in the application. It also has the ability to define inheritance relationships between tables that helps define the relational nature of the application database. 

One of the drawbacks of using PostgreSQL compared to other database management systems is that as it is open source it is not compatible with as wide a range of application as other systems. The biggest drawback of PostgreSQL is that it is also slower in its execution and read speed when compared to other competitors which can be important for certain tasks. Installation and configuration can also be difficult for beginners and can result in a steep learning curve.

### R4 - Identify and discuss the key functionalities and benefits of an ORM

An Object-Relational-Mapper(ORM) is software that essentially serves as an abstraction level between the application and the database. The ORM allows you to query and manipulate data from a database using an object-oriented paradigm in your preferred programming language. By doing this it reduces the amount of boilerplate code and awkward techniques that have to be implemented in order to interact with the database as needed. 

An ORM has many benefits for developers, one being that it allows the code to be kept much dryer and as such it is much easier to maintain, update and reuse the code. Queries through an ORM are also prepared and sanitised which greatly reduces the risk of SQL injection. Another benefit is that it allows you to write code in the language that your are using without having to worry about learning SQL statements. An ORM also comes with many advanced features that allow your code to perform better than if you had written the SQL queries yourself and allowsd development time to be much quicker. It also allows the use of different databases as the ORM can deal with specific database SQL and if the database of choice is chosen, the code can still be used.

### R5 - Document all endpoints for API

[Documentation of all API endpoints](/api_endpoint.md)

### R6 - An ERD

![ERD Image](/img/API-ERD.png)

### R7 - Details any third party services that your app will use

Flask - This application utilises flask as the web framework. It is a microframework that does not include an ORM but has a small and easily extensible core. As it is a microframework it allows the design to be kept simple and therefore more scalable. Flask itself also utilises Werkzeg WSGI toolkit and the Jinja2 template engine.

SQLAlchemy - Is the Python ORM that allows communication between python modules and the databse that it is run in conjunction with. In this Application it is used to translate python classes into tables created in the PostgreSQL database and allow SQL statements to be executed.

Marshmallow - It is an object serialization/deserialization library which is used to convert objects to and from python data types. It is closely integrated with SQLAlchemy and adds addititional functionality. It also allows for data validation to be performed on the database to ensure data integrity.

Bcrypt - An extension of flask that allows the application to handle hashing. This particular extension is designed to be slow and as such is much harder to crack, providing a more secure implementation. It is particularly useful for passwords storing and decrypting.

Psycopg2 - Is a PostgreSQL database adapter specifically for the Python programming language. It implements Python DB API 2.0 specification and thread safety allowing heavily multi-threaded applications to function.

Flask JWT Extended - Allows the application to store and retrieve JWT tokens created by the users logging in. It integrates well with API's and has important functionality such as creating a JWT token, requiring a valid JWT token for a route and even getting the current JWT token of the user.

Datetime - Python built in package that allows the application to handle dates and time more effectively. Allows the current time to be accurately represented and create JWT tokens for the correct amount of time.

### R8 - Describe your projects models in terms of the relationships they have with each other

This project utilises the ORM SQLAlchemy to facilitate the communication between the python programs and the PostgreSQL database. Through SQLAlchemy there were a number of classes created, including classes for users, cashflow items, categories, debts and savings accounts. These classes were set up to define the columns of data to be provided to the database aswell as define relationships between the classes. The users class defines a parent-child relationship between itself and both the cashflow items class and the savings account class. This parent-child relationship is also defined in the classes as being one to many as each user instance can be related to multiple instances of both cashflow items and savings accounts. The User class also specifies that if the user instance is deleted, so to are all the children instances that are related to it. In this way if a user is deleted out of the database, all of the corresponding information pertaining to the user instance is also deleted.

The cashflow items model is also a child of the category model in another example of the parent(Category model) having a one to many relationship with the child(cashflow item). In this model instance, a user_id foregin key and category_id foregin key are designated to relate it to the id of particular users and categories. The cashflow item model has one other relationship which is that of a parent(cashflow item) child(debt) relationship with the debt class. This relationship is one to zero or one as the parent can be related to zero or one debt instance. The debt instance will be deleted as well if the cashflow item model is removed.

As well as these classes, SQLAlchemy also allows the definition of Schemas for each of the models to be implemented. These schemas take on a few differnt roles, one of them being specifying the fields that the data will be returned to the api as. An example of this is returning user data but not allowing any password information to be sent. Another use of the schema is allowing the json data to be returned by the api to nest information regarding related tables in the returned data. An example of this is the user schema which has a cash flow item and savings field that will be populated with relevant fields information specified by the developer.

### R9 - Discuss the database relations to be implemented in your application

The database that is set up for this application will consist of several tables that all have differnet relations with eachother. The user table will contain information regarding personal information. This table has a one to many relationship with the Cashflow item table and the savings account table. Both of these tables contain a users_id foreign key that links to the users table so as to provide reference to which user they both belong. They are both one to many relationships as each user can have multiple cash flow items and savings accounts tied to them.

The Cashflow item table also contains another foregin key, category_id. This foreign key links to the Category's table and has a many to one relationship. As there are only currently two different types of category's, income and expense, each cashflow item will be related to one or the other. This means that when querying the incomes of a user, all of the cashflow items that have the foregin key related to income will be returned. 

As well as these two relations, the cashflow table also has a one to one or zero relationship with the debts table. The debts table contains a cashflow item foreign key that will provide extra information if any of the cashflow items have outstanding debts remaining on them, but if they dont it is null.

### R10 - Describe the way tasks are allocated and tracked in your project

[Trello board link](https://trello.com/invite/b/ypnsXjnh/ATTI94c8c0039b0506b43f30dad318c020d247FCB7A3/api-webserver)

During the undertaking of this project, an agile management method was implemented. It began with receiving user stories from people questioned around me to find out what sort of features would be appropriate for this idea and also if this idea was something that people would be interested in using. From this information, it was discovered that there was a need for this application and the main focus was an application that would be able to simplify ones finances and allow users to have information at their fingertips and be able to make their own informed decisions.

From this a trello board was created to be able to understand all of the tasks that would be associated with creating such an application and as a way to track the progress and also increase efficiency. The Trello board contained a list of features that needed to be implemented as well as a list of the tasks required to be displayed in the documentation of the project. From here, the tasks were ordered by their priority to the success of the project but also in the priority of being able to move on to the next task so as to increase efficiency.

Once a task was started it would be moved into pending and them from there into done once it was finished. However, while completing tasks, testing was constantly being done on the code to ensure it was still suitable, and therefore if it was determined that a previously completed task was not working it would be moved back into the pending section of the board. This happened multiple times as I was learning more about the implementation of an API webserver and provided great learning opportunities.

### Setting up the database

This API runs on the database of PostgreSQL, therfore first of all the budget database needs to be set up. This is done through psql and once logged in:
```sql
create budget database;
```

Once this is complete it is time to seed the database with some data. To do this in the termianl run:
```bash
flask db drop && flask db create && flask db seed
```

If that was successful it will have printed Tables dropped, Tables created successfully and Tables seeded. The database is now ready to be used.
