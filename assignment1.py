import mysql.connector
import os
import csv
from io import StringIO

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
            #query = "SELECT DISTINCT {} from refGene where name2 = '{}'".format(",".join(query_fields), self.gene)
            query = "SELECT DISTINCT %s from refGene where name2 = '%s'"% ((",".join(query_fields)), (self.gene))

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
                print("There are more than one entry for your gene. The first entry in file will be chosen")

    def get_gene_symbol(self):
        print("Your chosen Genesymbol is: %s" % self.gene)

    def get_coordinates_of_gene(self):
        ## Use UCSC file
        with open(self.file_name, "r") as f:
            first = f.readline().replace("(", "").replace(")", "")
            data= first.split(" ")

        self.start = data[3].replace(",", "")
        self.stop = data[4].replace(",", "")
        length_gene= int(self.stop) - int(self.start)

        print("The coordinates of your gene are: %s (start) and %s (stop)."
              "The length of your gene is: %s bp." % (self.start, self.stop, length_gene))

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
        print("todo")
        
    def get_number_of_exons(self):
        print("ads")
    
    
    def print_summary(self):
        print("Print all results here:")
        self.get_gene_symbol()
        self.download_gene_coordinates()
        self.get_coordinates_of_gene()


    
    
def main():
    print("Assignment 1")
    assignment1 = Assignment1("KCNE1", "hg38", "ucsc_file")
    assignment1.print_summary()
    
    
    print("Done with assignment 1")
    
        
if __name__ == '__main__':
    main()

