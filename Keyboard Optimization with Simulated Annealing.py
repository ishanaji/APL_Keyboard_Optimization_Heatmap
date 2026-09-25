import numpy as np  # Necessary Imports
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import copy


# ALL INPUTS NEEDED TO RUN THE PROGRAM ARE GIVEN HERE AT THE START, GIVE INPUTS ACCORDING TO THE COMMENTS TO RUN THE PROGRAM

# USER INPUT START
# PLACE YOUR INPUT TEXT TO OPTIMIZE FOR HERE, IN INPUT_STR:
input_str = """But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was 
born and I will give you a complete account of the system, and expound the actual teachings of the great explorer 
of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because 
it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are 
extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is 
pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. 
To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? 
But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids 
a pain that produces no resultant pleasure? On the other hand, we denounce with righteous indignation and dislike men who are so beguiled
 and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee"""

# PARAMETERS FOR SIMULATED ANNEALING, PLACE IN THESE 3 VARIABLES:
initial_temp = 100.0
cooling_rate = 0.995
num_iterations = 1000

# OLD LAYOUT FORMAT BEFORE ASSIGNMENT 4 UPDATION HAS BEEN USED FOR THIS. IT ONLY WORKS FOR OLDER FORMAT LAYOUT. SO PLEASE GIVE LAYOUT ACCORDINGLY
# THIS LAYOUT IS ONLY USED AS A STARTING LAYOUT TO PLOT THE KEYBOARD KEYS, THE ACTUAL ANNEALING PROCESS STARTS WITH A RANDOMLY GENERATED LAYOUT(WITH SAME COORDINATES)

# THIS PROGRAM ONLY WORKS IF A STARTING LAYOUT WITH SAME COORDINATES AS BELOW IS USED
# AND I HARD CODED FIXED HOME POSITIONS FOR THE FINGERS ACCORDING TO THIS GIVEN COORDINATE LAYOUT. SWAPPING KEY ORDERS IS THE ONLY ALLOWED OPERATION ON THIS BELOW LAYOUT.
# Do not switch special keys with regular keys though, as i have assumed that the special keys are NOT allowed to move during simulated annealing
# (as most standard real life keyboard layouts follow fixed special keys)
starting_layout = {
    "row1": {
        "keys": "`1234567890-=",
        "positions": [
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
            (4, 0),
            (5, 0),
            (6, 0),
            (7, 0),
            (8, 0),
            (9, 0),
            (10, 0),
            (11, 0),
            (12, 0),
        ],
    },
    "row2": {
        "keys": "qwertyuiop[]\\",
        "positions": [
            (0.5, 1),
            (1.5, 1),
            (2.5, 1),
            (3.5, 1),
            (4.5, 1),
            (5.5, 1),
            (6.5, 1),
            (7.5, 1),
            (8.5, 1),
            (9.5, 1),
            (10.5, 1),
            (11.5, 1),
            (12.5, 1),
        ],
    },
    "row3": {
        "keys": "asdfghjkl;'",
        "positions": [
            (0.75, 2),
            (1.75, 2),
            (2.75, 2),
            (3.75, 2),
            (4.75, 2),
            (5.75, 2),
            (6.75, 2),
            (7.75, 2),
            (8.75, 2),
            (9.75, 2),
            (10.75, 2),
        ],
    },
    "row4": {
        "keys": "zxcvbnm,./",
        "positions": [
            (1.25, 3),
            (2.25, 3),
            (3.25, 3),
            (4.25, 3),
            (5.25, 3),
            (6.25, 3),
            (7.25, 3),
            (8.25, 3),
            (9.25, 3),
            (10.25, 3),
        ],
    },
    "special_keys": {
        "Shift_L": (0, 3),
        "Shift_R": (11.25, 3),
        "Space": (3.5, 4),
        "Backspace": (13, 0),
        "Tab": (0, 1),
        "CapsLock": (0, 2),
        "Enter": (12, 2),
    },
}
# USER INPUT END


# keys that are typed using Shift, and their corresponding 'unshifted' keys
# Only Shift_L has been used for shift again(same as assignment 4)
# NOT USER INPUT
shift_keys = {
    "~": "`",
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
    "_": "-",
    "+": "=",
    "{": "[",
    "}": "]",
    "|": "\\",
    ":": ";",
    '"': "'",
    "<": ",",
    ">": ".",
    "?": "/",
}


# same function for calulating finger travel from assignment 4 has been used
# So the same assumptions hold

# A convention has been assumed for calculating finger travel
# Each finger is assumed to stay at its home key initially.
# For pressing a key in its range defined by fingers dictionary,the finger moves to the needed key and then back to its home key
# This total round trip distance is considered for each key press

# Same key being pressed mutiple times consecutively is also considered with the full round trip distance each time
# CAPSLOCK is not used, instead repeated SHIFTS only have been used


def finger_travel(
    count_dict: dict,
) -> dict:
    # count_dict is the dictionary used for counting number of key presses.
    # count_dict has dict(coordinate:frequency) type structure.

    fingers = {
        "L_index": [
            (3.75, 2),
            [
                (3.5, 4),
                (5, 0),
                (6, 0),
                (3.5, 1),
                (4.5, 1),
                (3.75, 2),
                (4.75, 2),
                (4.25, 3),
                (5.25, 3),
            ],
        ],
        "L_middle": [(2.75, 2), [(4, 0), (2.5, 1), (2.75, 2), (3.25, 3)]],
        "L_ring": [
            (1.75, 2),
            [
                (3, 0),
                (1.5, 1),
                (1.75, 2),
                (2.25, 3),
                (0.5, 1),
                (0.75, 2),
                (1.25, 3),
                (1, 0),
                (2, 0),
            ],
        ],
        "L_pinky": [(0, 3), [(0, 3), (0, 2), (0, 1), (0, 0)]],
        "R_index": [
            (6.75, 2),
            [(7, 0), (5.5, 1), (6.5, 1), (5.75, 2), (6.75, 2), (6.25, 3), (7.25, 3)],
        ],
        "R_middle": [(7.75, 2), [(8, 0), (7.5, 1), (7.75, 2), (8.25, 3)]],
        "R_ring": [
            (9.75, 2),
            [
                (9, 0),
                (10, 0),
                (11, 0),
                (12, 0),
                (8.5, 1),
                (9.5, 1),
                (10.5, 1),
                (11.5, 1),
                (8.75, 2),
                (9.75, 2),
                (10.75, 2),
                (9.25, 3),
                (10.25, 3),
            ],
        ],
        "R_pinky": [(11.25, 3), [(11.25, 3), (12, 2), (12.5, 1), (13, 0)]],
    }

    # Default finger position(home key for that finger) is the first element in the coordinates list.
    # example - (3.75,2) is home position for Left index finger (letter F in QWERTY) etc.
    # the second element of the value(nested list) contains all the coordinates that only that finger will be pressing

    # EXACT SAME AS EARLIER FINGER LAYOUT BUT WITH KEYS AND IN THE CONTEXT OF QWERTY LAYOUT FOR REFERENCE
    # fingers = {
    #     'L_index': ['f',['Space','5','6','r','t','f','g','v','b']],
    #     'L_middle': ['d',['4','e','d','c']],
    #     'L_ring': ['s',['3','w','s','x','q','a','z','1','2']],
    #     'L_pinky' : ['Shift_L',['Shift_L','CapsLock','Tab','`']],
    #     'R_index': ['j',['7','y','u','h','j','n','m']],
    #     'R_middle': ['k',['8','i','k',',']],
    #     'R_ring': [';',['9','0','-','=','o','p','[',']','l',';','\'','.','/']],
    #     'R_pinky' : ['Shift_R',['Shift_R','Enter','\\','Backspace']]
    # }

    dist = {
        "L_index": 0,
        "L_middle": 0,
        "L_ring": 0,
        "L_pinky": 0,
        "R_index": 0,
        "R_middle": 0,
        "R_ring": 0,
        "R_pinky": 0,
    }
    # Distance travelled by each finger

    for coord in count_dict:
        for finger in fingers:
            if coord in fingers[finger][1]:
                # if coordinate present in designated keys list for a particular finger,
                dist[finger] += (
                    count_dict[coord] * 2 * cart_dist(fingers[finger][0], coord)
                )
                # round trip distance (2*cart_dist)*frequency has been added
                break
                # move to next coordinate in count_dict
    return dist


# function for calulating (x2-x1)^2 + (y2-y1)^2   (Cartesian distance between 2 points)
def cart_dist(p1: tuple, p2: tuple) -> float:
    return (
        (float(p1[0]) - float(p2[0])) ** 2 + (float(p1[1]) - float(p2[1])) ** 2
    ) ** 0.5


# Function to get coordinate of a key in a given layout (layout1 input)
def key_position(key: str, layout1: dict) -> tuple:
    for row in layout1.values():
        if "keys" in row and key in row["keys"]:
            index = row["keys"].index(key)
            return row["positions"][index]
    return layout1["special_keys"].get(key)


# Generate random keyboard layout based on input starting_layout
# (With same coordinates as starting_layout but only keys(except special keys) are swapped)
def generate_random_layout(layout: dict) -> dict:
    keys = list(
        layout["row1"]["keys"]
        + layout["row2"]["keys"]
        + layout["row3"]["keys"]
        + layout["row4"]["keys"]
    )
    random.shuffle(keys)
    # Random shuffling of keys(except special keys)

    new_layout = {
        "row1": {"keys": "".join(keys[:13]), "positions": layout["row1"]["positions"]},
        "row2": {
            "keys": "".join(keys[13:26]),
            "positions": layout["row2"]["positions"],
        },
        "row3": {
            "keys": "".join(keys[26:37]),
            "positions": layout["row3"]["positions"],
        },
        "row4": {"keys": "".join(keys[37:]), "positions": layout["row4"]["positions"]},
        "special_keys": layout["special_keys"],
    }
    # the indices above are given accordingly to keep same number of keys as there originally were in each row
    return new_layout


# Calculate the total distance of finger travel for the input layout and input_string
# (It uses the finger_travel function from earlier with all the same assumptions)
def calculate_distance(layout2: dict, input_str: str) -> float:
    count = {}
    for letter in input_str:
        if letter.isupper():
            count[key_position("Shift_L", layout2)] = (
                count.get(key_position("Shift_L", layout2), 0) + 1
            )
            letter = letter.lower()
        if letter in shift_keys.keys():
            count[key_position("Shift_L", layout2)] = (
                count.get(key_position("Shift_L", layout2), 0) + 1
            )
            letter = shift_keys[letter]
        if letter == "\n":
            letter = "Enter"
        if letter == " ":
            letter = "Space"
        count[key_position(letter, layout2)] = (
            count.get(key_position(letter, layout2), 0) + 1
        )
        # Shift_L is incremented when uppercase or shift characters are encountered
        # After the conversions to make the letter recognizable in the layout, count[coordinate(letter)] is also incremented

    travel = finger_travel(count)
    total_dist = sum(travel.values())
    return total_dist
    # returns magnitude of total key travel distance


# Generate a neighbour layout by swapping two random keys
def get_neighbour(layout: dict) -> dict:
    keys = list(
        layout["row1"]["keys"]
        + layout["row2"]["keys"]
        + layout["row3"]["keys"]
        + layout["row4"]["keys"]
    )
    i, j = random.sample(range(len(keys)), 2)
    # Picks 2 random key indices
    keys[i], keys[j] = keys[j], keys[i]
    # Swaps the 2 keys

    new_layout = {
        "row1": {"keys": "".join(keys[:13]), "positions": layout["row1"]["positions"]},
        "row2": {
            "keys": "".join(keys[13:26]),
            "positions": layout["row2"]["positions"],
        },
        "row3": {
            "keys": "".join(keys[26:37]),
            "positions": layout["row3"]["positions"],
        },
        "row4": {"keys": "".join(keys[37:]), "positions": layout["row4"]["positions"]},
        "special_keys": layout["special_keys"],
    }
    return new_layout


# Simulated annealing algorithm

# This function almost entirely derives from the travelling salesman example shown in class:
# Main idea is that a new layout is accepted if :
# either it's a shorter distance layout, OR by a random probability that decreases as the number of iterations increases(the exponential term) (to prevent getting stuck in some local maxima)


def simulated_annealing(
    layout: dict,
    input_str: str,
    initial_temp: float,
    cooling_rate: float,
    num_iterations: int,
) -> tuple:
    current_layout = generate_random_layout(layout)
    current_distance = calculate_distance(current_layout, input_str)
    best_layout = copy.deepcopy(current_layout)
    best_distance = current_distance

    temp = initial_temp
    distances = [current_distance]
    best_layouts = [copy.deepcopy(best_layout)]
    best_distances = [best_distance]
    for i in range(num_iterations):
        neighbour_layout = get_neighbour(current_layout)
        neighbour_distance = calculate_distance(neighbour_layout, input_str)

        p = np.exp((current_distance - neighbour_distance) / temp)

        if neighbour_distance < current_distance or random.random() < p:
            # (random.random()) generates random number between 0 and 1. IF neighbour_dist > curr_dist(only case where random condition is evaluated),
            # then p is also a number between 0 and 1 that decreases as temp decreases.
            # temp decreases as number of iterations increases, so overall the random probability of accepting a layout decreases as number of iterations increases.(Hence the name Annealing)
            current_layout = neighbour_layout
            current_distance = neighbour_distance
            # current_layout and current_distance are changed if the layout has shorter key travel than the current layout OR by a random probability condition as stated above
            if current_distance < best_distance:
                best_layout = copy.deepcopy(current_layout)
                best_distance = current_distance
                # best_layout and best_distance are changed only if the layout actually has a shorter key travel than the current best layout

        best_layouts.append(copy.deepcopy(best_layout))
        best_distances.append(best_distance)
        temp *= cooling_rate
        distances.append(current_distance)
    return best_layouts, best_distances, distances


# Animation update function
def update(
    frame: int,
    input_str: str,
    best_layouts: list,
    distances: list,
    route_line: matplotlib.image.AxesImage,
    distance_line: matplotlib.lines.Line2D,
    best_distance_line: matplotlib.lines.Line2D,
    keyboard: dict,
) -> tuple:
    # frame is a number that goes from 0 to num_iterations, as we specify in function body, so we use it as a list index here
    current_layout = best_layouts[frame]
    # best_layouts[frame] only changes when a new best distance layout is obtained, ie. when the green line in graph dips
    # thus heatmap in graph only changes when green line dips
    data = np.zeros((80, 80))
    count = {}
    for letter in input_str:
        if letter.isupper():
            count[key_position("Shift_L", current_layout)] = (
                count.get(key_position("Shift_L", current_layout), 0) + 1
            )
            letter = letter.lower()
        if letter in shift_keys.keys():
            count[key_position("Shift_L", current_layout)] = (
                count.get(key_position("Shift_L", current_layout), 0) + 1
            )
            letter = shift_keys[letter]
        if letter == "\n":
            letter = "Enter"
        if letter == " ":
            letter = "Space"
        count[key_position(letter, current_layout)] = (
            count.get(key_position(letter, current_layout), 0) + 1
        )

    for coord in count:
        y2 = coord[1]
        x2 = coord[0]
        for i in range(4):
            for j in range(4):
                data[int(4 * y2) + i, int(4 * x2) + j] = count[coord]
    # Used to generate 4x4 = 16 squares for each 1x1 unit square in the final graph(for a resoultion of 0.25 as its used in the layout)
    # above code is same code I used in assignment 4 to generate heatmap, it has been reused here.

    for key in current_layout:
        if key != "special_keys":
            for pair in current_layout[key]["positions"]:
                letter = current_layout[key]["keys"][
                    current_layout[key]["positions"].index(pair)
                ]
                keyboard[(pair[0], pair[1])].set_text(letter)
                # used to update the letters in the keyboard in the graph(it changes when a new best_layout is found in the graph, along with the heatmap change)
        else:
            for sp in current_layout[key]:  # Same thing for special keys
                pair = current_layout[key][sp]
                letter = sp
                keyboard[(pair[0], pair[1])].set_text(letter)

    route_line.set_data(data)
    # route_line is updated with data calulated above to generate heatmap in each frame updation
    route_line.set_clim([0, max(count.values())])
    # set_clim sets a color limit for the heatmap (min color assigned to 0 freq. max color assigned to highest freq key.)

    cbar.update_normal(route_line)
    # updates colorbar (only really changes in the first frame(from empty colorbar))

    distance_line.set_data(range(frame + 1), distances[: (frame + 1)])
    # used to plot red line in graph(x coords = range(frame+1), y coords = (distances[:(frame+1)]))

    best_distance_line.set_data(range(frame + 1), best_distances[: frame + 1])
    # used to plot green line in graph

    return route_line, distance_line, best_distance_line, *(keyboard.values())
    # returns all the plotter objects that have to be updated in each frame of animation


# Main body of the program starts from here:


best_layouts, best_distances, distances = simulated_annealing(
    starting_layout, input_str, initial_temp, cooling_rate, num_iterations
)
# best_layouts contains the layouts such that their key travel was less than all the previous iteration layouts' key travel.(used to plot heatmaps in graph)
# because of this, the heatmap only updates when there is a new best distance encountered during simulated annealing, and not updated after every iteration

# best_distances contains key_travels for each of the layouts inside best_layouts(Used to plot green line in graph)
# distances contains total key travel calculated for the current layout in each iteration(Used to plot red line in graph)

# ax1 for heatmap plot
# ax2 for distance vs iteration line plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8))
fig.suptitle("Simulated Annealing for Keyboard Layout Optimization")


ax1.set_xlim(
    -0.5, 15
)  # used to zoom in on keyoard coordinates, hard coded from above layout(since it already relies on same fixed coordinates)
ax1.set_ylim(-0.5, 5)
ax1.set_title(
    """Heatmap of Finger Travel 
              (Keyboard Layout changes only when shorter key travel than current layout encountered)"""
)


keyboard = (
    {}
)  # used to update the letters, when the layout changes in the update function for animation

# below loop used to plot a static keyboard layout(square boxes) which does not get updated in animation(as only keys are swapped)
# it is also used to plot blank letters on each key in the graph, these objects are loaded into the keyboard dict.
# This keyboard dict is used in update function to update letters as layout changes
for key in starting_layout:
    if key != "special_keys":
        for pair in starting_layout[key]["positions"]:
            x = pair[0]
            y = pair[1]
            x1 = np.array(
                [x - 0.5, x + 0.5]
            )  # each key is assumed to have length and width of 1 unit
            y1 = np.array(
                [y - 0.5, y + 0.5]
            )  # This causes some odd overlap with few of the special keys, but those special keys like TAB are not used anyway
            X, Y = np.meshgrid(x1, y1)
            # MESHGRID used to generate 2D grid of points to plot 2 vertical lines for the square
            ax1.plot(X, Y, "w-")
            X, Y = np.meshgrid(y1, x1)
            # MESHGRID used to generate 2D grid of points to plot 2 horizotal lines for the square
            ax1.plot(Y, X, "w-")
            # plotting 4 lines of square individually also works

            keyboard[(x, y)] = ax1.text(x, y, "", color="w", fontsize=9)
            # keyboard dict is loaded with the blank plotter objects which will be updated for the animation
            # key is the coordinate pair and value is the plotter object, this is used for easy updation
    else:
        for sp in starting_layout[key]:  # Same thing for special keys
            pair = starting_layout[key][sp]
            x = pair[0]
            y = pair[1]

            x1 = np.array([x - 0.5, x + 0.5])
            y1 = np.array([y - 0.5, y + 0.5])
            X, Y = np.meshgrid(x1, y1)
            ax1.plot(X, Y, "w-")
            X, Y = np.meshgrid(y1, x1)
            ax1.plot(Y, X, "w-")

            keyboard[(x, y)] = ax1.text(x - 0.5, y, "", color="w", fontsize=9)
            # special keys are plotted with -0.5 x offset as the names are a bit longer, to prevent overlap with other letters


ax1.invert_yaxis()  # done because input layout is given with the top left corner origin assumption
# (so y axis has to be inverted to get top left origin from standard bottom left origin)

route_line = ax1.imshow(
    np.zeros((80, 80)),
    origin="lower",
    interpolation="spline16",
    cmap="magma",
    extent=[-0.5, 19.5, -0.5, 19.5],
)
# Blank plotter object which is updated inside update function to actually produce HEATMAPS for the animation

cbar = plt.colorbar(route_line, ax=ax1)
# colorbar for heatmap, range for it also updated inside update function(as initial route_line object is blank, so we get blank colormap otherwise)


ax2.set_xlim(0, num_iterations)
ax2.set_ylim(min(distances) * 0.9, max(distances) * 1.1)
# zooming into appropriate range for distances plot

ax2.set_title("Best Distance over Iterations")
ax2.set_xlabel("Iteration")
ax2.set_ylabel("Distance")

(distance_line,) = ax2.plot([], [], "r-", label="Key Travel in each iteration")
# blank plotter object used for distance vs iteration line(red line)

(best_distance_line,) = ax2.plot(
    [], [], "g-", label="Shortest Key Travel observed till current iteration"
)
# blank plotter object used for best distance so far vs iteration line(green line)

ax2.legend()
# To show the labels for the lines


# printing final results
print(
    f"The shortest key travel after optimizing the layout is {best_distances[-1]} units"
)
print()
print("Final optimized layout is: ")
print()
print(best_layouts[-1])

anim = FuncAnimation(
    fig,
    update,
    frames=range(0, num_iterations, 1),
    fargs=(
        input_str,
        best_layouts,
        distances,
        route_line,
        distance_line,
        best_distance_line,
        keyboard,
    ),
    interval=10,
    blit=False,
    repeat=False,
)
# blit = False allows for plotting static objects(like my keyboard key squares)

# route_line, distance_line, best_distance_line and keyboard are the variables that contain plotter objects whose updation generates the full animation that we see
# finally generating the animation using update function

plt.tight_layout()  # cleaner layout
plt.show()
# displaying the animation, final stopping frame of animation is the optimized layout
