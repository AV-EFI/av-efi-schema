# House keeping utilities

The tools in this directory are supposed to help update the repository
with relevant changes in the Data Type Registry.

Here is the general procedure:

```console
## Change to the directory containing this file first.
## Create and activate virtual environment
utils$ python3 -m venv .venv
utils$ . .venv/bin/activate
## Pull in dependencies
(.venv) utils$ pip install doit
## Delete json schema files in order to trigger download in next step
(.venv) utils$ doit clean
## Generate reStructuredText from json schema files
(.venv) utils$ doit
```

Review and commit changes as appropriate.
