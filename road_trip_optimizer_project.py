"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Author : Maureen Wanjiku Githaiga
Project 3: Road Trip Optimizer

This project implements a program which can be used to examine distances and routes
between cities. Program accesses distance information,which can be different between to cities 
depending on the travel direction.

Program first asks user for the file containing the distance data between the known cities and the 
information is stored in a suitable data structure.
Several actions are implemented: 
display - program displays all the data stored in the distance data structure. 
add - new connections can be added to the data struture.
remove- a connection between two cities can be removed.
neighbours - displays the connections from a particular city to its neighbours.
route- shows the route which one should take when travelling from departure city to destination city.
"""


def find_route(data, departure, destination):
    """
    This function tries to find a route between <departure>
    and <destination> cities. It assumes the existence of
    the two functions fetch_neighbours and distance_to_neighbour
    (see the assignment and the function templates below).
    They are used to get the relevant information from the data
    structure <data> for find_route to be able to do the search.

    The return value is a list of cities one must travel through
    to get from <departure> to <destination>. If for any
    reason the route does not exist, the return value is
    an empty list [].

    :param data: Dictionary of lists,A data structure containing the distance
           information between the known cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: list[str], a list of cities the route travels through, or
           an empty list if the route can not be found. If the departure
           and the destination cities are the same, the function returns
           a two element list where the departure city is stored twice.
    """

    # +--------------------------------------+
    # |                                      |
    # |     DO NOT MODIFY THIS FUNCTION!     |
    # |                                      |
    # +--------------------------------------+

    if departure not in data:
        return []

    elif departure == destination:
        return [departure, destination]

    greens = {departure}
    deltas = {departure: 0}
    came_from = {departure: None}

    while True:
        if destination in greens:
            break

        red_neighbours = []
        for city in greens:
            for neighbour in fetch_neighbours(data, city):
                if neighbour not in greens:
                    delta = deltas[city] + \
                            distance_to_neighbour(data, city, neighbour)
                    red_neighbours.append((city, neighbour, delta))

        if not red_neighbours:
            return []

        current_city, next_city, delta = min(red_neighbours,
                                             key=lambda x: x[2])

        greens.add(next_city)
        deltas[next_city] = delta
        came_from[next_city] = current_city

    route = []
    while True:
        route.append(destination)
        if destination == departure:
            break
        destination = came_from.get(destination)

    return list(reversed(route))


def read_distance_file(file_name):
    """
    Reads the distance information from <file_name> and stores it
    in the dictionary. This data structure is also the return value,
    unless an error happens during the file reading operation.

    :param file_name: str, The name of the file to be read.
    :return Data: dictionary of list|
    None: A data structure containing thinformation
         read from the <file_name> or None if any kind of error happens.
         The data structure to be chosen is completely up to you as long
         as all the required operations can be implemented using it.
    """
    data = {}
    try:

        file = open(file_name, mode="r", encoding="utf-8")

        for row in file:
            info = row.rstrip().split(';')
            departure, destination, distance = row.rstrip().split(";")
            distance = int(distance)

            if departure not in data:
                data[departure] = []
            data[departure].append([destination, distance])

        return data

    except OSError:
        return None


def fetch_neighbours(data, city):
    """
    Returns a list of all the cities that are directly
    connected to parameter <city>. In other words, a list
    of cities where there exist an arrow from <city> to
    each element of the returned list. Return value is
    an empty list [], if <city> is unknown or if there are no
    arrows leaving from <city>.

    :param data: A dictionary of lists, A data structure containing
    the distance information between the known cities.
    :param city: str, the name of the city whose neighbours we
           are interested in.
    :return: list[str], the neighbouring city names in a list.
             Returns [], if <city> is unknown (i.e. not stored as
             a departure city in <data>) or if there are no
             arrows leaving from the <city>.
    """
    neighbours = []

    if city not in data:
        return []

    for departure in data:
        if departure == city:
            for destination in data[departure]:
                neighbours.append(destination[0])
    return neighbours


def distance_to_neighbour(data, departure, destination):
    """
    Returns the distance between two neighbouring cities.
    Returns None if there is no direct connection from
    <departure> city to <destination> city. In other words
    if there is no arrow leading from <departure> city to
    <destination> city.

    :param data: A dictionary of lists,A data structure containing the distance
    information between the known cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: int | None, The distance between <departure> and
           <destination>. None if there is no direct connection
           between the two cities.
    """

    if departure not in data:
        return None

    for departure_city in data:

        if departure_city == departure:
            for destination_city in data[departure_city]:

                if destination_city[0] == destination:
                    distance = destination_city[1]
                    return distance

                elif destination_city[0] == '':
                    return None


def display(data):
    '''
    Displays the information stored in the file

    :param data:  a dictionary of lists
    :return: str displays the contents of the data structure in three columns.
    The departure city ,destination city and distance between them.
    '''
    for key, value in sorted(data.items()):

        for dest_dist in sorted(value):
            print(f'{key.ljust(14)}{dest_dist[0].ljust(14)}'
                  f'{str(dest_dist[1]).rjust(5)}')


def add(data):
    '''
    Adds a new one directional departure,destination and distance to
    the dictionary.If the connection exists the new distance replaces it.

    :param data: a dictionary of lists
    :return data: the dictionary of lists with the additional departure city,
    destination city and distance between them.
    '''
    departure_input = input('Enter departure city: ')
    destination_input = input('Enter destination city: ')
    distance_input = input('Distance: ')

    try:

        distance = int(distance_input)
        if departure_input not in data:
            data[departure_input] = [[destination_input, distance]]

        else:
            for dest_distance in data[departure_input]:
                if dest_distance[0] == destination_input:
                    dest_distance[1] = distance
                    break
            else:
                data[departure_input].append([destination_input, distance])
        return data

    except ValueError:
        print(f"Error: '{distance_input}' is not an integer.")
        return


def remove(data):
    '''
    Removes a connection between cities.
    Only a one directional connection is removed.

    :param data: A dictionary of lists.Contains the departure as the key
    and the [destination ,distance] as the list value.
    '''
    departure_input = input('Enter departure city: ')

    if departure_input in data:
        destination_input = input('Enter destination city: ')

        for dest_distance in data[departure_input]:
            if dest_distance[0] == destination_input:
                data[departure_input].remove(dest_distance)
                return

        print(f"Error: missing road segment between "
              f"'{departure_input}' and '{destination_input}'.")

    else:
        print(f"Error: '{departure_input}' is unknown.")
        return


def find_city(data, destination):
    '''
    Finds if a destination city exits in the data values.

    :param data: A dictionary of lists.Contains the departure as the key
    and the [destination ,distance] as the list value.
    :param destination: str.the name of the destination city.
    :return: True if the destination city exists in the data |
    False if the destination city does not exist in the data

    '''
    for departure in data:

        for destinations in data[departure]:
            city_name = destinations[0]
            if city_name == destination:
                return True

    return False


def neighbours(data):
    '''
    Displays the connections from a particular city to its neighbours.

    :param data: A dictionary of lists.Contains the departure as the key
    and the [destination ,distance] as the list value.

    '''
    departure_input = input('Enter departure city: ')

    if find_city(data,departure_input):

        for departure in data:
            if departure == departure_input:
                for dest_distance in sorted(data[departure_input]):
                    print(f'{departure.ljust(14)}{dest_distance[0].ljust(14)}'
                          f'{str(dest_distance[1]).rjust(5)}')

    else:
        print(f"Error: '{departure_input}' is unknown.")


def route(data):
    '''
    Displays the route from the departure city to the destination city
    and the length of the route (distance).
    if the city has no destinations then the route does not exist.

    :param data: A dictionary of lists.Contains the departure as the key
    and the [destination ,distance] as the list value.

    '''
    departure_input = input('Enter departure city: ')

    if find_city(data,departure_input):

        destination_input = input('Enter destination city: ')
        routes = find_route(data, departure_input, destination_input)

        if len(routes) == 0:
            print(f"No route found between '{departure_input}' and "
                  f"'{destination_input}'.")
            return

        total_distance = 0
        for i in range(len(routes) - 1):
            departure_city = routes[i]
            destination_city = routes[i + 1]

            for departure in data:

                if departure == departure_city:
                    for destination in data[departure]:
                        if destination[0] == destination_city:
                            total_distance += destination[1]
                            break
                    break

        print(f"{'-'.join(routes)} ({total_distance} km)")

    else:
        print(f"Error: '{departure_input}' is unknown.")


def main():
    input_file = input("Enter input file name: ")

    distance_data = read_distance_file(input_file)

    if distance_data is None:

        print(f"Error: '{input_file}' can not be read.")
        return

    while True:

        action = input("Enter action> ")

        if action == "":
         print("Done and done!")
         return

        elif "display".startswith(action):
         display(distance_data)

        elif "add".startswith(action):
         add(distance_data)

        elif "remove".startswith(action):
         remove(distance_data)

        elif "neighbours".startswith(action):
         neighbours(distance_data)

        elif "route".startswith(action):
         route(distance_data)

        else:
         print(f"Error: unknown action '{action}'.")

if __name__ == "__main__":
    main()
