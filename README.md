# Evaluating Which Python library is Best suitable for Bulk insert into Aurora Postgres SQL Performance Comparison

#### Authors 

###### Soumil Nitin Shah 
###### Hari Om Dubey(Consultant Software Engineer, Python developer)

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

## psycopg2 executemany
![image](https://user-images.githubusercontent.com/39345855/200120223-ff0a9f1f-41fe-4123-936b-53af1ce03a0b.png)


## psycopg2 execute batch
![image](https://user-images.githubusercontent.com/39345855/200120313-2375c168-657e-458a-bfd6-1a7d3e89e579.png)
* It won't matter too much if you are working with tiny amounts of data. But as the size of the data grows, it will definitely get more interesting to explore and use these alternative methods to speed up the process up to 13 times!

# SQL alchemy Insert Many 
![image](https://user-images.githubusercontent.com/39345855/200120362-2d18ae5f-ac8c-468a-97c4-261a4fd35628.png)

# Comparison 
![image](https://user-images.githubusercontent.com/39345855/200120373-1d9e84bc-5699-411c-83c7-520a22f1b8c5.png)

# Conclusion

* SqlAlchemy should always be the primary option when working with and entering bulk items into AWS Aurora because it is obvious from testing that it is a faster approach to insert data into Aurora PostgreSQL. When compared to psycopg2(executemany), VS SqlAlchemy is almost 60 to 70% faster. Comparing batch Size 30,000 Bulk Insert using psycopg2(executemany) we found it took around 1248 seconds vs when using psycopg2(execute_batch_method ) took 19.4 seconds VS SQLAlchemy took only 1.5 seconds.

# Future Work :
* I will do further tests to make sure the results are accurate. I would want to assess the Read Speed later. For bulk reads, which library would be better?

# Do not hesitate to fork the repository, contribute your discoveries, and submit a merge request.




References
* Aurora PostgreSQL Insert Many Performances Test Using Various Python Library. Accessed 27 Oct. 2022.

* “SQLAlchemy.” Pypi, pypi.org/project/SQLAlchemy. Accessed 27 Oct. 2022.

* “Psycopg2.” Psycopg2, pypi.org/project/psycopg2. Accessed 27 Oct. 2022.

* “Pandas to PostgreSQL Using Psycopg2: Bulk Insert Performance Benchmark.” Naysan, naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark. Accessed 27 Oct. 2022.

* “Improve Your Psycopg2 Executions for PostgreSQL in Python.” Datacareer, www.datacareer.de/blog/improve-your-psycopg2-executions-for-postgresql-in-python. Accessed 27 Oct. 2022.


