from flask import Flask, abort, request, Response
from statapi.methods import methods, get_doc, formatters
from utils.util import convert_str_to_bool

app = Flask(__name__)


@app.route('/stats/')
# @lru_cache(maxsize=1)  # can use cuz no flask proxies refered
def stats_root():
    """List all methods."""
    res = {'methods': list(methods)}
    format = request.args.get('format')
    if format:
        func_format = formatters[format][1]
        return func_format(res)
    format_str = "<h1>{}. {}</h1> <p>{}</p>"
    res['methods'] = [format_str.format(i, name, get_doc(name)) for i, name in enumerate(res['methods'], start=1)]
    return Response(res['methods'])


@app.route('/stats/<string:method>')
def stats(method):
    kwargs = request.args.to_dict()
    kwargs = convert_str_to_bool(**kwargs)
    print(kwargs)
    try:
        func = methods[method]
    except KeyError:
        abort(404, f'Method {method} not found')

    try:
        # format is set on a statapi module level defaults
        res, mime = func(**kwargs)
    except ValueError as exc:
        abort(404, exc)

    # TODO: add error reporting verbosity
    #       e.g. when format is not supported

    return Response(res, mimetype=mime)


if __name__ == '__main__':
    # We need to set logging to be able to see everything
    import logging
    app.logger.setLevel(logging.DEBUG)

    # (!) Never run your app on '0.0.0.0 unless you're deploying
    #     to production, in which case a proper WSGI application
    #     server and a reverse-proxy is needed
    #     0.0.0.0 means "run on all interfaces" -- insecure
    app.run(host='127.0.0.1', port=5000, debug=True)
