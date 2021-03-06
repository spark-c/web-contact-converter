# web-contact-converter
Written using Python/Flask with a html/css/js frontend.
created Feb 2021

This project is live [here](web-contact-converter.herokuapp.com)! (It is on a free Heroku dyno, so it may take a few seconds to load if the app was sleeping.)

See the project's [wiki](https://github.com/spark-c/web-contact-converter/wiki) for a more detailed look at the app's data pipeline.

A local company had a frequent task of manually transferring sales leads/contact information from a text document into a spreadsheet -- which took hours at a time. This app automates the process.

It requires the data input to be formatted as follows:

- Each company's information is separated by an empty line

- Each line contains one piece of the company's information

- The first line of the block must be the company's name.

- An email address is *required* somewhere in the block, or the information will be automatically discarded.

Example:
```
High Street Cleaners
(123) 555-1234
info@highstreetcleaners.com
9000 Laundry Ln
Earlington, WI 70264

Another Corp.
987-555-3214
help@anothercorp.net

...
```



