import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdr_python_sdk",                                    
    version="1.0.1",                                       
    author="pandora",                                    
    author_email="pandora@qiniu.com",               
    description="pandora python sdk",                    
    long_description=long_description,               
    long_description_content_type="text/markdown",     
    url="https://github.com/",                          
    packages=setuptools.find_packages(),                 
    classifiers=[                                          
        "Programming Language :: Python :: 3",         
        "License :: OSI Approved :: MIT License",    
        "Operating System :: OS Independent",         
    ],
)
