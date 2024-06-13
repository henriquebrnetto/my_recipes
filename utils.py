def decorate(password):
    if len(password)>3:
        half = len(password)//2
        return "rei leao"+password[:half]+"brigadeiro"+password[half:]+"bolo de cenoura"
    else:
        return "eu tentei"+password+"eu nao sei"
    
def flatten(lst):
    return [val for l in lst for val in l]