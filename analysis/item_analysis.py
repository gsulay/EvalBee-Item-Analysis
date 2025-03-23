import numpy as np
import pandas as pd
from pathlib import Path
import re
from pprint import pprint
import pingouin as pg
import scipy.stats as stats
import argparse
from sklearn.metrics import jaccard_score

class ItemAnalysis:
    def __init__(self, path, output_path):
        self.path = path
        self.output_path = output_path

        self.options_pattern = r'Q{1}\s[0-9]+\sOptions'
        self.key_pattern = r'Q{1}\s[0-9]+\sKey'
        self.marks_pattern = r'Q{1}\s[0-9]+\sMarks'

        self.df = pd.read_excel(Path(self.path))
        self.run_calculation(self.df)
        self.correlation_calculation(self.df)


    def item_analysis(self, base_df):

        all_topics = []


        for idx, col in enumerate(base_df.columns[10:]):
            idx = idx +10
            if re.match(self.options_pattern, col):
                topic_df['options'].append(idx)

            elif re.match(self.key_pattern, col):
                topic_df['keys'].append(idx)
            elif re.match(self.marks_pattern, col):
                topic_df['marks'].append(idx)
            else:
                try:
                    all_topics.append(topic_df)
                except NameError:
                    pass
                
                topic_df = {'topic': idx,
                            'keys':[],
                            'options': [],
                            'marks': [],
                            }
        all_topics.append(topic_df) #appends the latest topic

        all_topics_df = []
        #Create the df of each topic
        for topic_df in all_topics:
            if len(topic_df['marks']) == 0: #When having multiple topics, evalbee adds another column thus creating a new "false topic". This skips the false topic.
                continue
            base_cols = base_df.columns
            topic_lst = [base_df.columns[topic_df['topic']]]*len(topic_df['keys'])
            item_no = [f"Item No. {base_cols[i].split()[1]}" for i in topic_df['keys']]
            
            #Topic Reliability
            reliability_score = pg.cronbach_alpha(base_df.iloc[:, topic_df['marks']])[0]
            reliability = [reliability_score]*len(topic_df['keys'])

            #Per Item Analysis
            difficulty = []
            correct_answer = []
            count_of_a = []
            count_of_b = []
            count_of_c = []
            count_of_d = []
            count_of_e = []
            discrimination = []

            #Score of each student
            total_possible_score = len(topic_df['keys'])
            score = base_df.iloc[:,topic_df['marks']].sum(axis=1)/total_possible_score*100

            #Per Item Analysis
            for key, option, mark in zip(topic_df['keys'], topic_df['options'], topic_df['marks']):
                #Dataframe for the options, keys, and marks of each student
                option_series = base_df.iloc[:,option]
                key_series = base_df.iloc[:,key]
                mark_series = base_df.iloc[:, mark]

                #Difficulty(Percentage of incorrect to correct answers) and Correct Answer
                difficulty.append(mark_series.sum()/mark_series.count())
                correct_answer.append(key_series.iloc[0]) 

                #Count of each option
                count_of_a.append(option_series.loc[option_series == ('A')].count())
                count_of_b.append(option_series.loc[option_series == ('B')].count())
                count_of_c.append(option_series.loc[option_series == ('C')].count())
                count_of_d.append(option_series.loc[option_series == ('D')].count())
                count_of_e.append(option_series.loc[option_series == ('E')].count())

                #Calculate the Discrimination
                pbr = stats.pointbiserialr(mark_series, score)[0]
                if np.isnan(pbr):
                    if difficulty[-1] == 0:
                        discrimination.append('All Wrong')
                    else:
                        discrimination.append('All Correct')
                else:
                    discrimination.append(pbr)
            
            df = pd.DataFrame({'Topic':topic_lst,
                            'Topic Reliability':reliability,
                            'Item Number': item_no,
                            'Difficulty':difficulty,
                            'Correct Answer':correct_answer,
                            'A': count_of_a,
                            'B':count_of_b,
                            'C':count_of_c,
                            'D':count_of_d,
                            'E':count_of_e,
                            'Discrimination':discrimination})
            all_topics_df.append(df)

        final_df = pd.concat(all_topics_df)
        return final_df

    def run_calculation(self, df):
        all_sets = [(_,self.item_analysis(i)) for _,i in df.groupby('Exam Set')]

        #Topic Analysis
        set_dct = {'Set No':[],
                'Reliability':[]}
        for set_no, i_df in all_sets:
            set_dct['Set No'].append(set_no)
            set_dct['Reliability'].append(i_df.iloc[:,1].mean())

        self.all_sets = all_sets
        self.set_df = pd.DataFrame(set_dct)
        
    
    def export(self):
        with pd.ExcelWriter(self.output_path) as writer:
            self.df.to_excel(writer, sheet_name='Raw Score')
            for set_no, df in self.all_sets:
                df.to_excel(writer, sheet_name=f"Set {set_no} Analysis")
            for set_no, df in self.correlation_matrix:
                df.to_excel(writer, sheet_name=f"Set {set_no} Correlation Matrix")
            self.set_df.to_excel(writer, sheet_name="Set Statistics")

    def correlation_calculation(self, df):
        #Seggregate into Sets
        sets = [i for _,i in df.groupby('Exam Set')]
        marks_pattern = r'Q{1}\s[0-9]+\sMarks'
        marks_index = []

        self.correlation_matrix = []
        def corr_calc(df, name_override=None):   #Calculates the correlation given df
            #Isolate Only Marks
            for idx, col in enumerate(df.columns[10:]):
                idx = idx +10
                if re.match(self.marks_pattern, col):
                    marks_index.append(idx)

            new_df = df.iloc[:,[2,3]+marks_index]

            #Create Name and ID as the index
            new_df['Name and ID'] = new_df.apply(lambda x: f"{x['Name']} | {x['Roll No']}", axis=1)
            new_df = new_df.drop(columns=['Name', 'Roll No'])
            new_df = new_df.set_index('Name and ID')   #Sets the index to the Name

            #Use Jaccard Score for similarity (Pairwise Comparison)
            length = new_df.shape[0]

            all_scores = []
            for row in range(length):
                cols = []
                for col in range(length):
                    cleaned_y1 = new_df.iloc[row, :]
                    cleaned_y2 = new_df.iloc[col, :]

                    cols.append(jaccard_score(cleaned_y1,cleaned_y2))
                all_scores.append(cols)

            pairwise_jaccard = pd.DataFrame(all_scores, index=new_df.index, columns=new_df.index)

            if name_override == None:
                self.correlation_matrix.append([df.iloc[0,1], pairwise_jaccard])    #appends Set No and Correlation Matrix
            else:
                self.correlation_matrix.append([name_override, pairwise_jaccard])
        
        for set in sets:
            corr_calc(set)  #For Each Set
        
        corr_calc(df, "All Sets")   #Correlation for All

if __name__ == '__main__':
    # Create an argument parser if used via terminal
    parser = argparse.ArgumentParser(
        prog='EvalBee Item Analysis',
        description='Item Analysis Program from EvalBee export',
        epilog='Made by Gifrey Sulay'
    )
    
    # Positional argument for the filename
    parser.add_argument('filename', help='Path to the Excel file from EvalBee')
    
    # Optional argument for the export path
    parser.add_argument('output', help='Export path for the results', default=None)
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Create an instance of the ItemAnalysis class
    item_analysis = ItemAnalysis(args.filename, args.output)
    item_analysis.run_calculation(item_analysis.df)
    item_analysis.export()

