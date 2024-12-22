try:
    import os
    import psycopg2
    from psycopg2.extensions import AsIs
    from datetime import datetime
    import subprocess
    import logging
    import logging.handlers
except ImportError as e:
    print( "Erreur concernant les importations necessaire au script :", e )


# Variable for database
USER = "django"
#set your password here
PASSWORD = ""
HOST = "*"
PORT = "5432"
DATABASE = "mimicINT_db"

# Variable for paths
JOBS_DIR = '/home/mimicint/tagc-mimicweb/tagc-mimicint/jobs'
START_SNAKEMAKE_FILE = 'start_snakemake'
END_WORKFLOW_FILE = 'job_status/END_WORKFLOW'
ERROR_WORKFLOW_FILE = 'file_error_workflow'
SQUEUE_FILE = os.path.join( JOBS_DIR, 'slurm_squeue.txt' )
CONTAINER_DIR = '/home/mimicint/tagc-mimicweb/tagc-mimicintw/mimicINT/container'

# Variable to get actual date
now_date = datetime.now()

# Variable for log & error
logger = logging.getLogger( __name__ )
JOBS_STATUS_DIR_NOT_FOUND = \
    "Erreur 101 Le dossier jobs_status n'existe pas alors que le dossier output existe pour ce run"
SQUEUE_FILE_NOT_FOUND = "Le fichier slurm_squeue.txt n'existe pas"
START_RULE_ID_FILE_NOT_FOUND = "Erreur 102 Un des fichiers start_rule_id n'existe pas pour ce run"
CREATE_FILE_NOT_PERMISSION = "Vous n'avez pas les acces pour creer de fichier pour le dossier run : "
LOG_FILE = os.path.join( JOBS_DIR, "log_script.log" )
JOBS_NOT_A_DIR = "Tentative de parcourt d'un element qui n'est pas un dossier"


def log_write(type_error):
    logging.basicConfig(level=type_error,
                        filename=LOG_FILE,
                        filemode="a",
                        format='%(asctime)s - %(levelname)s - %(message)s')
    # log_handler = logging.handlers.WatchedFileHandler(LOG_FILE)
    # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # log_handler.setFormatter(formatter)
    # logger.addHandler(log_handler)
    # logger.setLevel(type_error)


def read_squeue( run_id, rule_id ):
    """
        returns job status according to the file slurm_squeue.txt, run_id and rule_id

        Parameter :
            run_id : str
                id of the current run
            rule_id : str
                id of the current jobs

        Return :
            status_job : str
                status of the jobs
    """

    # go to the job directory and read slurm_squeue.txt
    try:
        with open( SQUEUE_FILE ) as squeue_f:

            # check job statuts according to run_id and rule_id write in slurm_squeue.txt
            line = squeue_f.readline()
            while line:
                parse = line.split( ' ' )
                run_rule_id = parse[0]
                status_jobs = parse[1]
                line = squeue_f.readline()
                if run_rule_id == run_id + '.' + rule_id:
                    return status_jobs

    except FileNotFoundError as e:
        raise FileNotFoundError( SQUEUE_FILE_NOT_FOUND ) from e



def size_of_table():
    """
        returns the size of the table mimicINTapp_pipeline_rule in the database

        Parameter :
        -------------------

        Return :
            size_table : int
                size of the table
    """

    try:
        # connect to database
        connection = psycopg2.connect( "host=%s dbname=%s user=%s password=%s port=%s"
                                       % ( HOST, DATABASE, USER, PASSWORD, PORT ) )
        cursor = connection.cursor()

        # quote the column name, so it is not folded to lower case by PostgreSQL
        column_name = '"mimicINTapp_pipeline_rule"'
        quoted_column_name = AsIs( column_name)

        # execute a SQL command to select every iteration of the table
        postgresql_select_pipeline_rule = \
            "SELECT rule_id, rule_order, rule_duration FROM %s ORDER BY rule_order"
        cursor.execute( postgresql_select_pipeline_rule, ( quoted_column_name,) )

        # take the number (size of table) of every iteration in the table
        table_records = cursor.fetchall()
        size_table = len( table_records )

        # close the connection to database
        cursor.close()
        connection.close()

    except ( Exception, psycopg2.Error ) as e:
        raise Exception ( psycopg2.Error ) from e
    else:
        return size_table


def select_rule ( index ):
    """
        returns rule_id, rule_order, rule_duration when rule_order = index in the table mimicINTapp_pipeline_rule

        Parameter :
            index : int
                index of the current rule_id

        Return :
            rule_id : str
                rule_id of the job when rule_order = index
            rule_order : int
                rule_order of the job when rule_order = index
            rule_duration : int
                rule_duration of the job when rule_order = index
    """

    try:

        # connect to database
        connection = psycopg2.connect( "host=%s dbname=%s user=%s password=%s port=%s"
                                       % ( HOST, DATABASE, USER, PASSWORD, PORT ) )
        cursor = connection.cursor()

        # quote the column name, so it is not folded to lower case by PostgreSQL
        column_name = '"mimicINTapp_pipeline_rule"'
        quoted_column_name = AsIs( column_name)

        # execute a SQL command to select every iteration of the table when rule_order = index
        postgresql_select_pipeline_rule = \
            "SELECT rule_id, rule_order, rule_duration FROM %s WHERE rule_order = %s"
        cursor.execute( postgresql_select_pipeline_rule, ( quoted_column_name, index, ) )

        # take rule_id, rule_order and rule_duration according to the SQL command
        table_records = cursor.fetchall()
        for row in table_records:
            rule_id = row[0]
            rule_order = row[1]
            rule_duration = row[2]

        # close the connection to database
        cursor.close()
        connection.close()

    except ( Exception, psycopg2.Error ) as e:
        raise Exception( psycopg2.Error ) from e

    else:
        return rule_id, rule_order, rule_duration


def create_file( content, path_file ):
    """
        create a file with write inside the var content

        Parameter :
            content : str
                content of the file
            file_error_workflow : str
                path of the file created

        Return :
        ----------------
    """
    try:
        open_error_workflow = open( path_file, 'w' )
        lines = [content]
        open_error_workflow.writelines( lines )
        open_error_workflow.close()

    except PermissionError as e:
        raise PermissionError( CREATE_FILE_NOT_PERMISSION ) from e


def check_job_status( run_id ):
    """
        Check the status of every job according to the current run.
        It's checking if there is some error, or just if the workflow is executing perfectly fine.
        If there is an error, a file_error_workflow is created with inside the type of error.
        If the workflow was executed without error, a file_end_workflow.
        If the workflow is still working and there is no error, the function just stop.

        Parameter :
            run_id : str
                id of the current run

        Return :
        ------------------------------
    """

    # path to get the file wanted
    run_dir = os.path.join( JOBS_DIR, run_id )
    file_error_workflow = os.path.join( run_dir, ERROR_WORKFLOW_FILE )
    job_status_dir = os.path.join( run_dir, 'job_status' )
    ouput_dir = os.path.join( run_dir, 'output' )
    file_start_snakemake = os.path.join( run_dir, 'start_snakemake' )
    rule_index_file = os.path.join(run_dir, 'rule_index')

    # Verify if run_dir exist
    if not os.path.exists( run_dir ):
        return

    # Verify if job_status_dir exist
    if not os.path.exists( job_status_dir ):
        if not os.path.exists( ouput_dir ):
            log_write( logging.DEBUG )
            create_file( '', file_start_snakemake )
            logger.debug( "Recreation du fichier start_snakemake pour le dossier run : " + run_dir )
#        else:
#           create_file( JOBS_STATUS_DIR_NOT_FOUND, file_error_workflow )
#           raise FileNotFoundError( JOBS_STATUS_DIR_NOT_FOUND )

    # loop to check the status of every job, it's loop until the size of the table is reached
    size_table = size_of_table()
    for rule_index in range( 1, size_table + 1 ):

        rule_id, rule_order, rule_duration = select_rule( rule_index )

        # path to get the file according to the rule_id
        status_start_rule_id = os.path.join( job_status_dir, 'start_' + rule_id )
        status_end_rule_id = os.path.join( job_status_dir, 'end_' + rule_id )

        # check if the start file exist for the current job
        if not os.path.exists( status_start_rule_id ):
            break

        # we go check the next job if the current job is finished (end exist)
        elif os.path.exists( status_end_rule_id ):
            print( "start & end de la rule " + rule_id + " existe pour le run_id : " + run_id )
            create_file(str(rule_index), rule_index_file)
            continue

#        try:
#           subprocess.check_call( "docker exec docker-centos7-slurm-snakemake squeue -\"o%j %T \" -h > "
#                                  + JOBS_DIR + "/slurm_squeue.txt", shell=True )
#       except subprocess.SubprocessError as e:
#           raise Exception( subprocess.SubprocessError ) from e

        # read the file squeue.txt to get the status of the job according to SLURM, current run_id and rule_id
        status_slurm_squeue = read_squeue( run_id, rule_id )

        # check if the current job is considered RUNNING by SLURM
        if status_slurm_squeue == 'RUNNING':

            # open and read the file start_rule_id to get the date of creation
            try:
                with open( status_start_rule_id, 'r' ) as file:
                    date_start = file.readline()
                    date_start = datetime.strptime( date_start, "%Y-%m-%d %H:%M:%S\n" )
            except FileNotFoundError as e:
                create_file( START_RULE_ID_FILE_NOT_FOUND + + " (rule : " + rule_id + ")", file_error_workflow )
                raise FileNotFoundError( START_RULE_ID_FILE_NOT_FOUND ) from e

            # calculation of the duration of the job from its beginning until the current date
            time_elapsed = now_date - date_start
            time_elapsed_sec = time_elapsed.total_seconds()
            if time_elapsed_sec < 0:
                time_elapsed_sec = 0

            # check if the current job don't exceed the time write on the database
            if time_elapsed_sec < rule_duration:
                break

            else:
                type_error = "Erreur 103 : le job : " + rule_id + " du run " + run_id + " a pris trop de temps"
                create_file( type_error, file_error_workflow )
                break

        # create an error file because the file_start exist, but it's not considered RUNNING by SLURM
        else:
            pass
#           type_error = "Erreur 104 : le job : " + rule_id + " du run : " \
#                        + run_id + " a commence mais il n est pas considere en cours par SLURM"
#           create_file( type_error, file_error_workflow )
#           break

def get_rule_index(run_id):
    job_dir = os.path.join(JOBS_DIR, run_id)
    rule_index_file = os.path.join(job_dir, 'rule_index')
    with open (rule_index_file) as f:
        start_index = int(f.read().strip())
    return start_index

def check_run_status():
    """
        Check the status of every run in the job directory.
        It's checking if there is an error_workflow_file, start_snakemake or error_workflow_file.
        If there is one of this three file, the function check the next directory.
        If there is not one of this three file, it executes the function check_job_status()

        Parameter :
        ------------------------------

        Return :
        ------------------------------
    """

    # loop to check every directory in the folder job
    try:
        list_dir = os.listdir( JOBS_DIR )
    except NotADirectoryError as e:
        raise NotADirectoryError( JOBS_NOT_A_DIR ) from e

    for run_dir in list_dir:
        try:
            if os.path.isdir( os.path.join( JOBS_DIR, run_dir ) ):

                # Take the name of the current directory checked
                run_name = os.path.basename( run_dir )
                if run_name == "common_files" or run_name == "tools" or run_name == "mimicINT_InterPro":
                    continue

                # path to get the file wanted
                status_snakemake = os.path.join( JOBS_DIR, os.path.join( run_dir, START_SNAKEMAKE_FILE ) )
                status_end_workflow = os.path.join( JOBS_DIR, os.path.join( run_dir, END_WORKFLOW_FILE ) )
                status_error_workflow = os.path.join( JOBS_DIR, os.path.join( run_dir, ERROR_WORKFLOW_FILE) )
                rule_index_file = os.path.join( JOBS_DIR, os.path.join ( run_dir, 'rule_index' ) )

                if os.path.exists( status_end_workflow ) :
                    if get_rule_index( run_name ) != str( size_of_table() ):
                        create_file( str( size_of_table() ), rule_index_file )
                    continue

                if os.path.exists( status_snakemake ) or os.path.exists( status_error_workflow ):
        
                    continue

                else:
                    check_job_status( run_name )

        except Exception as e:
            if e.args[0] == JOBS_NOT_A_DIR:
                log_write( logging.ERROR )
                logger.error( e )
                raise

            if e.args[0] == SQUEUE_FILE_NOT_FOUND:
                create_file( '', SQUEUE_FILE )

                if os.path.exists( SQUEUE_FILE ):
                    log_write( logging.DEBUG )
                    logger.debug( "Creation du fichier slurm_squeue.txt" )
                    pass

                else:
                    log_write( logging.ERROR )
                    logger.error( e )
                    raise

            if e.args[0] == psycopg2.Error:
                log_write( logging.ERROR )
                logger.error( e )
                raise

            if e.args[0] == CREATE_FILE_NOT_PERMISSION:
                log_write( logging.ERROR )
                logger.error( str( e ) + run_name )
                pass

            if e.args[0] == JOBS_STATUS_DIR_NOT_FOUND:
                log_write( logging.CRITICAL )
                logger.critical( str( e ) + " (" + run_name + ")" )
                pass

            if e.args[0] == subprocess.SubprocessError:
                log_write( logging.ERROR )
                logger.error( e )
                raise

            if e.args[0] == START_RULE_ID_FILE_NOT_FOUND:
                log_write( logging.ERROR )
                logger.error( e )
                pass


check_run_status()
