from django.contrib import admin
from .models import *


#Le code ci-dessous permet de connecter les models a la page d'administration

#Table des parametres
@admin.register(setting_prediction)
class settingAdmin(admin.ModelAdmin):
    list_display = ("setting_ID", "setting_name", "tooltip")

#Table des news
@admin.register(news_part)
class newsAdmin(admin.ModelAdmin):
    list_display = ("news_ID", "news_title", "news_content")

#Table des textes de la page d'accueil
@admin.register(home_text)
class textAdmin(admin.ModelAdmin):
    list_display = ("text_ID", "text_title", "text_content")

#Table des fichiers de resultats
@admin.register(output_file)
class fileAdmin(admin.ModelAdmin):
    list_display = ("file_accession", "file_description", "file_path")

#Table des regles du pipeline
@admin.register(pipeline_rule)
class fileAdmin(admin.ModelAdmin):
    list_display = ("rule_id", "rule_order", "rule_description", "rule_duration", "log_path")