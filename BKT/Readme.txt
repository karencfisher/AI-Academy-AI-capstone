Baysian Knowledge Tracing task

Files:

BKTData_clean_csv: version of the original dataset with all steps w/o KC associations
                   removed.

BKT.py: the solution

Run simply, printing just final values for all students:

>>python BKT.py

With verbose mode (printing interim p(L) values for each step for each student)

>>python BKT.py verbose

One can also process a selected student in verbose mode in the Python CLI, Jupyter 
Notebook, etc. This will also allow specifying different initial parameters.

>>> from BKT import BKT
>>> initial_params = {'initial_prob_l': 0.2,
...                   'prob_g': 0.25,
...                   'prob_s': 0.1,
...                   'prob_t': 0.1}
# First parameter is verbose mode, True or False
>>> bkt = BKT(True, **initial_params)
>>> bkt.load_csv('BKTData.csv')
# Omitting list of students will process all the students in the data set
>>> results = bkt.process_students(['stu2'])

Processing student stu2...
Step 477: KC1=0.2 KC2=0.5263157894736843 KC3=0.2 KC4=0.2 KC5=0.2
Step 484: KC1=0.2 KC2=0.8200000000000001 KC3=0.2 KC4=0.2 KC5=0.2
Step 485: KC1=0.2 KC2=0.9482758620689655 KC3=0.2 KC4=0.2 KC5=0.2
Step 497: KC1=0.2 KC2=0.9482758620689655 KC3=0.2 KC4=0.2 KC5=0.5263157894736843
Step 585: KC1=0.2 KC2=0.9482758620689655 KC3=0.2 KC4=0.2 KC5=0.8200000000000001
Step 592: KC1=0.2 KC2=0.9482758620689655 KC3=0.2 KC4=0.2 KC5=0.9482758620689655
Step 599: KC1=0.2 KC2=0.9482758620689655 KC3=0.2 KC4=0.2 KC5=0.9865671641791044
Step 626: KC1=0.2 KC2=0.9482758620689655 KC3=0.5263157894736843 KC4=0.2 KC5=0.9865671641791044
Step 630: KC1=0.2 KC2=0.9482758620689655 KC3=0.8200000000000001 KC4=0.2 KC5=0.9865671641791044
...

You can then print the results for summary of final values

>>> print(results)
          KC_1  KC_2  KC_3  KC_4  KC_5      Mean
stu2  0.999918   1.0   1.0   1.0   1.0  0.999984
