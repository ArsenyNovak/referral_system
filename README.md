Referral System
===
site: http://arseniprojects.store:4000

Example referral System  



## Technologies
Python, Django, DjangoRestFramework  
Docker, PostgreSQL

## API  
[readme document API](project_rs/readmeAPI.md)  

[file check API Postman](referral system.postman_collection.json)

## Local setup

---
1. Run command: git clone https://github.com/ArsenyNovak/referral_system.git
2. Work directory create file ".env":
````
  SECRET_KEY=your_secret_key  
  DEBUG=True
  DB_NAME=db  
  DB_USER=your_name  
  DB_PASSWORD=your_password  
  DB_HOST=dbps  
  DB_PORT=5432
````  

3. Run command: docker compose up --build
4. Run command: docker compose exec Django python manage.py migrate

