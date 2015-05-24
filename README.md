===============
Flask-Material
===============
[![Join the chat at https://gitter.im/HellerCommaA/flask-material](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/HellerCommaA/flask-material?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/HellerCommaA/flask-material/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/HellerCommaA/flask-material/?branch=master)

[![Build Status](https://scrutinizer-ci.com/g/HellerCommaA/flask-material/badges/build.png?b=master)](https://scrutinizer-ci.com/g/HellerCommaA/flask-material/build-status/master)

Flask-Material packages `MaterializeCSS` <https://github.com/Dogfalo/materialize> into an extension that mostly consists
of a blueprint named 'material'. It can also create links to serve Materialize
from a CDN and works with no boilerplate code in your application.

Usage
-----

Here is an example::

  from flask_material import Material

  [...]

  Material(app)

This makes some new templates available, containing blank pages that include all
bootstrap resources, and have predefined blocks where you can put your content.


Notes
-----
This is largely a fork from the excellent work at <https://github.com/mbr/flask-bootstrap>

Contributing
----
PRs are welcome. Esspicially for documentation and implementation of the base components.
