# Data loading
import csv
# CLI argument handling
import sys
# Output final results as table
import pandas as pd


class BKTModel:
    def __init__(self, data, **params):
        '''
        Constructor

        Cache the initial parameters and student data. Also allocate
        the results vector. 

        Parameters are:

        P(L0) is the initial probability that the student knows a particular skill.
        P(G) is probability of guessing correctly, if the student doesn't know the skill.
        P(S) is probability of making a slip, if student does know the skill.
        P(T) is probability of learning the skill if the student does not know the skill.

        Results vector is an array of values, each the current P(Li) for each step and
        corresponding KC_n. They are initialized all with the value of P(L_0).
        '''
        self.initial_prob_l = params['initial_prob_l']
        self.prob_g = params['prob_g']
        self.prob_s = params['prob_s']
        self.prob_t = params['prob_t']
        self.data = data
        self.result_vector = [self.initial_prob_l] * 5

    def process_student(self, verbose=False):
        '''
        Process the rows for the student.

        For each row we determins which KC column is associated with the step. We then
        update the value stored in that element of the result_vector, based on the previous
        P(L_i-1). 
        '''
        for row in self.data:
            # Get index of associated KCn. If row all zeros, skip that row.
            kc_index = [i for i in range(2, len(row)) if row[i] == 1]
            if len(kc_index) == 0:
                continue
            kc_index = kc_index[0]

            # get previous P(Li-1)
            previous_p_l = self.result_vector[kc_index - 2]

            # Calculate P(Li) for current step
            self.result_vector[kc_index - 2] = self.__calc_update(row, previous_p_l)

            if verbose:
                print(f'Step {row[0]}: ', end='')
                for i in range(5):
                    print(f'KC{i+1}={self.result_vector[i]}', end= ' ')
                print('')
        return self.result_vector

    def __calc_update(self, row, previous_p_l):
        '''
        Perform the actual calculations, following the equations found in 
        van de Sande, B. (2013). "Properties of the Bayesian Knowledge Tracing Model." 
        Journal of Educational Data Mining, 5(2), 1–10

        https://doi.org/10.5281/zenodo.3554629

        The input is the individual row of data, and the previous P(Li-1) fpr the spcific
        KCn.
        '''
        question = row[1]

        # The differences in the equation depending on if answer is correct or not
        if question:
            s = 1 - self.prob_s
            g = self.prob_g
        else:
            s = self.prob_s
            g = 1 - self.prob_g

        enumerator = previous_p_l * s
        denominator = previous_p_l * s + (1 - previous_p_l) * g
        assert denominator != 0, 'needs smoothing!'
        prob_l_1 = enumerator / denominator
        prob_l = prob_l_1 + (1 - prob_l_1) * self.prob_t
        return prob_l
    

class BKT:
    def __init__(self, verbose, **params):
        '''
        Constructor
        '''
        self.verbose=verbose
        self.initial_params = params
        self.data = []
        self.students = []
        self.results_matrix = []
        pass

    def load_csv(self, file_path):
        '''
        Load the data file as CSV

        input: file_path, the file path for the data
        '''
        with open(file_path, 'r') as FP:
            # read first line to skip headers
            FP.readline()

            # read rest of file and store in 2-d array
            reader = csv.reader(FP, delimiter=',')
            for row in reader:
                # convert all but student id column to integers
                row = [row[0]] + [int(row[i]) for i in range(1, len(row))]
                self.data.append(row)
        
        # Get number of rows
        self.n_data = len(self.data)

        # list of unique students
        for row in self.data:
            if row[0] not in self.students:
                self.students.append(row[0])

    def get_student_data(self, student_ID):
        '''
        Filter the data for rows for a given student by their ID

        Input: the student_ID, an int
        returns: the data for that student
        '''
        data = [self.data[i][1:] for i in range(self.n_data) if 
                         self.data[i][0] == student_ID]
        return data

    def process_students(self, students=None):
        '''
        Process each student. Instantiating a BKTModel object, load the data
        and perform the calculations. The results are the final P(L) for
        each KCn in an array. The results are compiled into a pandas dataframe 
        as the final output
        '''
        if students is None:
            students = self.students

        for student in students:
            if self.verbose:
                print(f'\nProcessing student {student}...')

            # get the rows for one student
            data = self.get_student_data(student)

            # instantiate the BKTModel class for that student
            bkt = BKTModel(data, **self.initial_params)

            # Obtain results and add to final result matrix
            result = bkt.process_student(self.verbose)
            self.results_matrix.append(result)

        # compile results into a pandas dataframe for formatted table
        results = pd.DataFrame(self.results_matrix, 
                               index=students,
                               columns=['KC_1', 'KC_2', 'KC_3', 'KC_4', 'KC_5'])
        results['Mean'] = results.mean(axis=1)
        return results


def main():
    verbose = len(sys.argv) > 1 and sys.argv[1] == 'verbose'

    initial_params = {'initial_prob_l': 0.2,
                    'prob_g': 0.25,
                    'prob_s': 0.1,
                    'prob_t': 0.1}

    bkt = BKT(verbose, **initial_params)
    bkt.load_csv('BKTData.csv')
    results = bkt.process_students()
    print(f'\n{results}')

if __name__ == '__main__':
    main()
