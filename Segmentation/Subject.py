'''
Subject Class
  - reads a .csv file from a given direcotry
  - Holds a set of elements of type Subject
  - can return details recarding a specific subject if it exists
'''

import numpy as np
import pandas as pd
import Logger

# A list of all the Subjects
class Subject_List(object):

    def __init__(self,file_dir):
        self.initialize_varaibles(file_dir)
        self.initialize_subject_list(self.csv_file.values)

    def initialize_varaibles(self,file_dir):
        self.csv_file = pd.read_csv(open(file_dir,'r'), encoding='utf-8', engine='c')#,header=4)
        self.subject_set = set()

    '''
    Make/Populate the set of subjects:
        - members of the set are unique
    '''
    def initialize_subject_list(self, csv_file):
        for line in csv_file:
            temp_subject = Subject(name=line[0],code=line[1],
                                   year=line[2],organizer=line[3])
            self.subject_set.add(temp_subject)

    def __repr__(self):
        Subject_List_print = 40*'-'+'\n'
        for subject in self.subject_set:
            Subject_List_print += str(subject)+'\n'
        return Subject_List_print

    '''
    Function returns a Subject information if subject exists
    '''
    def get_subject(self,name,code,year,organizer):
        temp_subject = Subject(name=name,code=code,year=year,
                                            organizer=organizer)
        if temp_subject in self.subject_set:
            return temp_subject.get_details
        else:
            return 'NO SUCH SUBJECT RECORDED'

    def get_subject_via_code(self, code):
        for subject in self.subject_set:
            if (subject.code == code):
                return subject
        raise Exception('Subject {} has not been added to subject list!'.format(code))

'''
Subject calss
    - holds: name, code, year, organizer
    - has key,eq,hash for holding in a set
    - print(Subject) --> for details
'''
class Subject(object):

    def __init__(self,name,code,year,organizer):
        self.initialize_varaibles(name,code,year,organizer)

    def initialize_varaibles(self,name,code,year,organizer):
        self.name      = name
        self.code      = code
        self.year      = year
        self.organizer = organizer

    def __repr__(self):
        Subject_details = 'name: {}\ncode: {}\nyear: {}\norganizer: {}'\
            .format(self.name,self.code,self.year,self.organizer)\
            +'\n'+40*'-'
        return(Subject_details)

    def __str__(self):
        Subject_details = 'name: {}\ncode: {}\nyear: {}\norganizer: {}'\
            .format(self.name,self.code,self.year,self.organizer)\
            +'\n'+40*'-'
        return(Subject_details)

    def __key(self):
        return (self.name,self.code,self.year,self.organizer)

    def __hash__(self):
        return hash(self.__key())

    def set_date_time(date_time):
        self.date_time = date_time

    '''
    Returns a lsit of main attributes
    '''
    def get_details(self):
        return [self.name,self.code,self.year,self.organizer]

    def __eq__(self,other):
        if isinstance(other,type(self)):
            return self.__key()==other.__key()
        return NotImplemented

import os
import sys

def main():
    my_dir = os.path.join(os.getcwd(),*['file_dir','subject.csv'])
    my_Subject_List = Subject_List(my_dir)
    print('='*40)
    sbj_name      = 'Computer Design'
    sbj_code      = 'CDN000003'
    sbj_year      = 2018
    sbj_organizer = 'Nigel Topham'
    subject_interest = my_Subject_List.get_subject(sbj_name,sbj_code,sbj_year,sbj_organizer)
    print('All Subjects:\n{}'.format(my_Subject_List))
    print('Looking for a course:\n{}'.format(subject_interest))

if __name__=="__main__":
    main()
