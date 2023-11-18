from setuptools import setup

setup(
   name="imdownifyouredown",
   version="0.0.1",
   description="A fun lil side project",
   author="Wesley Yuan",
   author_email="wesley.yuan1746@gmail.com",
   packages=["imdownifyouredown"],  #same as name
   install_requires=["fastapi", "pysqlite3"], #external packages as dependencies
)