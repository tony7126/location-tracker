# Sherpany Location Tracker

Stores locations that have been clicked on using Google Maps.  Also stores the locations in Fusion Tables.

### Version
0.0.1
### Installation

Note: This has only been tested on Ubuntu 14.04

```sh
$ git clone git@github.com:tony7126/location-tracker.git
$ cd location-tracker
$ virtualenv ~/.virtualenvs/sher #uses python3.4
$ source ~/.virtualenvs/sher/bin/activate
$ pip install -r requirements
$ python manage.py migrate
$ python manage.py runserver
$ Go to http://localhost:8000
```

### Caveats

* Realistically each user would have their own map/Fusion Table, but for the sake of simplicity I made the Fusion Table project wide
* I left the bower components in the repository.  Normally they would be gitignored to avoid bloat in the repo
* Using a fusion table layer was attempted but the map on the page wasn't getting updated quickly enough in many cases (even when forcing a refresh)
* There is a JSON file storing sensitive information in the repository for Google's API.  I acknowledge this is bad practice but convenient for the sake of running the project! 
* I use pre_save and post_delete signals to update Fusion Tables.  This means that when the map is cleared, individual delete queries are sent to Fusion Tables which is far less efficient than just sending one big "delete all" query.  This can be changed if need be.

