===============
Flask-Material
===============

[![Join the chat at https://gitter.im/HellerCommaA/flask-materialize](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/HellerCommaA/flask-materialize?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/HellerCommaA/flask-materialize/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/HellerCommaA/flask-materialize/?branch=master)

[![Build Status](https://scrutinizer-ci.com/g/HellerCommaA/flask-materialize/badges/build.png?b=master)](https://scrutinizer-ci.com/g/HellerCommaA/flask-materialize/build-status/master)

Flask-Material packages `MaterializeCSS` <https://github.com/Dogfalo/materialize> into an extension that mostly consists
of a blueprint named 'material'. It can also create links to serve Materialize
from a CDN and works with no boilerplate code in your application.

Usage
-----

A sample helloworld app:  
**hello world.py**  
```
from flask import Flask, render_template  
from flask_material import Material  
app = Flask(__name__)  
Material(app)  
@app.route('/')  
def hello_world():  
      return render_template('test.html')  

if __name__ == '__main__':  
	app.run()  
```

**templates/test.html**
```
{% extends "material/base.html" %}
{% import "material/wtf.html" as wtf %}
{% import "material/fixes.html" as fixes %}
{% import "material/utils.html" as util %}

{% block title %}Hello, world!{% endblock %}

{% block content %}
<div class="container">
        <div class="row">
                <div class="col s12">
                        {{ util.form_button('Hello world!', ['waves-effect', 'waves-light']) }}
                </div>
        </div>
</div>
{% endblock %}
```

This makes some new templates available, containing blank pages that include all
Material resources, and have predefined blocks where you can put your content.

Availible Blocks
----------------
	{{block doc}}
Starts: Above `<!DOCTYPE html>`  
Ends: Below `</html>`

	{{block html_attribs}}  
Starts: Inside the `<html>` tag  
Ends: Inside the `<html>` tag

	{{block head}}
Starts: Just after the `<head>` tag  
Ends: Just before the `</head>` tag

	{{block title}}
Starts: Just inside the `<title>` tag  
Ends: Before `</title>` tag

	{{block metas}}
Starts: Inside the `<head>` block, after `</title>`. Automatically includes  
`<meta name="viewport" content="width=device-width, initial-scale=1.0">` Be sure to call super() if you want this meta tag  
Ends: Within `<head>` block, just before `{{block styles}}`

	{{block styles}}
Starts: Inside the head block, after the `metas` block closes. Includes a link to material.css be sure to call super()  
Ends: Just before `</head>`

	{{block body_attribs}}
Starts: Just after `<body`  
Ends: Just before `>` in the top `<body>` tag.  
	`<body{% block body_attribs %}{% endblock body_attribs %}>`
	
	{{block body}}
Starts: Immediately after `<body>`  
Contains: 	`{{block navbar}}`  
Contains: 	`{{block content}}`  
Contains:	`{{block scripts`  **which includes materialize.js and jquery.js, *be sure to call super***  
Ends: Just above `</body>`


Availible Macros
----------------
Be sure you are using `{% import "material/utils.html" as util %}` in your HTML document.

*Icon*  
Simply do: `{{ util.icon('ICON-NAME-WITHOUT-MDI', ['SIZE', 'OPTIONAL-CSS-CLASSES']) }}`

*Button*  
Macro prototype: `{{ util.form_button(content, class = [], type='submit', name='action', icon = False, iconclass=[] }}`

	**Note**  
	Class already includes btn. Everything else must be added.  
	<button class="btn {{ class|join(' ') }}" type="{{type}}" name="{{name}}">{{content}}
	{% if icon %}<i class="{{ iconclass|join(' ') }} right"></i>{% endif %}</button>

*Card*  
Card prototype: `{{ util.card('CARD-TITLE', 'CARD-CONTENT-CAN-USE-HTML-HERE', [['http://google.com/LINK.html', 'Link Title'], ['http://www.google.co.uk/link2.html', 'Link Title2']]) }}`  
Card does not include any row, or column sizes. You must wrap the card in your desired size.

Notes
-----
This is largely a fork from the excellent work at <https://github.com/mbr/flask-bootstrap>