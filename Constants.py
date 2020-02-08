def get_constants():
    # shift types list
    shift_types = ['morning', 'afternoon', 'night']

    # contract types list
    contract_types = ['full_time', 'part_time', 'on_call']

    # skills list
    skills = ['head_nurse', 'regular_nurse', 'trainee']

    # weights
    lambdaS1 = 30
    lambdaS2_min = 15
    lambdaS2_max = 30
    lambdaS3 = 30
    lambdaS4 = 10
    lambdaS5 = 30
    lambdaS6 = 20
    lambdaS7 = 30
    return shift_types, contract_types, skills, lambdaS1, lambdaS2_min, lambdaS2_max, lambdaS3, lambdaS4, lambdaS5, lambdaS6, lambdaS7