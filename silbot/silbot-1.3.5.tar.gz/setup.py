from distutils.core import setup

setup(
  name = 'silbot',         # How you named your package folder (MyLib)
  packages = ['silbot'],   # Chose the same as "name"
  version = '1.3.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This is an object oriented Telegram bot framework',   # Give a short description about your library
  long_description= "See on GitHub: https://github.com/SilverOS/Silbot-Py",
  long_description_content_type='text/markdown',
  author = 'SilverOS',                   # Type in your name
  author_email = 'support@silveros.it',      # Type in your E-Mail
  url = 'https://github.com/SilverOS/Silbot-Py',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/SilverOS/Silbot-Py/archive/1.3.2.tar.gz',    # I explain this later on
  keywords = ['telegram', 'bot', 'api', 'oop','getupdates','all types'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',

  ],
)