from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, add_job_to_db

app = Flask(__name__)


@app.route("/")
def main():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs)


@app.route("/not_ready")
def not_ready_page():
  return render_template('not_ready.html')


@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)

  if not job:
    return "Not Found", 404

  return render_template('jobpage.html', job=job)


@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id, data)
  return render_template('application_submitted.html',
                         application=data,
                         job=job)


@app.route("/post-a-job")
def post_job():
  return render_template("job_posting.html")


@app.route("/job-posted", methods=['post'])
def job_posted():
  data = request.form
  add_job_to_db(data)
  return render_template("job_posting.html")


@app.route("/api/job", methods=['post'])
def show_job_json():
  job = request.form
  return jsonify(job)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
