from setuptools import setup

setup(
   name="idifyd",
   version="0.0.1",
   description="A fun lil side project",
   author="Wesley Yuan",
   author_email="wesley.yuan1746@gmail.com",
   packages=["backend"],  #same as name
   install_requires=["fastapi"], #external packages as dependencies
)