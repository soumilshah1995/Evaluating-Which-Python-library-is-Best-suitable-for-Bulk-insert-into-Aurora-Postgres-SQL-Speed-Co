# Evaluating Which Python library is Best suitable for Bulk insert into Aurora Postgres SQL Performance Comparison

#### Authors 

###### Soumil Nitin Shah 
* I earned a Bachelor of Science in Electronic Engineering and a double master’s in electrical and Computer Engineering. I have extensive expertise in developing scalable and high-performance software applications in Python. I have a YouTube channel where I teach people about Data Science, Machine learning, Elastic search, and AWS. I work as a data collection and processing specialist at Jobtarget where I spent most of my time developing Ingestion Framework and creating microservices and scalable architecture on AWS 

###### Hari Om Dubey(Consultant Software Engineer, Python developer)
* I have completed a Master’s in Computer Application, and I have 5 years of experience in developing software applications using Python and Django frameworks. I love to code in Python and creating a solution for a problem by coding excites me. I have been working at Jobtarget for like past 2 months as a Software Engineer in a Data Team.

###### Overview:
* Amazon Aurora PostgreSQL is a fully managed, PostgreSQL–compatible, and ACID–compliant relational database engine that combines the speed, reliability, and manageability of Amazon Aurora with the simplicity and cost-effectiveness of open-source databases. Aurora PostgreSQL is a drop-in replacement for PostgreSQL and makes it simple and cost-effective to set up, operate, and scale your new and existing PostgreSQL deployments, thus freeing you to focus on your business and applications. In this I wanted to test various python libraries for speed and performance and present the findings with community 

----------------------------------------------------------------------
#  Introduction 

* The most well-known PostgreSQL database adapter for Python is called Pycopg. The full implementation of the Python DB API 2.0 specification and thread safety are its key features (several threads can share the same connection). It was created for heavily multi-threaded programs that make a lot of concurrent "INSERT" or "UPDATE" requests and generate a lot of cursor creation and destruction.
* The most well-known PostgreSQL database adapter for Python is called Pycopg. The full implementation of the Python DB API 2.0 specification and thread safety are its key features (several threads can share the same connection). It was created for heavily multi-threaded programs that make a lot of concurrent "INSERT" or "UPDATE" requests and generate a lot of cursor creation and destruction.
* Under the terms of the MIT License, SQLAlchemy is an open-source SQL toolkit and object-relational mapper for Python. The Python SQL toolkit and Object Relational Mapper, SQLAlchemy, provides application developers with all of SQL's functionality and versatility. It offers a complete set of well-known enterprise-level persistence patterns created for fast, effective database access and translated into a straightforward, Pythonic domain language.
* The ease of implementation, speedy code development, and lack of need for prior SQL knowledge are all reasons why SQLAlchemy is so well-liked. The high-level approach is emphasized in practically all online programming tutorials and courses for this reason. The majority of working software engineers also appear to choose SQLAlchemy.


# Aurora PostgreSQL SQL Configuration  

![image](https://user-images.githubusercontent.com/39345855/200120146-eb752476-8217-4f00-a91a-475d00cd79d4.png)

# Create a Table
```
CREATE TABLE IF NOT EXISTS public.user
                (
                    first_name character varying(256) COLLATE pg_catalog."default",
                    last_name character varying(256) COLLATE pg_catalog."default",
                    address character varying(256) COLLATE pg_catalog."default",
                    text character varying(256) COLLATE pg_catalog."default",
                    id character varying(256) COLLATE pg_catalog."default",
                    city character varying(256) COLLATE pg_catalog."default",
                    state character varying(256) COLLATE pg_catalog."default"
                )s
```
###### Figure 1: Shows Creating SQL table

* After creating the Table, we shall be inserting data into this tables in batches with some common libraries used for Aurora and shall measure the time it takes to insert batches of data and dervive insights which is faster in terms of speed.

# II Results

![image](https://user-images.githubusercontent.com/39345855/200120223-ff0a9f1f-41fe-4123-936b-53af1ce03a0b.png)
* Figure 1: Shows Creating SQL table

* After creating the Table, we shall be inserting data into this tables in batches with some common libraries used for Aurora and shall measure the time it takes to insert batches of data and derive insights which is faster in terms of speed.

#### Results
![image](https://user-images.githubusercontent.com/39345855/200120248-f69bce1a-b58c-4cfe-aaf4-c379af263a81.png)





References
* Aurora PostgreSQL Insert Many Performances Test Using Various Python Library. Accessed 27 Oct. 2022.

* “SQLAlchemy.” Pypi, pypi.org/project/SQLAlchemy. Accessed 27 Oct. 2022.

* “Psycopg2.” Psycopg2, pypi.org/project/psycopg2. Accessed 27 Oct. 2022.

* “Pandas to PostgreSQL Using Psycopg2: Bulk Insert Performance Benchmark.” Naysan, naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark. Accessed 27 Oct. 2022.

* “Improve Your Psycopg2 Executions for PostgreSQL in Python.” Datacareer, www.datacareer.de/blog/improve-your-psycopg2-executions-for-postgresql-in-python. Accessed 27 Oct. 2022.


