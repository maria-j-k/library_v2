# library_v2
New version of library project (Django), written in Flask.

## General Info
The application intends to be used by a school library, still in creation phase. 
First part of the application is managing the catalogue - import data from csv file, rectify errors in existing records, creation of new records. In order to reduce the risk of typos and time needed to enter each record, I've implemented Elasticsearch (modyfing to my needs Miguel Grinberg's solution from [Microblog tutorial](https://github.com/miguelgrinberg/microblog)) search-as-you-type functionality, enabling user to pick existing entity. 

Second part (planned) consist of readers interface - searching the catalogue, managing loans etc.

## Functionalities in place:
* scripts importing data from csv file to postgresql database
* adding a new position

## Functionalities to implement:
* adding a new copy of a book which exists already in database
* rectifying records imported from csv file
* implement users and permissions 
* restrict all this part of application to users with write permission to catalogue

## In future:
* develop users authentication system to include (beside staff) school students and teachers 
* enable searching the catalogue by various criteria
* enable book reservations and loans

## Technologies:
* Python
* Flask
* Elasticsearch
* Postgresql

For details see requiremets.txt
