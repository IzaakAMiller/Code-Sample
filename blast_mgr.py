import os
from ..models import BlastJob
from ..settings import BASE_DIR
from django_q.tasks import async_task, result, fetch
from ..tasks import run_Blast


class BlastMgr:
    """Helper class for running blast on docker"""

    query_set = BlastJob.objects.all()

    """
    Start async search task and return blast results
    """

    def run_blast(self, sequence):
        current_directory = os.getcwd()
        query_file = 'genome/fasta_query.fasta'
        self.create_query_fasta(query_file, sequence)

        blast_command = '''docker run --rm \
        --volume {0}/genome:/blast/genome:rw \
        ncbi/blast \
        blastn -subject genome/ecoli_k12_mg1655.fasta -query genome\{1} -outfmt "6 nident sstart send sstrand evalue pident"'''.format(
            current_directory, query_file)

        task_id = async_task(run_Blast, blast_command)

        task = result(task_id, -1)
        results = task.stdout.decode("utf-8").strip("\n")
        results_dict = self.process_results(results)
        results_dict['sequence'] = self.extract_sequence(results_dict['sstart'], results_dict['send'],
                                                    results_dict['sstrand'])

        return results_dict

    """
    Processes blast results into a dictionary to populate BlastResult model
    """

    def process_results(self, results):
        results = results.split("\t")
        if results == ['']:
            results = [0] * 6
        results_dict = {"result_no": results[0], "sstart": int(results[1]), "send": int(results[2]),
                        "sstrand": results[3], "evalue": results[4], "pident": results[5]}
        return results_dict

    """
    Extracts found sequence from blast result
    """

    def extract_sequence(self, start: int, end: int, strand: str):
        #add ability to select the file to run in front end
        with open("genome/ecoli_k12_mg1655.fasta", "r") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                sequence = record.seq[start - 1: end]
        if strand == 'minus':
            sequence = sequence.reverse_complement()
        return str(sequence)

    """
    Create fasta query file called 'fasta_query.fasta'
    """

    def create_query_fasta(self, file_path: str, sequence: str):
        with open(file_path, 'w') as out_fasta:
            out_fasta.write('>Query\n')
            for i in range(0, len(sequence), 80):
                out_fasta.write(f'{sequence[i: i + 80]}\n')

    """
    Start async search task and return blast results
    """
