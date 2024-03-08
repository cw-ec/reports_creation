from setuptools import setup
from components import ReportFactory

"""
Access point for report creation tool. 

Click setup doc: https://ericmjl.github.io/blog/2016/12/24/how-to-make-your-python-scripts-callable-from-the-command-line/

"""


ReportFactory(workflow='.\\workflows\\example.json')
