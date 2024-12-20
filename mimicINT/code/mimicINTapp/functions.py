from django.core.files.storage import default_storage
import os
from django.conf import settings
from mimicINTapp.forms import *
from datetime import *
from mimicINTapp.models import *
from django.db.models import Sum

#permet de telecharger les fichiers fasta soumis par l'utilisateur
'''def handle_uploaded_file(file, directory_file):
    with open(directory_file, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
'''

def get_rule_index(run_id):
    job_dir = os.path.join(settings.JOBS_DIR, run_id)
    rule_index_file = os.path.join(job_dir, 'rule_index')
    with open (rule_index_file) as f:
        start_index = int(f.read().strip())
    return start_index

def sum_rule_duration(run_id):
    start_index = get_rule_index(run_id)

    total_duration = 0

    if start_index == 0:
        total_duration = pipeline_rule.objects.aggregate(sum_duration=Sum('rule_duration'))
        total_duration = int(list(total_duration.values())[0])

    else:
        rules = pipeline_rule.objects.all()[start_index:]
        for rule in rules:
            total_duration += rule.rule_duration

    return total_duration
def end_time_run(run_id):
    job = Job_infos.objects.get(job_id=run_id)
    sum_duration = sum_rule_duration(run_id)
    end_time = job.submission_date + timedelta(seconds=sum_duration)
    return end_time

def progress_time_run(run_id):
    Job_infos.objects.get(job_id=run_id)
    end_time = end_time_run(run_id)
    now = datetime.now()
    progress = min((now - Job_infos.objects.get(job_id=run_id).submission_date).total_seconds() / (
                end_time - Job_infos.objects.get(job_id=run_id).submission_date).total_seconds(), 1) \
               * 100  # Calculer la progression en pourcentage

    return progress
