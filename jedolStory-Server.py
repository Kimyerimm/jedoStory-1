# app.py
# from flask import Flask, render_template, request, jsonify
from flask import Flask,request,abort, render_template, send_from_directory,jsonify,redirect, url_for, session, redirect, app
import os
import jedolAi as jedolAi
from datetime import datetime, timedelta
import lib.jshsFunctionLib as jshs


app = Flask(__name__)

app.secret_key = 'sntq0586'

@app.errorhandler(404)
def not_found(e):
    return render_template('/html/404.html'), 404

@app.route("/")
def index():
   if not 'usertokenId' in session:
        session['usertokenId'] = jshs.rnd_str(n=10, type="s")
        print("new-token",session['usertokenId'])    
   else:
        print("old-token",session['usertokenId'])         
   
   return render_template("/html/index.html",token=session['usertokenId'])

@app.route('/<path:page>')

def page(page):
   print(page)
   try:
        if ".html" in page:
            return render_template(page )
        else:
            return send_from_directory("templates", page)
   except Exception as e:
        abort(404)

@app.route("/query", methods=["POST"])
def query():
    
    query  = request.json.get("query")
    today = str( datetime.now().date().today())
    vectorDB_folder=f"vectorDB-faiss-jshs-{today}"
    
    if os.path.exists(vectorDB_folder) and os.path.isdir(vectorDB_folder):
         
         query  = request.json.get("query")
         print( "기존데이터 사용",query )
         answer = jedolAi.ai_reponse(vectorDB_folder, query  )
    else:
        print( "백터db만들기=", vectorDB_folder )
        
        vectorDB_folder=jedolAi.vectorDB_create(vectorDB_folder)
        answer = jedolAi.ai_reponse( vectorDB_folder, query  )

    return jsonify({"answer": answer })

if __name__ == "__main__":
       app.run(debug=True,host="0.0.0.0",port=5001)

