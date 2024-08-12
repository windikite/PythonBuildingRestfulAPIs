My 22nd assignment! This is a basic restful API as a companion to an earlier project, the fitness center database. It has endpoints that allow for full CRUD and comes with a setup script to create the correct database to use with it.

All you need is:  
1. Flask  
2. Marshmallow  
3. A password.py with the database password

Endpoints for members:  
1. GET: localhost:5000/members  
2. GET: localhost:5000/members/id  
3. POST: localhost:5000/members  
4. PUT: localhost:5000/members/id  
5. DELETE: localhost:5000/members/id  

JSON structure:  
{
    "age": "43",
    "name": "Tommy"
}  

---------------------------------------------------------

Endpoints for members:  
1. GET: localhost:5000/sessions  
2. GET: localhost:5000/sessions/id 
3. GET: localhost:5000/sessions_by_member/id 
4. POST: localhost:5000/sessions  
5. PUT: localhost:5000/sessions/id  
6. DELETE: localhost:5000/sessions/id  

JSON structure:  
{
    "activity": "Weightlifting",
    "member_id": "1",
    "session_date": "2024-07-23",
    "session_time": 700
}  