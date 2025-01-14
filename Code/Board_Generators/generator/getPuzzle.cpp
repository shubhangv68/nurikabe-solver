// Modified from Malorn44's NurikabeMaker (MainWindow.cpp)
#include "generator.h"
#include <vector>
#include <iostream>
#include <string>
#include <fstream>

// generates a puzzle using Generator
vector<vector<int> > getPuzzle(int row, int col)
{
    // generates a random number seed for use by Generator
    srand(time(NULL));

    Generator g(row, col);
    g.generate();       // generates the puzzle
    g.fillInNumbers();  // fills in sizes of rooms
    g.removeValue(-1);  // removes walls (solution)
    return g.getGrid();
}

// makes puzzle into one string, each row of numbers separated by a space, with specified rows and cols
std::string getPuzzleString(int rows, int cols) {
    std::vector<std::vector<int> > puzzle = getPuzzle(rows, cols);
    std::string result;
    for (const auto& row : puzzle) {
        for (int num : row) {
            result += std::to_string(num);
            result += ",";
        }
        result += " ";
    }
    return result;
}

// int main() {
//     // below just for testing
//     std::ofstream outputFile("puzzle_15x15.txt"); // output file
//     outputFile << getPuzzleString(15, 15);
//     outputFile.close();
//     return 0;
// }

int main(int argc, char *argv[]) {
    // example command to make it run: ./puzzle_generator 15 15
    // Check if the correct number of command-line arguments are provided
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <rows> <cols>" << std::endl;
        return 1; // Exit with an error code
    }

    // Parse command-line arguments into integers
    int rows = std::stoi(argv[1]);
    int cols = std::stoi(argv[2]);

    // // Generate and output the puzzle to a file
    // std::ofstream outputFile("puzzle_" + std::to_string(rows) + "x" + std::to_string(cols) + ".txt");
    // if (!outputFile.is_open()) {
    //     std::cerr << "Error: Unable to open output file." << std::endl;
    //     return 1; // Exit with an error code
    // }
    // outputFile << getPuzzleString(rows, cols);
    // outputFile.close();

    // Output the puzzle directly to std::cout
    std::cout << getPuzzleString(rows, cols);

    return 0;
}