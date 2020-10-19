## Set Up
To set up the project, follow the steps;
```
sudo brew install postgresql postgresql-contrib \ postgis

download WBD shapefiles and add it to the ./alva_geodjango directory
link [ https://tufts.box.com/s/31sr5my3k21xhfkxm6d7jj5li0fa3ai2 ]
```
## On a Virtual Environment
```
Sudo apt-get install python-virtualenv
virtualenv venv
cd venv && . bin/activate
```
## Clone the system
```
git clone https://github.com/maryal01/alva_geodjango.git
```
## Setting up DB
```
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
createuser postgres --createdb
createdb agricom -U postgres

#Enable PostGIS
psql agricom
agricom=# CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;
```
## Installing Requirements
```
pip3 install -r requirements.txt
```

## Sync and Running application
```
cd agricom
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py downloadHUC
python3 manage.py populateDB

python3 manage.py createsuperuser
python3 manage.py runserver
on browser: localhost:8000/admin
```
## JSON format for API framework
The format the server expects a list with points and polygons defined as decimal degrees, 
where point is defined as,
```
{
    longitude,
    latitude,
    type: "POINT"
}
```

and polygon is defined as,
```
{
    lower latitude,
    higher latitude,
    lower longitude,
    higher longitude,
    type: "BOX"
}
```

let $x,y,z \in (polygon, point)$ then the json object expected is

``` { resource_list: [ x, y, z ] } ```
