import DRE
# ['Common definitions for 'Code items generator'' begin (DON'T REMOVE THIS LINE!)]
# Generic code items' definitions
dre = DRE.DRE()

def obtainVarName( variable ):
    # ['<global>::obtainVarName' begin]
    for k, v in locals().items():
        if v is variable:
            a_as_str = k
    return a_as_str
    # ['<global>::obtainVarName' end]

# ['Common definitions for 'Code items generator'' end (DON'T REMOVE THIS LINE!)]
