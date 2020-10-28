from setuptools import setup, find_packages
setup(
    name='sro_db',  # Required
    version="10.0.3",  # Required
    author="Paulo Sergio dos Santo Junior",
    author_email="paulossjuniort@gmail.com",
    description="A lib to access SRO DB",
 
    packages=find_packages(),
    
    install_requires=[
        'SQLAlchemy', 'SQLAlchemy-Utils', 'factory-boy', 'SQLAlchemy-serializer'
    ],

    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
    setup_requires=['wheel'],
    
)
