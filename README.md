=====
Workspaces
=====

Workspaces is a Django app.


Quick start
-----------

1. Add "workspaces" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'workspaces',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('workspaces/', include('workspaces.urls')),

3. Run ``python manage.py migrate`` to create the workspaces models.

4. Start the development server and visit http://127.0.0.1:8000/workspaces/
