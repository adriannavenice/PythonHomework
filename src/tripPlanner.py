import json
from app.aiport import Airport
from tps.pyTPS import pyTPS
from graph.weightedGraph import WeightedGraph
from app.aiport import AppendStopTransaction

# Rest of the code...


# Rest of the code...


# WE WANT TO USE THE TRANSACTION PROCESSING SYSTEM
tps = pyTPS()

# WE WANT TO USE THE GRAPH DATA STRUCTURE
airport_graph = WeightedGraph()

# THESE ARE THE STOPS
stops = []

def display_airports():
    # LIST OF AIRPORTS
    print("\n\nAIRPORTS YOU CAN TRAVEL TO AND FROM:\n")
    codes = airport_graph.get_keys()
    text = ""
    for i in range(len(codes)):
        if (i % 10) == 0:
            text += "\t"
        text += codes[i]
        if i < (len(codes) - 1):
            text += ", "
        if (i % 10) == 9:
            text += "\n"
    text += "\n\n"
    print(text)

def display_current_trip():
    # DISPLAY YOUR CURRENT TRIP STOPS:
    text = "Current Trip Stops: \n"
    for i in range(len(stops)):
        text += "\t" + str(i + 1) + ". " + stops[i] + "\n"
    text += "\nCurrent Trip Legs: \n"
    leg_num = 1
    trip_distance = 0.0
    leg_distance = 0.0
    for i in range(len(stops)):
        last_stop, next_stop = "", ""
        leg_distance = 0.0

        # IS THERE ANOTHER LEG?
        if leg_num < len(stops):
            text += "\t" + str(i + 1) + '. '

            # GET THE LAST STOP
            last_stop = stops[leg_num - 1]

            # AND GET THE NEXT STOP
            next_stop = stops[leg_num]

            # FIND THE ROUTE FOR THIS LEG
            route = airport_graph.find_path(last_stop, next_stop)

            if len(route) < 2:
                text += "No Route Found from " + last_stop + " to " + next_stop + "\n"
            else:
                for i in range(len(route) - 1):
                    a1 = airport_graph.get_node_data(route[i])
                    a2 = airport_graph.get_node_data(route[i + 1])
                    distance = Airport.calculate_distance(a1, a2)
                    leg_distance += distance
                    if i == 0:
                        text += a1.get_code()
                    text += "-" + a2.get_code()
                text += " (Leg Distance: " + str(leg_distance) + " miles)\n"

            # MOVE TO THE NEXT LEG
            leg_num += 1
            trip_distance += leg_distance
    text += "Total Trip Distance: " + str(trip_distance) + " miles\n\n"
    print(text)

def display_menu():
    # DISPLAY THE MENU
    text = "ENTER A SELECTION\n"
    text += "S) Add a Stop to your Trip\n"
    text += "U) Undo\n"
    text += "R) Redo\n"
    text += "E) Empty Trip\n"
    text += "Q) Quit\n"
    print(text)

def get_user_input(prompt):
    answer = input(prompt)
    return answer

def process_user_input():
    choice = get_user_input("-")
    if choice == "S":
        entered_code = get_user_input("\nEnter the Airport Code: ")
        if airport_graph.node_exists(entered_code):
            neighbors = airport_graph.get_neighbors(entered_code)

            # MAKE SURE IT IS NOT THE SAME AIRPORT CODE AS THE PREVIOUS STOP
            if len(stops) > 0:
                last_stop = stops[-1]
                if last_stop == entered_code:
                    print("DUPLICATE STOP ERROR - NO STOP ADDED")
                else:
                    transaction = AppendStopTransaction(stops, entered_code)
                    tps.add_transaction(transaction)
            else:
                transaction = AppendStopTransaction(stops, entered_code)
                tps.add_transaction(transaction)
        else:
            print("INVALID AIRPORT CODE ERROR - NO STOP ADDED")
    # UNDO A TRANSACTION
    elif choice == "U":
        tps.undo_transaction()
    # REDO A TRANSACTION
    elif choice == "R":
        tps.do_transaction()
    # CLEAR ALL TRANSACTIONS
    elif choice == "E":
        tps.clear_all_transactions()
    # QUIT
    elif choice == "Q":
        return False
    return True

def init_all_airports():
    # FIRST ADD ALL THE AIRPORTS
    with open('data/Flights.json', 'r') as f:
        airport_data = json.load(f)
        for airport_json in airport_data['airports']:
            new_airport = Airport(airport_json['code'],
                                   airport_json['latitudeDegrees'],
                                   airport_json['latitudeMinutes'],
                                   airport_json['longitudeDegrees'],
                                   airport_json['longitudeMinutes'])
            airport_graph.add_node(airport_json['code'], new_airport)

        # NOW CONNECT THE AIRPORTS
        for edge_json in airport_data['edges']:
            init_edge(edge_json[0], edge_json[1])

def init_edge(node1, node2):
    a1 = airport_graph.get_node_data(node1)
    a2 = airport_graph.get_node_data(node2)
    distance = Airport.calculateDistance(a1, a2)
    airport_graph.add_edge(node1, node2, distance)
    airport_graph.add_edge(node2, node1, distance)

init_all_airports()

# LOOP FLAG VARIABLE
keep_going = True
while keep_going:
    display_airports()
    display_current_trip()
    display_menu()
    keep_going = process_user_input()

