
def sort(id_list):
    """
    :param id_list: List containing artist ID's (Integers)
    :return: Sorted list in ascending order
    """
    id_list.sort()
    return id_list


def binary_search(id_list, id):
    """
    :param id_list: Sorted list containing artist ID's
    :param id: Id we are checking if it is in list
    :return: Bool
    """
    middle_index = len(id_list) // 2
    if id_list[middle_index] == id:
        return True
    if len(id_list) == 1:
        return False
    elif id > id_list[middle_index]:
        return binary_search(id_list[middle_index+1:], id)
    elif id < id_list[middle_index]:
        return binary_search(id_list[:middle_index], id)

