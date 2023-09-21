import os
from sqlalchemy import create_engine, text

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})



def load_jobs_from_db():
  with engine.connect() as conn:

    result = conn.execute(text("SELECT * FROM jobhunt_jobs"))

    jobs = []
    for row in result.all():
      jobs.append(row._mapping)
    return jobs


def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(
      text(f"SELECT * FROM jobhunt_jobs WHERE id = {id}"), )
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._mapping


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text(
      """INSERT INTO jobhunt_applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url)
                        VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)"""
    )
    params = {
      'job_id': job_id,
      'full_name': data['full_name'],
      'email': data['email'],
      'linkedin_url': data['linkedin_url'],
      'education': data['education'],
      'work_experience': data['work_experience'],
      'resume_url': data['resume_url']
    }
    conn.execute(query, params)


def add_job_to_db(data):
  with engine.connect() as conn:
    query = text("""INSERT INTO jobhunt_jobs ( title, location, salary, 
      currrency, responsibilities, requirements) 
      VALUES(:title, :location, :salary, :currrency, :responsibilities, 
      :requirements)""")
    params = {
      'title': data['title'],
      'location': data['location'],
      'salary': data['salary'],
      'currrency': data['currrency'],
      'responsibilities': data['responsibilities'],
      'requirements': data['requirements']
    }
    conn.execute(query, params)
