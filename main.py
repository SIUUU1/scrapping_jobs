from flask import Flask, render_template, url_for, request, redirect, send_file
from extractors.wwr import get_jobs
from models.job import Job
from file import save_to_file

app = Flask("JobScrapper",  static_folder='static')

# @app.route('/<pdb_id>')
# def viewer1(pdb_id):
#     pdb_filename = f'{pdb_id.upper()}.pdb'
#     pdb_url = url_for('static', filename='pdbs/' + pdb_filename)
#     return render_template('browse_complex.html', data_href=pdb_url)

@app.route("/")
def home():
  return render_template("home.html", name="siu")

db = {}

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None or keyword == "":
    return redirect("/")
  if keyword in db:
    jobs = db[keyword]
  else:
    jobs = get_jobs(keyword)
    db[keyword] = jobs
  return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route('/export')
def export():
    keyword = request.args.get("keyword")
    if keyword == None or keyword == "":
      return redirect("/")
    if keyword not in db:
      return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0", debug=True, port=8080)