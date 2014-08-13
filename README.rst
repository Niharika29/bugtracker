This is a Bug Tracking/Reporting/administering app developed as part of Google Summer of Code for TimVideos organization. 

The demo of which can be accessed at http://bugtracker.codersquid.com/bugform
And the backend can be accessed at http://bugtracker.codersquid.com/bugform/admin

Information collected includes user's location, IP, detected bandwidth, page loading-time etc.

The backend displays a table (contructed with django-tables2) showing all filed bugs, sortable by the headers. A basic Search feature is in place for searching bugs containing given string in their description. 

Authentication is done using Django's inbuilt Authorization system. 
