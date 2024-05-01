# Nurikabe
Semester long project for CompSci 683. Our group is focusing on Nurikabe as a CSP.

Important files:
 - backtracking.py: Our implementation of the backtracking algorithm for the Nurikabe solver.
 - checkAnswer.py: Checks all the constraints for a valid Nurikabe solution.
 - inference.py: Inferences that can be made on a Nurikabe board state to guarantee some tiles.
 - tests.py: Runs the tests that creates the graphs for our report. Warning; some take a while to run. See below note.

Once you download the code
1. open your terminal:
2. move to the Solvers directory
   - cd 683-Nurikabe
   - cd Code
   - cd Solvers
3. run: python backtracking.py

You will then be prompted with a board size to input and whether you want to perform pre-inferencing or not.

Some commands you can run directly are:
- python backtracking.py 1 noInference (this runs a 5x5 board without inference)
- python backtracking.py 1 yesInference (this runs a 5x5 board with inference)
- python backtracking.py 3 yesInference (this runs an 8x8 board with inference, takes around 40 seconds)
- python backtracking.py 5 noInference (this runs a 12x12 board with no inference)

Testing note, all but one of the graphs take quite a while to run. To run the graph that doesn't take a while, within the main of tests.py make sure 'data = read_in_test_database()' and 'graphs_2(data)' are uncommented and 'graphs_1' and 'graphs_3' are commented. Once this is the case run the file and it'll create the graphs.
- These graphs take a while to run because they are actually solving the boards
- The graphs that they make are the same as the graphs within the final report
