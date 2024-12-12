**How to run project**

step1: install python and pip

step2: install the require files in venv(recommended) or main environment
#For macOS -> python -m venv venv

step3: install all dependencies -> pip install -r requirements.txt

step4: set values of all variables in .env file and it will load them in OS env variables

#first create a database in localhost server having seperate passwords and database name and keep other variables same. In my case these are the variables

DATABASE_USERNAME=postgres
DATABASE_PASSWORD=password
DATABASE_NAME=hotwaxassessment
DATABASE_PORT=5432
DATABASE_HOST=localhost
ALGORITHM=HS256
SECRET_KEY=09d2b8y3r03o4yih2a4nfaarw6ca2t3h4isuo4t3e5th0i0s2a53p2pacf63b88e8d3e7
EXPIRY_TIME_TAKEN=90

step5: running command -> uvicorn app.main:app

Note: For calling apis use Bearer Token Authentication in postman. This token can be generated using GET generate token API ("/authentication/token")

link to check swagger documentation HTTP://localhost:8000/docs

Token API
<img width="959" alt="Screenshot 2024-12-12 at 17 36 23" src="https://github.com/user-attachments/assets/333260ed-c68d-4bed-bd47-4e7c440811b0" />

Create orders
<img width="1003" alt="Screenshot 2024-12-12 at 17 37 29" src="https://github.com/user-attachments/assets/6461e32a-7126-4b0a-822f-cc4db3454302" />

Get orders
<img width="994" alt="Screenshot 2024-12-12 at 17 40 09" src="https://github.com/user-attachments/assets/f872abbd-f94f-48fe-842f-f57213dd49c1" />

Delete order
<img width="1019" alt="Screenshot 2024-12-12 at 17 41 14" src="https://github.com/user-attachments/assets/ec64a852-9bd8-4ce4-b2d6-0fa0e0db3f86" />

Create order items (with wrong token)
<img width="997" alt="Screenshot 2024-12-12 at 17 41 58" src="https://github.com/user-attachments/assets/6cdc13c4-7cfe-4417-9cf3-bd0c5bf2bfba" />

Create order items (with correct token)
<img width="1002" alt="Screenshot 2024-12-12 at 17 42 09" src="https://github.com/user-attachments/assets/ac6c2780-ddf0-4c59-9ed7-2976a02eaa22" />

Update order items
<img width="991" alt="Screenshot 2024-12-12 at 17 43 18" src="https://github.com/user-attachments/assets/13cd9350-022e-406f-b3ca-142e50d1defe" />

Delete Order items
<img width="1004" alt="Screenshot 2024-12-12 at 17 43 43" src="https://github.com/user-attachments/assets/4319bc52-8c9d-4661-b94a-284727a29067" />
