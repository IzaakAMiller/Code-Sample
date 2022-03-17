import subprocess

#Used to run blast command in q_cluster task
def run_Blast(blast_command:str):
    task = subprocess.run(blast_command,shell=True,stdout=subprocess.PIPE)
    return task
