# ehrql-tutorial

ehrQL (rhymes with circle), the Electronic Health Records Query Language, is a query language and software tool designed for working with health data. [Learn more about ehrQL here.](https://docs.opensafely.org/ehrql/)

## About the workshop

This was a workshop designed by the NHS England Data Science team to teach colleagues how to use ehrQL, in addition to the [tutorial](https://docs.opensafely.org/ehrql/tutorial/) provided by Open Safely.

## Set up and use

To complete the workshop you will need access to GitHub codespaces.

- Fork the repository
- Set up a codespace (this will be easier than cloning to your local machine as it will install all necessary packages)
- Read through:
    - analysis/dataset_definition.py
    - analysis/create_graph.py
    - project.yaml

- Complete the task outlined in your_task.md, which will give you a chance to play around with the kind of data you can pull out of OS.

## About the OpenSAFELY platform

The OpenSAFELY platform is a secure analytics framework for electronic health records research in the NHS.

Instead of requesting access for slices of patient data and transporting them elsewhere for analysis,
the platform supports developing analytics against dummy data
and then running against the real data *within the same infrastructure that the real data is stored*.
Read more at [OpenSAFELY.org](https://opensafely.org).

[1]: https://docs.opensafely.org/ehrql/tutorial/
