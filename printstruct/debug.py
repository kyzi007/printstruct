from pydoc import getdoc
import inspect
import tempfile
import webbrowser
import sys

def _param_html(text):
    return '<span class="params"> ' + text + '</span>'


def _doc_html(text):
    return '<span class="doc">' + text + '</span>'


def _atr_html(text):
    return '<span class="light">var: </span> <strong>' + text + '</strong>'


def _fun_html(text):
    return '<span class="light">fun: </span> <strong>' + text + '</strong>'


def _structure_html(func, params):
    return '<div>' + func + '</div><div>' + params + '</div>'


_br = '</br>'


def print_struct(obj, name='temp'):
    """ print object structure """
    result_fun = ''
    result_var = ''
    for atrName in dir(obj):
        if not atrName.startswith('__') and not atrName.startswith('_'):
            atr = getattr(obj, atrName)
            if callable(atr) and (inspect.isfunction(atr) or inspect.ismethod(atr)):
                result_fun += _fun_html(atrName) + _br
                params = ''
                if len(inspect.getargspec(atr).args):
                    for paramName in inspect.getargspec(atr).args:
                        if not paramName.startswith('self'):
                            if params:
                                params += ', '
                            params += paramName
                    if params:
                        result_fun += _br + _param_html(params)
                result_fun += _br + _doc_html(getdoc(atr)) + _br
            else:
                result_var += _atr_html(atrName) + _br
    _open_in_browser(_structure_html(result_fun, result_var), name)


def _open_in_browser(html, name):
    for p in sys.path:
        try:
            template = file(p+ '/printdoc/template.html', 'r').read()
        except:
            pass

    template = template.replace('$TITLE$', 'Print ' + name)
    template = template.replace('$BODY$', html)
    path = tempfile.gettempdir() + '/doc_' + name + '.html'
    output = open(path, 'w')
    output.write(template)
    output.close()
    webbrowser.open('file:' + path)


def _get_path(): return str(inspect.getfile(inspect.currentframe())).replace('debug.py', '')
