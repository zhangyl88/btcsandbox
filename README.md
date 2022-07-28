# btc-sandbox
This is an open-source backend module for trading investment platform. Project was built with [django-rest-framework](https://www.django-rest-framework.org/) and [python](https://www.python.org/downloads/) and &#8211;&#8211;&#8211;


Distributed under the MIT License. See
[LICENSE](https://en.wikipedia.org/wiki/MIT_License) for more information.

## Installation

<b>Note: </b>To setup this project on your machine, you must get [python](https://www.python.org/downloads/) and [pip3](https://pip.pypa.io/en/stable/installation/) globally installed in your machine


CLone repoistory and navigate to cloned folder

    $ git clone  https://github.com/dycode999/btcsandbox.git
    $ cd btcsandbox

Create and activate a virtual environment

    $ python -m pip3 install virtualenv
    $ virtualenv env
    $ source env/Scripts/activate

Install requiements and run migrations

    $ pip install -r requirements.txt
    $ python manage.py migrate

Launch server

    $ python manage.py runserver


### Contributors
<a href="https://github.com/dycode999/btcsandbox/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=dycode999/btcsandbox" height="40"/>
</a>
<br>

## Licence & Author
MIT License

Copyright (c) 2022 dycode&#8482;

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.