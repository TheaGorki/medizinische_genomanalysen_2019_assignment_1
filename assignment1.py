import mysql.connector
import os
import pysam

__author__ = 'Anna-Dorothea Gorki'

##
## Concept:
## TODO
##


class Assignment1:
    
    def __init__(self, gene, genome_reference, file):
        self.gene = gene
        self.genome_reference = genome_reference
        self.file_name = file

    
    def download_gene_coordinates(self):
        ## Uses mySQL to get information about gene of interest

        if os.path.exists(self.file_name) == True:
            print("Your UCSC File already exists")
        else:
            print("Connecting to UCSC to fetch data")

            ## Open connection
            cnx = mysql.connector.connect(host='genome-mysql.cse.ucsc.edu', user='genomep', passwd='password', db=self.genome_reference)

            ## Get cursor
            cursor = cnx.cursor()

            ## Build query fields
            query_fields = ["refGene.name2",
                            "refGene.name",
                            "refGene.chrom",
                            "refGene.txStart",
                            "refGene.txEnd",
                            "refGene.strand",
                            "refGene.exonCount",
                            "refGene.exonStarts",
                            "refGene.exonEnds"]


            ## Build query

            query = "SELECT DISTINCT %s from refGene where name2 = '%s'"% ((",".join(query_fields)), (self.gene))

            # other solution: query = "SELECT DISTINCT {} from refGene where name2 = '{}'".format(",".join(query_fields), self.gene)

            ## Execute query
            cursor.execute(query)

            ## Write to file
            with open(self.file_name, "w") as fh:
                for row in cursor:
                    fh.write(str(row) + "\n")


            ## Close cursor & connection
            cursor.close()
            cnx.close()

            print("Done fetching data")

        with open(self.file_name, "r") as f:
            data= f.read()
            count = data.count(self.gene)
            if count >1:
                print("There are more than one entry for your gene. The first entry in file will be chosen.")

    def get_gene_symbol(self):
        print("Your chosen Genesymbol is: %s" % self.gene)

    def get_coordinates_of_gene(self):
        ## Use UCSC file
        with open(self.file_name, "r") as f:
            first = f.readline().replace("(", "").replace(")", "")
            self.data= first.split(" ")

        self.chromosome = self.data[2].replace(",", "").replace("'", "")
        self.start = self.data[3].replace(",", "")
        self.stop = self.data[4].replace(",", "")
        length_gene= int(self.stop) - int(self.start)

        print("Your gene is located on %s. The coordinates of your gene are: %s (start) and %s (stop)."
              "The length of your gene is: %s bp." % (self.chromosome, self.start, self.stop, length_gene))

    def get_sam_header(self):
        print("todo")
        
    def get_properly_paired_reads_of_gene(self):
        print("todo")
        
    def get_gene_reads_with_indels(self):
        print("todo")
        
    def calculate_total_average_coverage(self):
        print("todo")
        
    def calculate_gene_average_coverage(self):
        print("todo")
        
    def get_number_mapped_reads(self):
        print("todo")

    def get_region_of_gene(self):
        exon_region_start = self.data[7].replace(",", " ").split()
        exon_region_start = [x.strip('\'') for x in exon_region_start]
        exon_region_stop = self.data[8].replace(",", " ").split()
        exon_region_stop = [x.strip('\'') for x in exon_region_stop]

        for i in range(1,len(exon_region_start)):
                print("The region %s goes from %s to %s" % (i, exon_region_stop[i-1], exon_region_start[i-1]))
        
    def get_number_of_exons(self):
        exon_count = self.data[6].replace(",","")
        print("The gene has %s exons" % exon_count)
    
    
    def print_summary(self):
        print("Print all results here:")
        self.get_gene_symbol()
        self.download_gene_coordinates()
        self.get_coordinates_of_gene()
        self.get_number_of_exons()
        self.get_region_of_gene()


    
    
def main():
    print("Assignment 1")
    assignment1 = Assignment1("PCNT", "hg38", "ucsc_file")
    assignment1.print_summary()
    
    
    print("Done with assignment 1")
    
        
if __name__ == '__main__':
    main()

