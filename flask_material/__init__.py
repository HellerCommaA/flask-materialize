#!/usr/bin/env python
# coding=utf8

__app_version__ = '0.1.1'
__material_version__ = '0.96.1'

import re

from flask import Blueprint, current_app, url_for

try:
    from wtforms.fields import HiddenField
except ImportError:
    def is_hidden_field_filter(field):
        raise RuntimeError('WTForms is not installed.')
else:
    def is_hidden_field_filter(field):
        return isinstance(field, HiddenField)


class CDN(object):
    """Base class for CDN objects."""
    def get_resource_url(self, filename):
        """Return resource url for filename."""
        raise NotImplementedError


class StaticCDN(object):
    """A CDN that serves content from the local application.

    :param static_endpoint: Endpoint to use.
    :param rev: If ``True``, honor ``MATERIAL_QUERYSTRING_REVVING``.
    """
    def __init__(self, static_endpoint='static', rev=False):
        self.static_endpoint = static_endpoint
        self.rev = rev

    def get_resource_url(self, filename):
        extra_args = {}

        if self.rev and current_app.config['MATERIAL_QUERYSTRING_REVVING']:
            extra_args['material'] = __version__

        return url_for(self.static_endpoint, filename=filename, **extra_args)


class WebCDN(object):
    """Serves files from the Web.

    :param baseurl: The baseurl. Filenames are simply appended to this URL.
    """
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get_resource_url(self, filename):
        return self.baseurl + filename


class ConditionalCDN(object):
    """Serves files from one CDN or another, depending on whether a
    configuration value is set.

    :param confvar: Configuration variable to use.
    :param primary: CDN to use if the configuration variable is ``True``.
    :param fallback: CDN to use otherwise.
    """
    def __init__(self, confvar, primary, fallback):
        self.confvar = confvar
        self.primary = primary
        self.fallback = fallback

    def get_resource_url(self, filename):
        if current_app.config[self.confvar]:
            return self.primary.get_resource_url(filename)
        return self.fallback.get_resource_url(filename)


def material_find_resource(filename, cdn, use_minified=None, local=True):
    """Resource finding function, also available in templates.

    Tries to find a resource, will force SSL depending on
    ``MATERIAL_CDN_FORCE_SSL`` settings.

    :param filename: File to find a URL for.
    :param cdn: Name of the CDN to use.
    :param use_minified': If set to ``True``/``False``, use/don't use
                          minified. If ``None``, honors
                          ``MATERIAL_USE_MINIFIED``.
    :param local: If ``True``, uses the ``local``-CDN when
                  ``MATERIAL_SERVE_LOCAL`` is enabled. If ``False``, uses
                  the ``static``-CDN instead.
    :return: A URL.
    """
    config = current_app.config

    if config['MATERIAL_SERVE_LOCAL']:
        if 'css/' not in filename and 'js/' not in filename:
            filename = 'js/' + filename

    if None == use_minified:
        use_minified = config['MATERIAL_USE_MINIFIED']

    if use_minified:
        filename = '%s.min.%s' % tuple(filename.rsplit('.', 1))

    cdns = current_app.extensions['material']['cdns']
    resource_url = cdns[cdn].get_resource_url(filename)

    if resource_url.startswith('//') and config['MATERIAL_CDN_FORCE_SSL']:
        resource_url = 'https:%s' % resource_url

    return resource_url


class Material(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        MATERIAL_VERSION = '0.96.1'
        JQUERY_VERSION = '1.11.3'
        HTML5SHIV_VERSION = '3.7.2'
        RESPONDJS_VERSION = '1.4.2'

        app.config.setdefault('MATERIAL_USE_MINIFIED', True)
        app.config.setdefault('MATERIAL_CDN_FORCE_SSL', False)

        app.config.setdefault('MATERIAL_QUERYSTRING_REVVING', True)
        app.config.setdefault('MATERIAL_SERVE_LOCAL', False)

        app.config.setdefault('MATERIAL_LOCAL_SUBDOMAIN', None)

        blueprint = Blueprint(
            'material',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path=app.static_url_path + '/material',
            subdomain=app.config['MATERIAL_LOCAL_SUBDOMAIN'])

        app.register_blueprint(blueprint)

        app.jinja_env.globals['material_is_hidden_field'] =\
            is_hidden_field_filter
        app.jinja_env.globals['material_find_resource'] =\
            material_find_resource

        if not hasattr(app, 'extensions'):
            app.extensions = {}

        local = StaticCDN('material.static', rev=True)
        static = StaticCDN()

        def lwrap(cdn, primary=static):
            return ConditionalCDN('MATERIAL_SERVE_LOCAL', primary, cdn)

        material = lwrap(
            WebCDN('//cdnjs.cloudflare.com/ajax/libs/materialize/%s/'
                   % MATERIAL_VERSION),
            local)

        jquery = lwrap(
            WebCDN('//cdnjs.cloudflare.com/ajax/libs/jquery/%s/'
                   % JQUERY_VERSION),
            local)

        html5shiv = lwrap(
            WebCDN('//cdnjs.cloudflare.com/ajax/libs/html5shiv/%s/'
                   % HTML5SHIV_VERSION))

        respondjs = lwrap(
            WebCDN('//cdnjs.cloudflare.com/ajax/libs/respond.js/%s/'
                   % RESPONDJS_VERSION))

        app.extensions['material'] = {
            'cdns': {
                'local': local,
                'static': static,
                'material': material,
                'jquery': jquery,
                'html5shiv': html5shiv,
                'respond.js': respondjs,
            },
        }
