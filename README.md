===============
Flask-Materialize
===============

# **With the recent addition of Google's Material Design Lite, this project will soon be ported over to that framework and change names. <http://www.getmdl.io/> However, this project will be maintained in this repo and on PyPi. More updates will follow.**


[![Join the chat at https://gitter.im/HellerCommaA/flask-materialize](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/HellerCommaA/flask-materialize?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/HellerCommaA/flask-materialize/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/HellerCommaA/flask-materialize/?branch=master)

[![Build Status](https://scrutinizer-ci.com/g/HellerCommaA/flask-materialize/badges/build.png?b=master)](https://scrutinizer-ci.com/g/HellerCommaA/flask-materialize/build-status/master)

Flask-Material packages `MaterializeCSS` <https://github.com/Dogfalo/materialize> into an extension that mostly consists
of a blueprint named 'material'. It can also create links to serve Materialize
from a CDN and works with no boilerplate code in your application.


Demo
----
A quick demo applicdation can be seen at http://flask-template-materia.elasticbeanstalk.com/  
This demo is a clone of https://github.com/HellerCommaA/flask-template-materialize  

Usage
-----

First, easily install the package with `pip install flask-material`

A sample helloworld app:  
**hello_world.py**  
*Yes, I know this is a long helloworld, but, you'll have a great base to start with if you follow along!*  

```python
from flask import Flask, render_template  
from flask_material import Material  
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required

app = Flask(__name__)  
Material(app)  
app.config['SECRET_KEY'] = 'USE-YOUR-OWN-SECRET-KEY-DAMNIT'
app.config['RECAPTCHA_PUBLIC_KEY'] = 'TEST'

# straight from the wtforms docs:
class TelephoneForm(Form):
    country_code = IntegerField('Country Code', [validators.required()])
    area_code = IntegerField('Area Code/Exchange', [validators.required()])
    number = TextField('Number')

class ExampleForm(Form):
    field1 = TextField('First Field', description='This is field one.')
    field2 = TextField('Second Field', description='This is field two.',
                       validators=[Required()])
    hidden_field = HiddenField('You cannot see this', description='Nope')
    recaptcha = RecaptchaField('A sample recaptcha field')
    radio_field = RadioField('This is a radio field', choices=[
        ('head_radio', 'Head radio'),
        ('radio_76fm', "Radio '76 FM"),
        ('lips_106', 'Lips 106'),
        ('wctr', 'WCTR'),
    ])
    checkbox_field = BooleanField('This is a checkbox',
                                  description='Checkboxes can be tricky.')

    # subforms
    mobile_phone = FormField(TelephoneForm)

    # you can change the label as well
    office_phone = FormField(TelephoneForm, label='Your office phone')

    ff = FileField('Sample upload')

    submit_button = SubmitField('Submit Form')


    def validate_hidden_field(form, field):
        raise ValidationError('Always wrong')

@app.route('/')  
def hello_world():
      form = ExampleForm()   
      return render_template('test.html', form = form)  

if __name__ == '__main__':  
    app.run(debug = True)  
```

**templates/test.html with silly macros**

```python
{% extends "material/base.html" %}
{% import "material/utils.html" as util %}
{% import "material/wtf.html" as wtf %}

{% block title %}Hello, world!{% endblock %}

{% block content %}
{{ container() }}
        {{ row() }}
                {{ col(['s12', 'm6']) }}
                	{{ util.card('Hello world!', wtf.quick_form(form) )}}
                {{ enddiv() }}
                {{ col(['s12', 'm6'])}}
                	{{ util.card('Isn\'t Flask great?', '<p>I really do enjoy it!</p>', [['https://github.com/HellerCommaA', 'My Github']])}}
            	{{ enddiv() }}
        {{ enddiv() }}
{{ enddiv() }}
{% endblock %}
```

**OR templates/test.html without silly macros**

```python
{% extends "material/base.html" %}
{% import "material/utils.html" as util %}
{% import "material/wtf.html" as wtf %}

{% block title %}Hello, world!{% endblock %}

{% block content %}
<div class="container">
        <div class="row">
                <div class="col s12 m6">
                	{{ util.card('Hello world!', wtf.quick_form(form) )}}
                </div>
                <div class="col s12 m6">
                	{{ util.card('Isn\'t Flask great?', '<p>I really do enjoy it!</p>', [['https://github.com/HellerCommaA', 'My Github']])}}
            	</div>
        </div>
</div>
{% endblock %}
```

This makes some new templates available, containing blank pages that include all
Material resources, and have predefined blocks where you can put your content.

Available Blocks
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
Contains:	`{{block scripts}}`  **which includes materialize.js and jquery.js, *be sure to call super***  
Contains: 	`{{block footer}}`  
Ends: Just above `</body>`

Available Macros
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

----
**These may or may not be useful, feedback requested. **  

*Container*  
`{{ container() }}` Generates `<div class="container">`

*Row*  
`{{ row() }}` Generates `<div class="row">`  

*Col*  
`{{ col( ['s12', 'm6'] ) }}` Generates `<div class="col s12 m6">`

*Enddiv*  
`{{ enddiv() }}` Generates `</div>`

TODO
----
* Fix WTF forms integration (quick form)  
* Finish documentation

Notes
-----
This is largely a fork from the excellent work at <https://github.com/mbr/flask-bootstrap>
