# API endpoint documentation

## User Routes:

/user/register/
- Methods: POST
- Arguments: None
- Description: Creates new user account
- Authentication: None
- Authorization: None
- Request Body: 
```json
{
    "f_name": "Dale",
    "l_name": "Dahlenburg",
    "email": "13457@coderacademy.edu.au",
    "password": "Password1"
}
```
- Response Body:
```json
{
    "id": "1",
    "f_name": "Dale",
    "l_name": "Dahlenburg",
    "email": "13457@coderacademy.edu.au",
    "date_created": "2022-11-10"
}
```
- Response code: 409

/user/login/
- Methods: POST
- Arguments: None
- Description: Allow user to login and access their information
- Authentication: Check entered email and password against stored data
- Authorization: None
- Request Body:
```json
{
    "email": "13457@coderacademy.edu.au",
    "password": "Password1"
}
```
- Response Body:
```json
{
    "email": "13457@coderacademy.edu.au",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.         eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODA0MTgxNCwianRpIjoiZjJkNWU0MzQtZjgwNi00YjRiLWFkNDktYzg3ZTFiMDhlMjMzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE2NjgwNDE4MTQsImV4cCI6MTY2ODA4NTAxNH0.VkordzIRFT0-7oaQcfsQIfIWdRVKbXV1yLyy53YVEHc"
}
```
- Response code: 401

/user/<int:id>/
- Methods: PUT, PATCH
- Arguments: Id of user
- Description: Allows logged in users to update their user information
- Authentication: jwt_required() header
- Authorization: Bearer token of logged in user, user id from token must match id in url
- Request Body:
```json
{
    "f_name": "Barry",
    "l_name": "Burns"
}
```
- Response Body:

For PATCH and PUT response
```json
{
    "f_name": "Barry",
    "l_name": "Burns",
    "email": "13457@coderacademy.edu.au",
}
```

For Delete response
```json
{
    "message": "User deleted successfully"
}
```
- Response code: 404

/user/<int:id>/
- Methods: DELETE
- Arguments: Id of user
- Description: Allows logged in users to delete their user information
- Authentication: jwt_required() header
- Authorization: Bearer token of logged in user, user id from token must match id in url
- Request Body: None
- Response Body: 
```json
{
    "message": "User deleted successfully"
}
```
- Response code: 404

/user/details/
- Methods: GET
- Arguments: None
- Description: Retrive the logged in user's details
- Authentication: jwt_required() header
- Authorization: Bearer token, user id taken from get_jwt_identity and compared to the user's id
- Request Body: None
- Response Body:
```json
{
    "id": 1,
    "f_name": "Dale",
    "l_name": "Dahlenburg",
    "email": "dale.19@icloud.com",
    "date_created": "2022-11-10",
    "cash_flow_item": [
        {
            "description": "Wage",
            "amount": 1500.0
        },
        {
            "description": "Electricity",
            "amount": 200.0
        },
        {
            "description": "Home Loan",
            "amount": 1000.0
        }
    ],
    "saving": [
        {
            "bank_name": "ANZ",
            "current_amount": 5000.0,
            "date_updated": "2022-11-10"
        },
        {
            "bank_name": "Commbank",
            "current_amount": 30000.0,
            "date_updated": "2022-11-10"
        }
    ]
}
```
- Response code: Standard error responses

---

## Cashflow Items Routes:

/cashflow/
- Methods: GET
- Arguments: None
- Description: Get all items including incomes and expenses
- Authentication: jwt_required() header
- Authorization: bearer token user id taken from get_jwt_identity and compared to the user_id's on each item to determine if it belongs to logged in user
- Request Body: None
- Response Body:
```json
{
    "incomes": [
        {
            "id": 1,
            "description": "Wage",
            "amount": 1500.0,
            "date_created": "2022-11-10",
            "frequency": "Weekly",
            "user_id": 1,
            "category_id": 1
        }
    ]
},
{
    "expenses": [
        {
            "id": 4,
            "description": "Electricity",
            "amount": 200.0,
            "date_created": "2022-11-10",
            "frequency": "Monthly",
            "user_id": 1,
            "category_id": 2,
            "debt": []
        },
        {
            "id": 8,
            "description": "Home Loan",
            "amount": 1000.0,
            "date_created": "2022-11-10",
            "frequency": "Monthly",
            "user_id": 1,
            "category_id": 2,
            "debt": [
                {
                    "outstanding_amount": 300000.0
                }
            ]
        }
    ]
}
```
- Response code: Standard error responses

/cashflow/income/
- Methods: GET
- Arguments: None
- Description: Display all associated incomes for a logged in user
- Authentication: jwt_required() header
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on each item to determine if it belongs to logged in user
- Request Body: None
- Response Body:
```json
[
    {
        "id": 1,
        "description": "Wage",
        "amount": 1500.0,
        "date_created": "2022-11-10",
        "frequency": "Weekly",
        "user_id": 1,
        "category_id": 1
    }
]
```
- Response code: Standard error responses

/cashflow/expense/
- Methods: GET
- Arguments: None
- Description: Display all associated expenses with logged in user
- Authentication: jwt_required() header
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on each item to determine if it belongs to logged in user
- Request Body: None
- Response Body:
```json
[
    {
        "id": 4,
        "description": "Electricity",
        "amount": 200.0,
        "date_created": "2022-11-10",
        "frequency": "Monthly",
        "user_id": 1,
        "category_id": 2,
        "debt": []
    },
    {
        "id": 8,
        "description": "Home Loan",
        "amount": 1000.0,
        "date_created": "2022-11-10",
        "frequency": "Monthly",
        "user_id": 1,
        "category_id": 2,
        "debt": [
            {
                "outstanding_amount": 300000.0
            }
        ]
    }
]
```
- Response code: Standard error responses

/cashflow/<int:category_id>/
- Methods: POST
- Arguments: Id of category that it will be associated with, income = 1 or expense = 2
- Description: Create a new item either, income or expense
- Authentication: jwt_required() header
- Authorization: Bearer token user id taken and assigned to the new items user_id to identify it in the future
- Request Body:
```json
{
    "description": "car payments",
    "amount": 180.0,
    "frequency": "Fortnightly"
}
```
- Response Body:
```json
{
    "id": 13,
    "description": "car payments",
    "amount": 180.0,
    "date_created": "2022-11-10",
    "frequency": "Fortnightly",
    "user_id": 9,
    "category_id": 2,
    "debt": []
}
```
- Response code: Standard error responses

/cashflow/<int:id>/
- Methods: PUT, PATCH
- Arguments: Id of item to be affected
- Description: Update certain item created by logged in user
- Authentication: jwt_required() header
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on each item to determine if it belongs to logged in user
- Request Body:
```json
{
    "description": "Bee Keeping"
}
```
- Response Body:
```json
{
    "description": "Bee Keeping",
    "amount": 400.0,
    "frequency": "Fortnightly"
}
```
- Response code: Standard error responses

/cashflow/<int:id>/
- Methods: PUT, PATCH
- Arguments: Id of item to be affected
- Description: Update certain item created by logged in user
- Authentication: jwt_required() header
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on each item to determine if it belongs to logged in user
- Request Body: None
- Response Body:
```json
{
    "message": "Item deleted successfully"
}
```
- Response Code: 404

/cashflow/budget/
- Methods: GET
- Arguments: None
- Description: Finds remaing budget after total expenses have been taken from total income.
- Authentication: jwt_required() header
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on each item to determine if it belongs to logged in user
- Request Body: None
- Response Body:
```json
{
    "budget_remaining": "Your remaining budget is $1161.25"
}
```
- Response code: Standard error responses

---

## Debt Routes:

/debt/
- Methods: GET
- Arguments: None
- Description: Returns all expenses that are outstanding debts
- Authentication: jwt_required()
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on each item to determine if it belongs to logged in user
- Request Body: None
- Response Body:
```json
{
    "User Debts": [
        [
            {
                "id": 5,
                "description": "Car Loan",
                "amount": 155.0,
                "date_created": "2022-11-10",
                "frequency": "Monthly",
                "user_id": 1,
                "category_id": 2,
                "debt": [
                    {
                        "outstanding_amount": 25000.0
                    }
                ]
            }
        ],
        [
            {
                "id": 8,
                "description": "Home Loan",
                "amount": 1000.0,
                "date_created": "2022-11-10",
                "frequency": "Monthly",
                "user_id": 1,
                "category_id": 2,
                "debt": [
                    {
                        "outstanding_amount": 300000.0
                    }
                ]
            }
        ]
    ]
}
```
- Response code: Standard error responses

/debt/<int:id>/
- Methods: POST
- Arguments: Id of the cashflow items id that is going to be related to the debt
- Description: Create a debt description for an expense
- Authentication: jwt_required()
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on the cash flow item to determine if it belongs to logged in user
- Request Body:
```json
{
    "outstanding_amount": 15000
}
```
- Response Body:
```json
{
    "id": 5,
    "outstanding_amount": 15000.0,
    "cash_flow_item_id": 5
}
```
- Response Code: 404

/debt/<int:id>/
- Methods: PATCH PUT
- Arguments: Id of the cashflow items id that is going to be related to the debt
- Description: Update a debt description for an expense
- Authentication: jwt_required()
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on the cash flow item to determine if it belongs to logged in user
- Request Body:
```json
{
    "outstanding_amount": 15000
}
```
- Response Body:
```json
{
    "id": 5,
    "outstanding_amount": 15000.0,
    "cash_flow_item_id": 5
}
```
- Response Code:

/debt/<int:id>/
- Methods: DELETE
- Arguments: Id of the cashflow items id that is going to be related to the debt
- Description: Delete a debt description for an expense
- Authentication: jwt_required()
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on the cash flow item to determine if it belongs to logged in user
- Request Body: None
- Response Body:
```json
{
    "message": "Debt item deleted successfully"
}
```
- Response Code: 404

---

## Saving Routes:

/saving/
- Methods: GET
- Arguments: None
- Description: Display all savings accounts
- Authentication: jwt_required() header
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on the saving item to determine if it belongs to logged in user
- Request Body: None
- Response Body:
```json
[
    {
        "bank_name": "Commbank",
        "current_amount": 30000.0
    },
    {
        "bank_name": "ANZ",
        "current_amount": 40000.0
    }
]
```
- Response Code: 404

/saving/
- Methods: POST
- Arguments: None
- Description: Create new savings account associated with logged in user
- Authentication: jwt_required() header
- Authorization: Bearer token user id taken from get_jwt_identity and added to the new instance to link the account to the user logged in
- Request Body:
```json
{
    "bank_name": "ANZ",
    "current_amount": 150000.0
}
```
- Response Body:
```json
{
    "id": 6,
    "bank_name": "ANZ",
    "current_amount": 150000.0,
    "date_updated": "2022-11-10",
    "user_id": 1
}
```
- Response code: Standard error responses

/saving/<int:id>/
- Methods: PATCH PUT
- Arguments: Id of Savings account related to user
- Description: Update the details of existing savings account
- Authentication: jwt_required() header
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on the saving account
- Request Body:
```json
{
    "current_amount": 20000.0
}
```
- Response Body:
```json
{
    "bank_name": "ANZ",
    "current_amount": 20000.0,
    "date_updated": "2022-11-10"
}
```
- Response Code: 404

/saving/<int:id>/
- Methods: DELETE
- Arguments: Id of Savings account related to user
- Description: delet the existing savings account
- Authentication: jwt_required() header
- Authorization: Bearer token user id taken from get_jwt_identity and compared to the user_id's on the saving account
- Request Body: None
- Response Body:
```json
{
    "message": "Account successfully deleted"
}
```
- Response Code: 404
