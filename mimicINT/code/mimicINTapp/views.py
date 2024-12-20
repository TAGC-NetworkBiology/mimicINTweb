from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.core.files.storage import default_storage
from django.db.models import *
from django.conf import settings
from django.http import JsonResponse

from mimicINTapp.models import *
from mimicINTapp.forms import *
from mimicINTapp.functions import *

import os
import shortuuid
import codecs
import yaml
import csv
import json
import zipfile

from datetime import datetime
from decimal import Decimal
from itertools import groupby

import subprocess
import shutil


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

#Vue de la page d'accueil
def home(request,):
    mynews = news_part.objects.order_by(F('news_ID').desc(nulls_last=True))
    mytexts = home_text.objects.order_by('text_ID')
    return render_to_response("helloDJ/home.html",
                               {'title' : "mimicINT", 'page': 'home', 'news_list': mynews, 'text_list': mytexts})


#Vue de la page tutoriel (pour le moment elle sert de test du theme de l'application)
def tutorial(request,):
    return render_to_response("helloDJ/tutorial.html",
                               {'title' : "mimicINT", 'page': 'tutorial',})
                               
#Vue de la page tutoriel (pour le moment elle sert de test du theme de l'application)
def documentation(request,):
    return render_to_response("helloDJ/documentation.html",
                               {'title' : "mimicINT", 'page': 'documentation',})

#Vue de la page About (pour le moment elle sert de test du theme de l'application)
def about(request,):
    return render_to_response("helloDJ/about.html",
                               {'title' : "mimicINT", 'page': 'about',})


#Vue de la page du formulaire d'inference
def form(request,):
    form = MyForm()
    mysettings = setting_prediction.objects.order_by('setting_ID')
    
    example_path = os.path.join(settings.COMMON_DIR, '/jobs/common_files/example/example_set.fasta')
    with open(example_path, 'r') as file:
        fasta_example = file.read()
    fasta_example = fasta_example.replace("\n", "\\n")
    

    return render(request, 'helloDJ/form.html', {'title' : "mimicINT", 'form': form, 'page': 'prediction', 'setting_list': mysettings, 'fasta_example': fasta_example })


#Vue permettant la transition entre le form et le pipeline
#recupere la methode POST et creait le dossier de job et son fichier de config
#Dans cette partie il reste a verifier le contenu des champs input et le format FASTA
def pre_pipeline(request,):
    #recuperation de la methode POST
    if request.method == 'POST':
        query_sequences = request.POST.get('query_sequencies', False) #query_fasta_file dans config_user.yaml
        run_name = request.POST.get('run_name', False)
        microbe_species = request.POST.get('microbe_species', False)
        query_informations = request.POST.get('query_informations', False)        
        interaction_templates = request.POST.get('interaction_templates', False)
        iucut = request.POST.get('iucut', False) 
        minregion = request.POST.get('minregion', False) 
        conserved_motifs = request.POST.get('conserved_motifs', False)
        conserved_motifs = int(conserved_motifs)
        conserved_motifs = 10 ** -conserved_motifs
        conserved_motifs = str(conserved_motifs)
        iumethod = request.POST.get('iumethod', False)
        simplify_seq_name = request.POST.get('simplify_seq_name', False)
        domain_score_threshold = request.POST.get('domain_score_threshold', False)

        if domain_score_threshold == "0":
            domain_score_filter = "A"
        else:
            domain_score_filter = "D"

        if simplify_seq_name == False:
            simplify_seq_name = 'False'
        else:
            simplify_seq_name = 'True'

        #creation d'un ID unique
        run_id = shortuuid.uuid()
        #genere la date actuelle
        run_date = datetime.now()
        run_date = run_date.strftime("%Y-%m-%d %H:%M:%S")


        #Inserer run_id et run_date dans la table job_infos
        Job_infos.objects.create(job_id=run_id, submission_date=run_date)
        
        #creer le repertoire et ses fichiers
        job_dir = os.path.join(settings.JOBS_DIR, '/jobs/'+run_id)

        config_file = job_dir+"/config/config.yaml"
        config_cluster_file = job_dir + "/config/config_cluster.json"
        snakemake_file = job_dir+"/snakemake.log"
        start_file = job_dir+"/start_snakemake"
        resume_file = job_dir+"/resume.txt"
        fasta_file = job_dir+"/input/sequences/query_sequences.fasta"
        fasta_file_config = "input/sequences/query_sequences.fasta"
        workflow_path = job_dir+"/workflow/mimicint_interpro_snakefile"
        rule_index_file = os.path.join(job_dir, 'rule_index')

        os.makedirs(job_dir+"/input", exist_ok=True)
        os.makedirs(job_dir+"/output", exist_ok=True)
        os.makedirs(job_dir+"/config", exist_ok=True)
        os.makedirs(job_dir + "/workflow", exist_ok=True)

        source = settings.COMMON_DIR + '/input/' #source = os.path.join(settings.COMMON_DIR, '/common_files/input/')
        destination = os.path.join(settings.JOBS_DIR, run_id+'/input')
        copytree (source, destination, symlinks=False, ignore=None)

        source = settings.COMMON_DIR + '/output/'#os.path.join(settings.COMMON_DIR, '/common_files/output/')
        destination = os.path.join(settings.JOBS_DIR, run_id+'/output')
        copytree (source, destination, symlinks=False, ignore=None)

        source = '../mimicINT_InterPro'
        destination = job_dir + '/mimicINT_InterPro'
        os.symlink(source, destination, target_is_directory=True)

        source = '../common_files/Docker'
        destination = job_dir+'/Docker'
        os.symlink(source, destination, target_is_directory=True)

        #initialise le fichier rule_index à 0
        open_rule_index = open(rule_index_file, 'w')
        open_rule_index.writelines('0')
        open_rule_index.close()

        with open(settings.COMMON_DIR + '/config/config.yaml', 'r') as read_config_file:
            lines = read_config_file.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("query_fasta_file:"):
                lines[i] = "query_fasta_file: " + fasta_file_config + "\n"
            elif lines[i].startswith("score_threshold_interpro_query:"):
                lines[i] = "score_threshold_interpro_query: " + conserved_motifs + "\n" #score_threshold_interpro_query
            elif lines[i].startswith("minregion:"):
                lines[i] = "minregion: " + minregion + "\n" #minregion
            elif lines[i].startswith("iucut:"):
                lines[i] = "iucut: " + iucut + "\n" #detection threshold en nom de variable
            elif lines[i].startswith("iumethod:"):
                lines[i] = "iumethod: " + iumethod + "\n"
            elif lines[i].startswith("simplify_seq_name:"):
                lines[i] = "simplify_seq_name: " + simplify_seq_name + "\n"
            elif lines[i].startswith("domain_score_threshold:"):
                lines[i] = "domain_score_threshold: " + domain_score_threshold + "\n"
            elif lines[i].startswith("domain_score_filter:"):
                lines[i] = "domain_score_filter: " + domain_score_filter + "\n"

        # write the modified config file
        with open(config_file, 'w') as write_config_file:
            write_config_file.writelines(lines)

        #recupere le contenu du champs input et creer le fichier fasta
        if query_sequences != "":
            open_fasta = open(fasta_file, 'w')
            open_fasta.writelines(query_sequences)
            open_fasta.close()


        #genere le fichier resume
        open_resume = open(resume_file, 'w')
        lines = ["Job ID: "+run_id+" \n","Date: "+str(run_date)+" \n"]
        open_resume.writelines(lines)
        open_resume.close()

        #genere le fichier snakemake
        open_snakemake = open(snakemake_file, 'w')
        open_snakemake.close()

        #genere le fichier de workflow
        open_workflow = open(workflow_path, 'w')
        with open (settings.COMMON_DIR+'/workflow/mimicint_interpro_snakefile', 'r') as workflow_file:
            open_workflow.write(workflow_file.read())
        open_workflow.close()

        #genere le fichier config.json
        write_config_cluster = open(config_cluster_file, 'w')
        with open (settings.COMMON_DIR+'/config/config_cluster.json', 'r') as read_config_cluster_file:
            write_config_cluster.write(read_config_cluster_file.read())
        write_config_cluster.close()
        with open(config_cluster_file, 'rt') as read_config_cluster_file_run:
            x = read_config_cluster_file_run.read()
        with open(config_cluster_file, 'wt') as write_config_cluster_file_run:
            x = x.replace('PUT_RUNID', run_id)
            write_config_cluster_file_run.write(x)

        #genere le fichier start
        open_start = open(start_file, 'w')
        open_start.close()

        #genere le fichier rule_index


        #return HttpResponseRedirect('/prediction/'+run_id)
        return HttpResponseRedirect('/results/'+run_id)
        
    else:
        return HttpResponseRedirect('/prediction')




#Vue de la page d'accueil
#Tous les codes suivants sont encore en phase de developpement
#Cette vue doit etre connectee au model des regles du pipeline
def pipeline (request, run_id=""):
#     #recupere la date actuelle
#     now_date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
#     now_date = datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")
#
#
#     job_dir = os.path.join(settings.JOBS_DIR, '/jobs/'+run_id)
#
#     resume_file = job_dir+"/resume.txt"
#
#     #on recupere la date dans le fichier resume
#     with open(resume_file,'r') as file:
#         for i in range(2):
#             date_line = file.readline()
#     run_date = date_line.replace("Date: ", "")
#     run_date = run_date.replace(" \n", "")
#     run_date = datetime.strptime(run_date, "%Y-%m-%d %H:%M:%S")
#
#     #compare la date actuelle et celle du fichier resume
#     datetime_difference = now_date - run_date
#     minutes_difference = datetime_difference.seconds / 60
#
#
#     #si le temps est depasse on renvoie la reponse vers le formulaire (erreur)
#
#
#     if minutes_difference > 15:
#         return HttpResponseRedirect('/prediction')
#
#     subprocess.call("echo test", shell=True)
#     stop = 0
#     wait = True
#     outputs = output_file.objects.all() #outputs -> le contenu de la table output_file de la bd (càd toutes les outputs attendues)
#     rules = pipeline_rule.objects.all().order_by('rule_order') #rules -> le contenu de la table pipeline_rule (càd toutes les règles du pipeline)
#     print("test")                                            #Ces règles sont triées par ordre d'éxécution (rule _order)
#     for element in rules: #pour chaque règle
#         status_path = job_dir + '/job_status/start_' + element.rule_ID  # Récupération du chemin du statut de la règle
#         if os.path.exists(status_path): #Si le status existe (càd si la règle s'est lancée)
#             for bd_output in outputs: #Pour chaque output...
#                 if bd_output.rule_id == element.rule_ID: #...généré par la règle
#                     if not os.path.exists(job_dir + bd_output.file_path):  # On vérifie l'inexistance du fichier d'output
#                         subprocess.call("echo Rule1:" + bd_output.rule_id + " >> sortie", shell=True)
#                         with open(status_path, 'r') as file:
#                             date_start = file.readline()  # Récupération de la date de début de la règle
#                             date_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S\n")  # Transformation de la chaine en date
#                             difference = now_date - date_start  # Calcul du temps écoulé depuis le début de la règle
#                             difference_min = difference.seconds / 60  # Calcul de ce temps en minutes
#                         if difference_min > element.rule_duration:  # Si le temps d'éxecution de la règle (dans la BD) est dépassé, on va voir Slurm
#                             state = ""
#                             name = run_id + "_" + element.rule_ID  # On part du principe que les jobs seront nommés <id du run>-<id de la règle>
#                             with open(JOBS_DIR + "/slurm_squeue.txt", 'r') as file:  # Ouverture et lecture de slurm_squeue.txt
#                                 for line in file:  # Pour chaque ligne dans le fichier (ligne: <nom du job> <Id du job> <Etat du job>)
#                                     end = False
#                                     i = 1
#                                     job_name = line[0]
#                                     while not end:
#                                         if line[i] == ' ' and line[i - 1] != ' ':  # Si le premier mot de la ligne (le nom du job) est passé, on s'arrête
#                                             end = True
#                                         else:  # Sinon, on continue
#                                             job_name = job_name + line[i]  # job_name devient ainsi le nom du job correspondant à la ligne
#                                         i = i + 1
#                                     if job_name == name:  # Si on trouve la ligne du job cherché
#                                         end = False
#                                         column = 1
#                                         while not end:
#                                             if line[i] != ' ' and line[i - 1] == ' ':  # Chaque fois qu'on passe à un nouveau mot dans la ligne
#                                                 column = column + 1
#                                                 if column == 3:  # Si on atteint le mot 3 (l'état du job)
#                                                     while line[i] != ' ':
#                                                         state = state + line[i]
#                                                         i = i + 1
#                                                     end = True
#                                             i = i + 1
#                                 if state != "PENDING" and state != "RUNNING":  # Si le job n'est pas en cours d'éxécution ou en attente (et que l'output n'a pas été généré)
#                                     # if state == "BOOT_FAIL\n" or state == "CANCELLED\n" or state == "FAILED\n" or state == "NODE_FAIL\n" or state == "OUT_OF_MEMORY\n" or state == "TIMEOUT\n" or state == "unknown\n":
#                                     # Vérification de l'état du job. Résumé des différents états possibles: https://slurm.schedmd.com/squeue.html#lbAG. Si le job a échoué, alors...
#                                     # Afficher une page d'erreur
#                                     subprocess.call("echo Echec >> sortie", shell=True)
#                                     subprocess.call("echo" + element.rule_ID + ">> sortie", shell=True)
#                                     subprocess.call("echo" + bd_output.rule_id + ">> sortie", shell=True)
#                                     subprocess.call("echo" + difference_min + ">> sortie", shell=True)
#                                     return HttpResponseRedirect('/prediction')  # ça pour l'instant
#                                 else: #Si l'état du job est pending ou running
#                                     wait = True
#                                     break
#                         else: #Si le temps d'éxecution maximum n'est pas dépassé
#                             wait = True
#                             break
#                     else: #Si le fichier d'ouput est trouvé
#                         stop = stop+1
#                         wait = False
#                         subprocess.call("echo " + bd_output.rule_id + " >> reussite", shell=True)
#                         if stop == len(outputs): #Si stop est égal au nombre d'output (càd tout les outputs ont été générés)
#                             subprocess.call("echo Réussite >> sortie", shell=True)
#                             return HttpResponseRedirect('/results/' + 'runone')  # Affichage des résultats
#         if wait: #wait == True si: la règle ne s'est pas lancé OU le temps d'éxecution maximum n'est pas dépassé OU l'état du job est pending ou running
#          break

      
	 	return  render_to_response("helloDJ/pipeline.html",{'title': "mimicINT", 'page': 'pipeline', 'run_id': run_id, })
      
      
 #     return HttpResponseRedirect('/results/'+'run_id') # Affichage des résultats



    # for element in outputs:
    #     if not os.path.exists(job_dir + element.file_path): #On vérifie l'inexistance des fichiers d'output
    #         rule = pipeline_rule.objects.get(rule_ID = element.rule_id) #rule est la règle du pipeline générant l'ouput correspondant
    #         status_path = job_dir + '/job_status/start_' + rule.description #Récupération du cemin du statut de la règle
    #         if os.path.exists(status_path):
    #             with open(status_path, 'r') as file:
    #                 date_start = file.readline() #Récupération de la date de début de la règle
    #             date_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S") #Transformation de la chaine en date
    #             difference = now_date - date_start #Calcul du temps écoulé depuis le début de la règle
    #             difference_min = difference.seconds /60 #Calcul de ce temps en minutes
    #             if difference_min > rule.rule_duration: #Si le temps d'éxecution de la règle (dans la BD) est dépassé, on va voir Slurm
    #                 state = ""
    #                 name = run_id+"-"+rule.rule_ID #On part du principe que les jobs seront nommés <id du run>-<id de la règle>
    #                 with open(JOBS_DIR+"/slurm_squeue.txt",'r') as file: #Ouverture et lecture de slurm_squeue.txt
    #                     for line in file: #Pour chaque ligne dans le fichier (ligne: <nom du job> <Id du job> <Etat du job>)
    #                         end = False
    #                         i = 1
    #                         job_name = line[0]
    #                         while end == False:
    #                             if line[i] == ' ' and line[i-1] != ' ': #Si le premier mot de la ligne (le nom du job) est passé, on s'arrête
    #                                 end = True
    #                             else: #Sinon, on continue
    #                                 job_name = job_name + line[i] #job_name devient ainsi le nom du job correspondant à la ligne
    #                             i = i+1
    #                         if job_name == name: #Si on trouve la ligne du job cherché
    #                                 end = False
    #                                 column = 1
    #                                 while end == False:
    #                                     if line[i] != ' ' and line[i-1] == ' ': #Chaque fois qu'on passe à un nouveau mot dans la ligne
    #                                         column = column + 1
    #                                         if column == 3: #Si on atteint le mot 3 (l'état du job)
    #                                             while line[i] != ' ':
    #                                                 state = st + line[i]
    #                                                 i = i+1
    #                                             end = True
    #                                     i = i+1
    #                 if state != "PENDING" or state != "RUNNING": #Si le job n'est pas en cours d'éxécution ou en attente (et que l'output n'a pas été généré)
    #                 #if state == "BOOT_FAIL\n" or state == "CANCELLED\n" or state == "FAILED\n" or state == "NODE_FAIL\n" or state == "OUT_OF_MEMORY\n" or state == "TIMEOUT\n" or state == "unknown\n":
	# 			#Vérification de l'état du job. Résumé des différents états possibles: https://slurm.schedmd.com/squeue.html#lbAG. Si le job a échoué, alors...
	#             #Afficher une page d'erreur
    #                     return HttpResponseRedirect('/prediction') #ça pour l'instant
    #         wait = True #Arrive lorsqu'un ouput n'a pas été généré, et que le job le générant n'a pas encore démarrer ou le temps normal d'éxecution n'est pas dépassé
    # if wait:
    #     return render_to_response("helloDJ/pipeline.html",{'title' : "mimicINT",'page': 'pipeline','run_id': run_id,})
    # else:
    #     return HttpResponseRedirect('/results/'+'runone') # Affichage des résultats


#Vue du formulaire permettant d'acceder aux resulats d'un job
def jobs(request,):
    form = jobForm()
    job_not_found = False
    if request.method == "POST":
        job_id = request.POST.get('job_id', False)
        job_dir = os.path.join(settings.JOBS_DIR, '/jobs/'+job_id)
        if os.path.exists (job_dir):
            return HttpResponseRedirect('/results/'+job_id)
        else:
            job_not_found = True
    return render(request, 'helloDJ/jobs.html', {'title' : "mimicINT", 'form': form, 'page': 'jobs', 'job_not_found': job_not_found })



def cytoscape(request, job_id=""):
    if job_id == "":
        job_id="none"
    job_dir = os.path.join(settings.JOBS_DIR, '/jobs/'+job_id)

    if not os.path.exists (job_dir):
        return HttpResponseRedirect('/jobs')

    try:
        network_file = output_file.objects.get(file_accession = "network_json")
        network_path = job_dir + network_file.file_path
        json_data = open(network_path)
        network_load = json.load(json_data)    # deserializes it
        network_dumps = json.dumps(network_load)   # json formatted string

        return render_to_response("helloDJ/cytoscape.html",
                                   {'title' : 'mimicINT', 'page': 'jobs', 'data_network': network_dumps})

    except output_file.DoesNotExist:
        error_user = "5 Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        type_error = "105"

        return render(
            request,
            "helloDJ/error.html",
            {
                'title': 'Worklow error',
                'page': 'jobs',
                'error_user': error_user,
                'type_error': type_error,
            }
        )


# Vue des resultats
# Le dernier element de l'occurence correspond a l'ID du job
def result(request, job_id=""):
    #Si l'ID n'existe pas en renvoie vers le formulaires des jobs
    if job_id == "":
        job_id="none"
    job_dir = os.path.join(settings.JOBS_DIR, '/jobs/'+job_id)
    json_dir = os.path.join(settings.JOBS_DIR, '/jobs/'+job_id + '/output')
    
    if not os.path.exists (job_dir):
        return HttpResponseRedirect('/jobs')

    #Verification existence file_error_workflow
    error_workflow = os.path.join( job_dir, 'file_error_workflow' )
    if os.path.exists( error_workflow ):
        with open( error_workflow ) as error_workflow_f:

            line = error_workflow_f.readline()
            while line:
                parse = line.split( ' ' )
                type_error = parse[1]
                line = error_workflow_f.readline()

        if type_error == "101":
            error_user = "1 Lorem ipsum dolor sit amet, consectetur adipiscing elit."

        if type_error == "102":
            error_user = "2 Lorem ipsum dolor sit amet, consectetur adipiscing elit."

        if type_error == "103":
            error_user = "3 Lorem ipsum dolor sit amet, consectetur adipiscing elit."

        if type_error == "104":
            error_user = "4 Lorem ipsum dolor sit amet, consectetur adipiscing elit."

        return render(
            request,
            "helloDJ/error.html",
            {
                'title': 'Worklow error',
                'page': 'jobs',
                'error_user': error_user,
                'type_error': type_error,
            }
        )

    end_workflow = os.path.join(job_dir, 'job_status/END_WORKFLOW')
    if os.path.exists(end_workflow):
        '''
        #Recuperation du fichier json pour cytoscape
        network_file = output_file.objects.get(file_accession = "network_json")
        network_path = job_dir + network_file.file_path
        json_data = open(network_path)
        network_load = json.load(json_data)    # deserializes it
        network_dumps = json.dumps(network_load)   # json formatted string

        #Recuperation du fichier JSON pour feature-viewer
        feature_file = output_file.objects.get(file_accession = "features_json")
        feature_path = job_dir + feature_file.file_path
        feature_json = open(feature_path)
        feature_load = json.load(feature_json)    # deserializes it
        feature_dumps = json.dumps(feature_load)   # json formatted string
        '''
        '''
        #Recuperation des interactions domaine-domain
        ddi_interaction_file = output_file.objects.get(file_accession = "ddi_interactions_tsv")
        ddi_interaction_path = directory_path + ddi_interaction_file.file_path
    
        domain_interaction_list = []
        with default_storage.open(ddi_interaction_path) as tsvfile:
            maketsv = codecs.iterdecode(tsvfile, "utf-8")
            domain_interaction_tsv = csv.reader(maketsv, delimiter="\t")
            next (domain_interaction_tsv)
            for line in domain_interaction_tsv:
                line += ["Domain"]
                domain_interaction_list += [line]
        tsvfile.close()
    
    
        #Recuperation des interactions SLiM-domain
        dmi_interaction_file = output_file.objects.get(file_accession = "dmi_interactions_tsv")
        dmi_interaction_path = directory_path + dmi_interaction_file.file_path
    
        motif_interaction_list = []
        with default_storage.open(dmi_interaction_path) as tsvfile:
            maketsv = codecs.iterdecode(tsvfile, "utf-8")
            motif_interaction_tsv = csv.reader(maketsv, delimiter="\t")
            next (motif_interaction_tsv)
            for line in motif_interaction_tsv:
                line += ["SLiM"]
                motif_interaction_list += [line]
        tsvfile.close()
    
        #Fusion des fichiers ddi et dmi pour la tables des interactions inferees
        interaction_list = domain_interaction_list + motif_interaction_list
    
    
        #Creation des donnees de la table des domaines et motifs des proteines query
        query_domain_list = []
        for int_el in interaction_list:
            new_element = int_el [0:5]
            new_element.append(int_el[10])
            query_domain_list.append(new_element)
    
            query_domain_list.sort()
            query_domain_list = list (query_domain_list for query_domain_list,_ in groupby(query_domain_list))
    
    
        #Recuperation des donnes pour la table des proteines query
        query_protein_file = output_file.objects.get(file_accession = "disorder_propensities_tsv")
        query_protein_path = directory_path + query_protein_file.file_path
        query_protein_list = []
        with default_storage.open(query_protein_path) as tsvfile:
            maketsv = codecs.iterdecode(tsvfile, "utf-8")
            query_protein_tsv = csv.reader(maketsv, delimiter="\t")
            next (query_protein_tsv)
            for line in query_protein_tsv:
                line[2] = Decimal(str(round(float(line[2]),2)))
                query_protein_list += [line]
        tsvfile.close()
    
    
        #Recuperation des donnees pour la table des annotations
        gprofiler_path = directory_path + "/output/8_gprofiler/gprofiler_result.tsv"
        gprofiler_list = []
        with default_storage.open(gprofiler_path) as tsvfile:
            maketsv = codecs.iterdecode(tsvfile, "utf-8")
            gprofiler_tsv = csv.reader(maketsv, delimiter="\t")
            next (gprofiler_tsv)
            for line in gprofiler_tsv:
                line.pop()
                line[3] = Decimal(str(round(float(line[3]),5)))
                line[7] = Decimal(str(round(float(line[7]),5)))
                line[8] = Decimal(str(round(float(line[8]),5)))
                gprofiler_list += [line]
    
            tsvfile.close()
    
    
        #Boucle permettant d'enlever les interactions doublons
        new_interaction_list  = []
        for int_el in interaction_list:
            new_element = int_el [0:2]
            new_element.append(int_el [4])
            new_element.append(int_el [5])
            new_element.append(int_el [6])
            new_element.append(int_el[9])
            new_element.append(int_el [10])
            new_interaction_list.append(new_element)
            new_interaction_list.sort()
            new_interaction_list = list (new_interaction_list for new_interaction_list,_ in groupby(new_interaction_list))
        '''

		  
    
        query_protein_path = job_dir + '/output/mimicINT_InterPro/7_renamed_sequences/query_disorder_prop.tsv'	
        with open(query_protein_path) as tsvfile:
            interaction_tsv = csv.reader(tsvfile, delimiter="\t")
            next (interaction_tsv)
            interaction_list = list(interaction_tsv)
            rows_to_keep = []
            for row in interaction_list:
                rows_to_keep.append(('<a href="https://www.uniprot.org/uniprotkb/'+ row[0] + '" target="_blank">'+ row[0] + '</a>', row[1] , format(float(row[2]), '.3f')))            
        tsvfile.close()
        #print(interaction_tsv)
        
        ## sauvegarde dans un fichier json
        query_protein_path_json = json_dir + '/query_disorder_prop.json'
        json_output = str(json.dumps(rows_to_keep))
        print(json_output)
        #print (os.getenv("HOME"))
        with open(query_protein_path_json, "w+") as json_prot:
            json_prot.write(json_output)
            json_prot.close()

			
        domain_domain_count = 0
        slim_domain_count = 0
        unique_interaction_count = 0
        interaction_path = job_dir + '/output/mimicINT_InterPro/7_renamed_sequences/all_interactions.tsv'

        with open(interaction_path) as tsvfile:
            interaction_tsv = csv.reader(tsvfile, delimiter="\t")
            next (interaction_tsv)
            concatened_data = [item[0] + item[1] for item in interaction_tsv]      
            for row in set(concatened_data):
                unique_interaction_count +=1       
        tsvfile.close()

        with open(interaction_path) as tsvfile:
            interaction_tsv = csv.reader(tsvfile, delimiter="\t")
            next (interaction_tsv)
            for row in interaction_tsv:
                if row[2] == 'domain-domain':
                    domain_domain_count += 1
                elif row[2] == 'slim-domain':
                    slim_domain_count += 1
        tsvfile.close()

        '''
        protein_path = job_dir + '/output/9_web_files/query_protein.tsv'
        with open(protein_path) as tsvfile:
            protein_tsv = csv.reader(tsvfile, delimiter="\t")
            next (protein_tsv)
            protein_list = list(protein_tsv)
        tsvfile.close()
        '''
        #tableau de resultats formates pour le json
        row_domains_slims = []
        
        domain_path = job_dir + '/output/mimicINT_InterPro/7_renamed_sequences/query_domains.tsv'
        with open(domain_path) as tsvfile:
            domain_tsv = csv.reader(tsvfile, delimiter="\t")
            next (domain_tsv)
            domain_list = list(domain_tsv)
            tsvfile.close()

        for row in domain_list: 
            row_domains_slims.append((row[0],'<a href="https://www.ebi.ac.uk/interpro/entry/InterPro/'+ row[7]+ '" target="_blank">'+ row[7]+ '</a>',row[3],row[4],row[5], "domain"))
            
        

        slim_path = job_dir + '/output/mimicINT_InterPro/7_renamed_sequences/query_slims.tsv'
        with open(slim_path) as tsvfile:
            slim_tsv = csv.reader(tsvfile, delimiter="\t")
            next (slim_tsv)
            slim_list = list(slim_tsv)
        tsvfile.close()

        for row in slim_list: 
            row_domains_slims.append((row[0],'<a href="http://elm.eu.org/elms/'+ row[1] +'" target="_blank">'+row[1]+'</a>',row[2],row[3],row[4], "SLiM"))

        #print(row_domains_slims)
        
        ## sauvegarde dans un fichier json        
        query_domains_slims_path_json = json_dir + '/query_domains_slims.json'
		  
        json_output = str(json.dumps(row_domains_slims))
        #print(json_output)
        
        with open(query_domains_slims_path_json, "w+") as json_file:
            json_file.write(json_output)
            json_file.close()


        enrichment_path = job_dir + '/output/mimicINT_InterPro/8_gprofiler/gprofiler_result.tsv'
        with open(enrichment_path) as tsvfile:
            enrichment_tsv = csv.reader(tsvfile, delimiter="\t")
            next (enrichment_tsv)
            enrichment_list = list(enrichment_tsv)
        tsvfile.close()
        
        #tableau de resultats formates pour le json
        row_gprofiler = []
        for row in enrichment_list: 
            #print(row)
            row_gprofiler.append((row[0:7]))



        ## sauvegarde dans un fichier json
        gprofiler_path_json = json_dir + '/gprofiler_results.json'
		  
        json_output = str(json.dumps(row_gprofiler))
        #print(json_output)
        
        with open(gprofiler_path_json, "w+") as json_file:
            json_file.write(json_output)
            json_file.close()


        sequence_name_path = job_dir + '/output/mimicINT_InterPro/7_renamed_sequences/sequence_names.tsv'
        nb_sequence = 0
        with open(sequence_name_path) as tsvfile:
            sequence_name_tsv = csv.reader(tsvfile, delimiter="\t")
            next (sequence_name_tsv)
            for row in sequence_name_tsv:
                nb_sequence += 1
        tsvfile.close()
        #
        host_sequences = set([])
        
        #tableau de resultats formates pour le json
        row_inferred = []
        
        
        inferred_ddi_path = job_dir + '/output/mimicINT_InterPro/5_interactions/inferred_ddi_interactions.tsv'
        selected_columns = [0, 1, 5, 6]
        selected_values = set()
        with open(inferred_ddi_path) as tsvfile:
            inferred_ddi_tsv = csv.reader(tsvfile, delimiter="\t")
            next (inferred_ddi_tsv)
            for row in inferred_ddi_tsv:
                selected_row = [row[i] for i in selected_columns]
                selected_values.add(tuple(selected_row))
                
                host_sequences.add(row[5])
        tsvfile.close()
        inferred_ddi_list = list(selected_values)

        for row in inferred_ddi_list: 
            #print(row)
            row_inferred.append((row[0],
            						'<a href="https://www.ebi.ac.uk/interpro/entry/InterPro/'+ row[1] +'" target="_blank">'+row[1]+'</a>',
           	 						'<a href="https://www.uniprot.org/uniprotkb/'+ row[2] +'" target="_blank">'+row[2]+'</a>',
            						'<a href="https://www.ebi.ac.uk/interpro/entry/InterPro/'+ row[3] +'" target="_blank">'+row[3]+'</a>',
            						"domain-domain"))


        selected_values = set()
        inferred_dmi_path = job_dir + '/output/mimicINT_InterPro/5_interactions/inferred_dmi_interactions.tsv'
        with open(inferred_dmi_path) as tsvfile:
            inferred_dmi_tsv = csv.reader(tsvfile, delimiter="\t")
            next (inferred_dmi_tsv)
            for row in inferred_dmi_tsv:
                selected_row = [row[i] for i in selected_columns]
                selected_values.add(tuple(selected_row))
                #
                host_sequences.add(row[5])
        tsvfile.close()
        inferred_dmi_list = list(selected_values)

        for row in inferred_dmi_list: 
            #print(row)
            row_inferred.append((row[0],
            						'<a href="http://elm.eu.org/elms/'+ row[1] +'" target="_blank">'+row[1]+'</a>',
           	 						'<a href="https://www.uniprot.org/uniprotkb/'+ row[2] +'" target="_blank">'+row[2]+'</a>',
            						'<a href="https://www.ebi.ac.uk/interpro/entry/InterPro/'+ row[3] +'" target="_blank">'+row[3]+'</a>',
            						"slim-domain"))



        ## sauvegarde dans un fichier json
        inferred_path_json = json_dir + '/inferred_ddi_dmi_interractions.json'
		  
        json_output = str(json.dumps(row_inferred))
        #print(json_output)
        
        with open(inferred_path_json, "w+") as json_file:
            json_file.write(json_output)
            json_file.close()


        #tableau de resultats formates pour le json
        row_filtered = []

        selected_values = set()
        inferred_filtered_dmi_path = job_dir + '/output/mimicINT_InterPro/5_interactions/filtered_dmi_interactions.tsv'
        with open(inferred_filtered_dmi_path) as tsvfile:
            filtered_dmi_tsv = csv.reader(tsvfile, delimiter="\t")
            next (filtered_dmi_tsv)
            for row in filtered_dmi_tsv:
                selected_row = [row[i] for i in selected_columns]
                selected_values.add(tuple(selected_row))
        tsvfile.close()
        inferred_filtered_dmi_list = list(selected_values)


        for row in inferred_ddi_list: 
            #print(row)
            row_filtered.append((row[0],
            						'<a href="https://www.ebi.ac.uk/interpro/entry/InterPro/'+ row[1] +'" target="_blank">'+row[1]+'</a>',
           	 						'<a href="https://www.uniprot.org/uniprotkb/'+ row[2] +'" target="_blank">'+row[2]+'</a>',
            						'<a href="https://www.ebi.ac.uk/interpro/entry/InterPro/'+ row[3] +'" target="_blank">'+row[3]+'</a>',
            						"domain-domain"))

        for row in inferred_filtered_dmi_list: 
            #print(row)
            row_filtered.append((row[0],
            						'<a href="http://elm.eu.org/elms/'+ row[1] +'" target="_blank">'+row[1]+'</a>',
           	 						'<a href="https://www.uniprot.org/uniprotkb/'+ row[2] +'" target="_blank">'+row[2]+'</a>',
            						'<a href="https://www.ebi.ac.uk/interpro/entry/InterPro/'+ row[3] +'" target="_blank">'+row[3]+'</a>',
            						"slim-domain"))



        ## sauvegarde dans un fichier json
        filtered_path_json = json_dir + '/filtered_ddi_dmi_interractions.json'
		  
        json_output = str(json.dumps(row_filtered))
        #print(json_output)
        
        with open(filtered_path_json, "w+") as json_file:
            json_file.write(json_output)
            json_file.close()




        nb_host_sequence = len(host_sequences)

        return render(
            request,
            "helloDJ/result.html",
            {
                'title' : 'mimicINT',
                'page': 'jobs',
                'job_path': True,
                'job_id': job_id,
         #       'interaction_list': interaction_list,
                #'query_protein_list': protein_list,
          #      'query_domain_list': domain_list,
          #      'query_slim_list': slim_list,
                #'data_network': network_dumps,
                #'data_features': feature_dumps,
                #
                'nb_host_sequence' : nb_host_sequence,
                'nb_sequence': nb_sequence,
                'domain_domain_count': domain_domain_count,
                'slim_domain_count': slim_domain_count,
                'unique_interaction_count': unique_interaction_count,
           #     'inferred_ddi_list': inferred_ddi_list,
           #     'inferred_dmi_list': inferred_dmi_list,
           #     'inferred_filtered_dmi_list': inferred_filtered_dmi_list,
           #     'enrichment_list': enrichment_list,
            }
        )

    else:
        context = {
            'title': 'Worklow in progress',
            'page': 'jobs',
            'job_id': job_id,
        }
        return  render_to_response("helloDJ/pipeline.html",{'title': "mimicINT", 'page': 'pipeline', 'run_id': job_id, })
   #     return render(request, 'helloDJ/progress.html', context=context)
  # 	 	return  render_to_response("helloDJ/pipeline.html",{'title': "mimicINT", 'page': 'pipeline', 'run_id': job_id, })
		#return render(request, 'helloDJ/pipeline.html', context=context)
     
def progress(request, job_id):
    try:
        progress = progress_time_run(job_id)

        total_rule = pipeline_rule.objects.all().count()

        rule_index = get_rule_index(job_id)
            
        return JsonResponse(
            {'progress': progress,
             'total_rule': total_rule,
             'rule_index': rule_index,
             }
        )
    except Job_infos.DoesNotExist:
        return JsonResponse({'error': 'Job not found'})
        
        
def table_json(request, job_id, json_filename):
    job_dir = os.path.join(settings.JOBS_DIR, '/jobs/'+job_id + '/output')
   # zip_folder = os.path.join(job_dir, 'output/mimicINT_InterPro')

    #json_filename = 'query_disorder_prop.json'
    json_path = os.path.join(job_dir, json_filename)
    json_data = open(json_path)
   
    #json_dumps = json.load(json_data)   # json formatted string
    response = HttpResponse(json.dumps(json.load(json_data)))
    return response

def table1(request, job_id):
    job_dir = os.path.join(settings.JOBS_DIR, '/jobs/'+job_id + '/output')
   # zip_folder = os.path.join(job_dir, 'output/mimicINT_InterPro')

    json_filename = 'query_disorder_prop.json'
    json_path = os.path.join(job_dir, json_filename)
    json_data = open(json_path)
   
    #json_dumps = json.load(json_data)   # json formatted string
    response = HttpResponse(json.dumps(json.load(json_data)))
    return response

def download_zip(request, job_id):
    job_dir = os.path.join(settings.JOBS_DIR, '/jobs/'+job_id)
    zip_folder = os.path.join(job_dir, 'output/mimicINT_InterPro')

    zip_filename = job_id + '.zip'
    zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)

    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for root, _, files in os.walk(zip_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, zip_folder))

    with open(zip_path, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(zip_filename)
        return response
