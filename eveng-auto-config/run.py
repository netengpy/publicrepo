#!/usr/bin/env python3.8

from flask import Flask, render_template, Response, request, abort, send_file
import os
import sys
import subprocess
from time import sleep
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
import logging


app = Flask(__name__)

@app.route('/config', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = '/home/omz/workspace/eveng-config-deploy/atc-iol-initialcfgs'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)
    print('PATH - ', abs_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    return render_template('files.html', files=sorted(files))


@app.route('/deploy',methods = ['POST', 'GET'])
def execute():
    foldername = request.form['foldername'] 
    print(foldername)
    def inner():
      sys.stdout.flush()
      print("<<DEBUG_INFO>>",foldername)
      cmd = "./deploy-config.py {}".format(foldername)
      print("<<DEBUG_INFO>>",cmd)
      #sleep(1)
      proc = subprocess.Popen(cmd, shell=True, bufsize=1, stdout=subprocess.PIPE, universal_newlines=True)

      for line in iter(proc.stdout.readline,''):
          yield line
  
    env = Environment(loader=FileSystemLoader('templates'))
    tmpl = env.get_template('deploy.html')
    return Response(tmpl.generate(response=inner()))

if __name__ == '__main__':
    print(" * Running on http://127.0.0.1:5000/config (Press CTRL+C to quit)")
    print(" * Logging enabled to debug.log")
    logging.basicConfig(filename='debug.log',level=logging.DEBUG)
    app.run(debug = True)

#
#    FOR DEBUGGING and LOGGING
#
#    import logging
#    logFormatStr = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d}\n[%(levelname)s]: %(message)s'
#    logging.basicConfig(format = logFormatStr, filename = "debug.log", level=logging.DEBUG)
#    formatter = logging.Formatter(logFormatStr,'%d-%m %H:%M:%S')
#    fileHandler = logging.FileHandler("summary.log")
#    fileHandler.setLevel(logging.DEBUG)
#    fileHandler.setFormatter(formatter)
#    streamHandler = logging.StreamHandler()
#    streamHandler.setLevel(logging.DEBUG)
#    streamHandler.setFormatter(formatter)
#    app.logger.addHandler(fileHandler)
#    app.logger.addHandler(streamHandler)
#    app.logger.info("* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)")
#    app.logger.info("* Logging enabled to debug.log & summary.log")
   
#    # set debug = False to stop console debug and auto-reload after detecting change
#    app.run(debug = True, threaded=True)