from gt_app import app


if __name__ == '__main__':
    #if not app.debug: # if app is in production
    import logging
    from logging import FileHandler
    fhandler = FileHandler(filename='gtserver.log', encoding='utf-8')
    fhandler.setLevel(logging.INFO)
    app.debug = True
    if not app.debug:
        fhandler.setLevel(logging.ERROR)
    app.logger.addHandler(fhandler)
    # set processes param for mulpiple concurrent users.
    #app.run(host='0.0.0.0', port=5000, processes=4)
    app.run(port=5005)


