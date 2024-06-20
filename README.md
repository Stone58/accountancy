## CONTEXT
To provide some background on this project, I was given a 5-day challenge. While I am proficient in Python and have experience with libraries like Pandas, Numpy, Matplotlib, Scikit-learn, etc., and have developed Python applications using Flask, the challenge was to complete the app within the given timeframe using Django framework. Despite not having prior knowledge of how the Django framework works, considering my workload and responsibilities, I successfully learned, comprehended, and built the Django app in just 2 days. The application encompasses various modules, including the database, models, tests, API endpoints, and documentation.

## TECHNOLOGIES USED: Python, Django Framework, JWT for security, and REST-API-Test for unit testing and API test, Swagger for documentation

## TASK:
For the task related to this project, please check the "Python_challenge_1_django.pdf" file.

## Regarding Coding
- I used English for coding; therefore, I translated the tables as follows: Firms -> company; Operations -> operation.
- Besides those tables, there are other tables: Operation Type -> operationType; User -> user.

## How to Test the Project:
- Firstly, since JWT authentication is in place, obtaining a token is necessary. The endpoint for that is:
```bash
  http://127.0.0.1:8000/api/token/
```
- There is an existing admin superuser with the default username='admin' and password='1234.'
- Roles (IDs and their descriptions): 1 -> Admin; 2 -> Accountant; 3 -> Worker
- Using it to get a token is required.
- To create operations, users, operation types, and firms need to be created first.

## For Automated Testing:
```bash
python manage.py test
```

## Project Setup:
- I developed the project in a Windows environment and prepared a batch file for it. It can be adjusted and executed based on the environment and 'python' path variable (or individually).

## Project Improvements and Questions

### Remaining Questions:
- Can accountants or managers create operations currently?
- Is it possible to edit operations, or is deletion and recreation the only option?
- Can the date be entered manually, or is it solely based on the system time?

### Enhancing Authorization Management:
- According to the current task specifications and time constraints, authorization was implemented using group features. Could a more optimized approach be to create specific permissions for each method and associate them with groups? This might provide a more flexible structure.

### Detailed Testing:
- While CRUD operations seem to work correctly using the administrator role, more detailed test cases covering different user roles could be developed.

### Regarding Changes in Tables:
- Consider adding an additional field to track who last modified a piece of data. This could be beneficial for auditing and accountability purposes.

