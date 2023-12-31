from setuptools import setup

setup(
   name="imdownifyouredown",
   version="0.0.1",
   description="A fun lil side project",
   author="Wesley Yuan",
   author_email="wesley.yuan1746@gmail.com",
   packages=["imdownifyouredown"],  #same as name
   install_requires=[  #external packages as dependencies
      "fastapi",
      "pysqlite3",
      "pytest",
      "httpx",
      "uvicorn",
   ], 
)