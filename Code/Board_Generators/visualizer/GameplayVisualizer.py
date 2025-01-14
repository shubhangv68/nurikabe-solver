import json
import tkinter as tk
import random

# Load JSON file with the boards
with open("../board_database.json") as f:
    data_set = json.load(f)

cell_size = 60  # Cell's dimension in the board
global root_board
global current_board


# Toggle a tile's color and the corresponding value in the board data array
def toggle_color(event):
    current_color = event.widget.itemcget(tk.CURRENT, "fill")
    new_color = "black" if current_color == "white" else "white"
    event.widget.itemconfig(tk.CURRENT, fill=new_color)
    col = int(event.widget.coords(tk.CURRENT)[0] // cell_size)
    row = int(event.widget.coords(tk.CURRENT)[1] // cell_size)

    # Toggle the value in the array
    if current_board[row][col] == 0:
        current_board[row][col] = -1
    else:
        current_board[row][col] = 0


# Draws the board given a specific size and list of locations of numbers
def draw_board(canvas, arr=None):
    if arr is None:
        arr = []

    canvas.delete("all")  # Clear canvas before drawing

    for i in range(len(arr)):
        for j in range(len(arr[0])):
            x0 = j * cell_size
            y0 = i * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            tile = canvas.create_rectangle(x0, y0, x1, y1, fill="white", outline="black", width=2)
            if arr[i][j] != 0 and arr[i][j] != -1:
                canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=str(arr[i][j]), fill="black",
                                   font=("Helvetica", 20))
            else:
                canvas.tag_bind(tile, "<Button-1>", toggle_color)


# Creates popout window to show the board
def create_board_window(canvas_height, canvas_width, board_data):
    global root_board
    root_board = tk.Toplevel()
    root_board.title("Nurikabe Puzzle")

    canvas = tk.Canvas(root_board, width=canvas_width * cell_size, height=canvas_height * cell_size)
    canvas.pack()

    draw_board(canvas, board_data)


# Function to handle button click and generate board
def generate_board():
    global current_board
    if 'root_board' in globals():
        root_board.destroy()
    req_key = size_entry.get()
    if req_key in data_set:  # Check if the input key is valid
        board_key = random.choice(list(data_set[req_key].keys()))
        current_board = data_set[req_key][board_key]["board"]
        create_board_window(len(current_board), len(current_board[0]), current_board)
        invalid_input_label.config(text="")  # Clear any previous error message
    else:
        invalid_input_label.config(text="Invalid input. Please try again.")  # Show error message


# Create main window
root = tk.Tk()
root.title("Nurikabe Board Generator")

root.geometry("+100+100")  # Offset the window position for padding
root.configure(padx=20, pady=20)

# Label and Entry for board size input
size_label = tk.Label(root, text="Enter board size (e.g., '5x5'): ")
size_label.pack(anchor=tk.CENTER)

size_entry = tk.Entry(root, width=20)
size_entry.pack(padx=5, pady=5)

# Label to show error message
invalid_input_label = tk.Label(root, text="", fg="red")
invalid_input_label.pack(anchor=tk.CENTER)

# Button to generate board
generate_button = tk.Button(root, text="Generate Board", command=generate_board)
generate_button.pack()

root.mainloop()
