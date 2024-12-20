from django.db import models
from django.contrib import admin


# The following code defines the models 

# ======================================
# Tables related to dynamic page content
# ======================================

## home_text
#  ---------
#
# This table registers the following attributes:
# - text_ID: Integer - An unique ID.
# - text_title: Text - The title of the paragraph.
# - text_content: Text - The content of the paragraph.
#
class home_text(models.Model):
    text_ID = models.IntegerField(primary_key=True, default=0, editable=False)
    text_title = models.TextField(max_length = 50, default="", blank=True, null = True)
    text_content = models.TextField(max_length = 500, default="", blank=True, null = True)

## news_part
#  ---------
#
# This tables contains news to be displayed on the home page.
#
# This table registers the following attributes:
# - news_ID: Integer - An unique ID.
# - news_title: Text - The title of the news.
# - new_content: Text - The content of the news
#
class news_part(models.Model):
    news_ID = models.IntegerField(primary_key=True, default=0, editable=False)
    news_title = models.TextField(max_length = 100, default="", blank=True, null = True)
    news_content = models.TextField(max_length = 500, default="", blank=True, null = True)



# ======================================
# Tables related to workflow itself
# ======================================

## setting_prediction
#  ------------------
#
# This table contains the documentation of the parameters
# that can be set by the user or automatically set during the run.
#
# This table registers the following attributes:
# - setting_ID: Integer - An unique ID.
# - setting_name: Text - The name of the setting.
# - tooltip: Text - The documentation of the setting.
# 
class setting_prediction(models.Model):
    setting_ID = models.IntegerField(primary_key=True, default=0, editable=False)
    setting_name = models.TextField(max_length = 50, default="", blank=True, null = True)
    tooltip = models.TextField(max_length = 500, default="", blank=True, null = True)


## pipeline_rule
#  -------------
#
# This table defines the rules of the pipeline, 
# as well as some metadata about these.
#
# This table registers the following attributes:
# - rule_ID: Text - An unique identifier of the rules.
# - rule_order: Integer - The order of execution of the rule.
# - rule_description: Text - A textual description of the rule.
# - rule_duration: Integer - The time after which the rule should be 
#                             considered as failed (time out).
# - log_path: Text - The path to the log file.
#
class pipeline_rule(models.Model):
    rule_id = models.TextField(primary_key=True, editable=False, max_length = 200,)
    rule_order = models.IntegerField(default=0, null = True)
    rule_description = models.TextField(max_length = 200, default="", blank=True, null = True)
    rule_duration = models.IntegerField(default=0, null = True)
    log_path = models.TextField(max_length = 200, default="", blank=True, null = True)


## output_file
#  -----------
#
# This table defines the common paths of the output files.
# 
# This table registers the following attributes:
# - file_accession: Text - An unique identifier of the output.
# - file_description: Text - A textual description of the output.
# - file_path: Text - The common path of the file.
#
class output_file(models.Model):
    file_accession = models.TextField(primary_key=True,  editable=False)
    file_description = models.TextField(max_length = 200, default="", blank=True, null = True)    
    file_path = models.TextField(max_length = 200, default="", blank=True, null = True)
    rule_id = models.TextField(editable=False, max_length = 200,)
    
## job_infos
#  ---------
#
# This table aims to contain information about the jobs 
# started from the web interface. 
# This table registers the following attributes:
# - job_id: String - An unique identifier of the job.
# - email: String - The email of the user.
# - submission_date: Date - The date at which the job has been submitted.
# - status: String - The status of the job.
# - run_name: String - The name of the job as defined by the user.
# - target_name: String - The name of the target organism.
# - query_name: String - The name of the query organism as defined by the user.
# - about: Text - The description of the run as added by the user.
# 
class Job_infos(models.Model):
    job_id = models.CharField(primary_key=True, max_length=255)
    email = models.CharField(max_length=255)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255)
    run_name = models.CharField(max_length=255)
    target_name = models.CharField(max_length=255)
    query_name = models.CharField(max_length=255)
    about = models.TextField(max_length=65535)

    