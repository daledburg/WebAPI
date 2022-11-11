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

### R8 - Describe your projects models in terms of the relationships they have with each other

In this project there are five different models that are implemented. They include, a User model, a Category model, a Cashflow Item model, a Debt model and a Saving account model. The User model has a one to many relationship with the Cashflow Item model and also a one to many relationship with the Saving account model. For both of these a foreign key user_id is placed into the cash_flow_items table and the savings_account table to provide reference to the users table id for the particular user that has created each entry. Each user that is registered will be able to have multiple Cashflow items and Savings accounts linked to them. 

The Category model also has a one to many relationship with the Cashflow Item model as each Cashflow item row will contain a foreign key category_id. This refers to either the income or expense catrgeories and each of these descriptors will be linked with many Cashflow Items. 

The Cashflow Item model also has a one to one relationship with the Debt model as each Cashflow item can have an outstanding amount or not. The debt table contains a cash_flow_items_id foregin key that will identify which Cashflow item it is in reference too.

### R9 - Discuss the database relations to be implemented in your application

### R10 - Describe the way tasks are allocated and tracked in your project
