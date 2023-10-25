def IsValid(dictionary, keys):
    amount = 0
    for i in keys:
        if i in dictionary:
            amount += 1
    return amount == len(dictionary)

def IsFullValid(dictionary, keys):
    if IsValid(dictionary, keys):
        return len(dictionary) == len(keys)
    else:
        return False