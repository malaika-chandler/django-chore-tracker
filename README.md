# Chore Tracker

A simple tracker for recurrent chores using Django 3

## Getting Started

Download the repo and in the root directory add a file called `secret_key.txt` containing the Django secret key

### Prerequisites

[Install Django 3](https://docs.djangoproject.com/en/3.0/topics/install/#installing-official-release)  

Then install django-bootstrap3
```
pip install django-bootstrap3
```

If using the dummy data population script
```
pip install Faker
```

## Application Images

Lists instances of upcoming chores in order of scheduled due date. The instance can be marked complete by clicking the button at the top right corner. The overflow menu contains links to parent chore page and the option to delete or edit that instance.  
![Default Upcoming View](sample-images/upcoming.png?raw=true "View of upcoming chores")  

There's also a separate view for the chores themselves. Chores with overdue instances show in red. The dates in blue indicate upcoming events scheduled for that chore. The overflow menu contains links to the detailed view for and the option to delete a given chore.  
![All Chores View](sample-images/all.png?raw=true "All chores view with overdue indicators")  

## Built With

* [Django](https://docs.djangoproject.com/en/3.0/) - The web framework used
* [Bootstrap 3](https://getbootstrap.com/docs/3.4/) - Styling and components
* [django-bootstrap3](https://pypi.org/project/django-bootstrap3/) - Used to quickly style forms
* [Faker](https://faker.readthedocs.io/en/master/) - Used in the dummy data population script
* [Anaconda](https://www.anaconda.com/) - For maintaining distinct development environments

## Acknowledgements
The brand image used called ["housework"](https://svgsilh.com/4caf50/image/311681.html) found using [https://creativecommons.org](https://ccsearch.creativecommons.org) image search and
is licensed under CC0 1.0. To view a copy of this license, visit https://creativecommons.org/licenses/cc0/1.0/
