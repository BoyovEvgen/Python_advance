import catday
import utils
from flask import Flask, Response, abort, send_file, render_template, request, redirect, url_for
import PIL.Image
import os
import io
import logging
import random


from time import perf_counter

app = Flask(__name__)

@app.route('/')
def hello_world():
    # # TODO: use proper template instead of the following
    # ret = r'Try <a href="/cats/catoftheday.jpg">Cat of the Day</a>'
    # ret += r'<br><img src="/cats/catoftheday.jpg" alt="catoftheday"'
    # ret += r' style="max-height: 90vh; margin: auto; display: flex"></img>'
    return render_template('index.html')

# Note:
#   If a rule ends with a slash and is requested without a slash by the user,
#   the user is automatically redirected to the same page with a trailing 
#   slash attached.
#   If a rule does not end with a trailing slash and the user requests
#   the page with a trailing slash, a 404 not found is raised.
# So we try to always define rules with trailing slashes '/'

@app.route('/cats/')
def list_cats():
    msg = 'There are {num} cats in our collection'
    return msg.format(num=len(catday.CATS))


def get_cat(numext, try_random=False):
    try:
        ret = catday.find_cat_file(numext=numext,
                                   try_random=try_random)
    except ValueError:      # integer unconvertable or wrong range
        abort(404, 'Wrong image number')
    else:
        app.logger.debug('Retrieve image "%s" for '
                        'base %s with ext "%s"',
                        *ret)
        return ret


@app.route('/cats/cat<int:num>.<string:ext>')
def cat_original(num, ext):
    t_start = perf_counter()    # measure request time

    file, base, ext = get_cat(f'{num}.{ext}', try_random=False)

    name = f'cat{base}{ext}'   # the filename passed to browser
    
    app.logger.debug('Original extension is %s', file.suffix)
    
    # if the extension is different, perform conversion with PIL
    if ext.lower() != file.suffix.lower():
        
        try:
            img = PIL.Image.open(file)
            # Save to buffer in memory and serve with Flask
            buf = utils.ImageIO(img, ext=ext)
        except utils.ImageIOError as err:
            abort(400, str(err))
        else:
            # now our file gets mocked by conversion result
            file = buf
    
    # if the file has the same extension,
    # don't convert at all and return directly

    took = perf_counter() - t_start

    if app.logger.isEnabledFor(logging.DEBUG):
        msg = f'Request took {took * 1000:.2f} ms'
        app.logger.debug(msg)

    return send_file(file, as_attachment=False, download_name=name)


@app.route('/cats/catoftheday<name>')
def cat_modified(name, message=None, blank=False):
    file, base, ext = get_cat(name, try_random=True)

    date = utils.DateTriple()       # try UADateTriple() here
    date_suffix = date.tostr(fmt='{day}_{month:.3}').lower()
    text = message or date.tostr(fmt='{weekday:.3},\n{day}\n{month:.3}')


    try:
        img = PIL.Image.open(file)
        bgcolor = (255, 255, 255, int(255 * 0.4))
        cut = catday.cutter.text_cutout(img, text, bgcolor=bgcolor)
        if ext in ['.jpg', '.jpeg', '.jfif']:
            # eliminate alpha-channel as JPEG has no alpha
            cut = cut.convert('RGB')
        file = utils.ImageIO(cut, ext=ext)
    except utils.ImageIOError as err:
        abort(400, str(err))

    # passed to browser
    name = f'catoftheday{base}-{date_suffix}{ext}'

    return send_file(file, as_attachment=False, download_name=name)


@app.route('/constructor/')
def constructor():
    number_of_pictures = len(catday.CATS)
    return render_template('constructor.html', num=number_of_pictures)


@app.route('/get-image/<int:num>/')
def get_image(num):
    try:
        image = catday.find_cat_file(numext=str(num)+'.jpg')[0]
    except ValueError:      # integer unconvertable or wrong range
        abort(404, 'Wrong image number')
    else:
        app.logger.debug('Retrieve image "%s" for '
                        'base %s with ext "%s"')
        return send_file(image)


@app.route('/image-maker/', methods=['POST'])
def image_maker():

    message = request.form.get('message').replace('\r', '')
    number_img = request.form.get('number_img')
    ext = request.form.get('ext') or '.jpg'
    print(ext)
    num_ext = number_img + ext
    app.logger.debug(number_img)
    app.logger.debug(message)
    return cat_modified(name=str(num_ext), message=message)


@app.route('/image-upload/',  methods=['GET', 'POST'])
def image_upload():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        file = request.files['file']
        ext = os.path.splitext(file.filename)[1]
        if ext in ('.jpg', '.jpeg', '.jfif', '.png'):
            filename = utils.get_hash(file) + ext
            if not catday.check_file_exists(filename):
                path_file = os.path.join(catday.FULL_PATH_CATDIR, filename)
                file.save(path_file)
                catday.update_cats()
                return 'Successful'
            else:
                return 'Such file already exists'
        else:
            return 'Invalid file format. Use: .jpg, .jpeg, .jfif, .png'


if __name__ == '__main__':
    import logging
    app.logger.setLevel(logging.DEBUG)
    app.run(host='127.0.0.1', port=5000, debug=True)