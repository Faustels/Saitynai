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

def IsPutValid(dictionary, required, allPossible):
    for i in required:
        if i not in dictionary:
            return False
    return IsValid(dictionary, allPossible)

def EditElement(element, body, types, method):
    for i in types:
        if i in body:
            setattr(element, i, body[i])
        elif method == "PUT":
            setattr(element, i, None)
    return element