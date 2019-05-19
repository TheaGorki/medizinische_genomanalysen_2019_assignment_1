#!/usr/bin/env python
import mysql.connector
import os
import pysam


__author__ = 'Anna-Dorothea Gorki'

##
## Concept:
## TODO
##


class Assignment1:
    
    def __init__(self, gene, genome_reference, file, bamfile):
        self.gene = gene
        self.genome_reference = genome_reference
        self.file_name = file
        self.bamfile =bamfile

    
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
        #Prints gene symbol
        print("Your chosen Genesymbol is: %s" % self.gene)

    def get_coordinates_of_gene(self):
        ## Use UCSC file to get chromosome location and start and stop position of gene of interest
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
        #Uses pysam tool to create AlignmentFile from bam file, complete header with header=self.samfile.header
        self.samfile = pysam.AlignmentFile(self.bamfile, "rb")
        header= self.samfile.header['HD']

        print(header)

    def get_properly_paired_reads_of_gene(self):
        #is_proper_pair is AlignedSemgent attribute
        self.reads= list(self.samfile.fetch(self.chromosome, int(self.start), int(self.stop)))
        paired_reads=[i for i in self.reads if i.is_proper_pair]

        print("Number of properly paired reads: %s" % (len(paired_reads)))
        
    def get_gene_reads_with_indels(self):
        #Cigar (Compact Idiosyncratic Gapped Alignment Report), cigartuples is AlignedSegment attribute-->operation1=insertion, operation2=deletion
        list_indel = []
        for i in self.reads:
            if not i.is_unmapped:
                indels = i.cigartuples
                for (operation,length) in indels:
                    if (operation == 1) or (operation == 2):
                        list_indel.append(i)

        print("Number of reads with indels: %s" % (len(list_indel)))
        
    def calculate_total_average_coverage(self):
        #calculation of average coverage in all bam file, Chromosome length from header
        sum_coverage = 0
        total_length = 0
        for pileupcolumn in self.samfile.pileup():
            sum_coverage = sum_coverage + pileupcolumn.n
            total_length = total_length + 1
        average = sum_coverage / total_length

        print("Total average coverage is: %s" % average)
        
    def calculate_gene_average_coverage(self):
        #calculating average coverage of gene of interest in bam file
        gene_length = int(self.stop) - int(self.start)
        gene_coverage=0
        for pileupcolumn in self.samfile.pileup(self.chromosome, int(self.start), int(self.stop)):
            gene_coverage = gene_coverage + pileupcolumn.n
        gene_average = gene_coverage / gene_length

        print("Gene average coverage is: %s" % gene_average)

        
    def get_number_mapped_reads(self):
        #get mapped reads by excluding unmapped reads (AlignmentSegment attribute)
        reads_mapped= 0
        for i in self.reads:
            if not i.is_unmapped:
                reads_mapped= reads_mapped +1
        print("Number of mapped reads is: %s" % reads_mapped)

    def get_region_of_gene(self):
        #uses exon positions to get regions of gene
        exon_region_start = self.data[7].replace(",", " ").split()
        exon_region_start = [x.strip('\'') for x in exon_region_start]
        exon_region_stop = self.data[8].replace(",", " ").split()
        exon_region_stop = [x.strip('\'') for x in exon_region_stop]

        for i in range(1,len(exon_region_start)):
                print("The region %s goes from %s to %s" % (i, exon_region_stop[i-1], exon_region_start[i-1]))
        
    def get_number_of_exons(self):
        #output: number of exons in gene of interest
        exon_count = self.data[6].replace(",","")
        print("The gene has %s exons" % exon_count)

    def print_summary(self):
        print("Print all results here:")
        self.get_gene_symbol()
        self.download_gene_coordinates()
        self.get_coordinates_of_gene()
        self.get_number_of_exons()
        self.get_region_of_gene()
        self.get_sam_header()
        self.get_properly_paired_reads_of_gene()
        self.get_number_mapped_reads()
        self.get_gene_reads_with_indels()
        self.calculate_total_average_coverage()
        self.calculate_gene_average_coverage()

    
def main():
    print("Assignment 1")
    assignment1 = Assignment1("PCNT", "hg38", "ucsc_file", "http://hmd.ait.ac.at/medgen2019/chr21.bam")
    assignment1.print_summary()
    
    
    print("Done with assignment 1")
    
        
if __name__ == '__main__':
    main()

