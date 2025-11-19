


def format_symptom(symptom):
    return symptom.lower().replace(" ","_")




def yes_no_into_binary(value):
    #convert yes/no to 1/0 and  return 0 for empty input
    return 1 if value.lower=="yes" else 0



def sex_to_binary(value):
    #convert yes/no to 1/0 and  return 0 for empty input
    return 1 if value.lower=="male" else 0