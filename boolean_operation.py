

def apply_boolean_operation(state_1, state_2, operation):
    if operation == 'union':
        if state_1 == 'FULL' or state_2 == 'FULL':
            return 'FULL'

        if state_1 == 'EMPTY' and state_2 == 'EMPTY':
            return 'EMPTY'

        return 'PARTIAL'

    elif operation == 'intersection':
        if state_1 == 'EMPTY' or state_2 == 'EMPTY':
            return 'EMPTY'

        if state_1 == 'FULL' and state_2 == 'FULL':
            return 'FULL'

        return 'PARTIAL'


    if operation == 'difference':
        if state_1 == 'EMPTY':
            return 'EMPTY'
        if state_1 == 'FULL' and state_2 == 'EMPTY':
            return 'FULL'
        if state_1 == 'FULL' and state_2 == 'FULL':
            return 'EMPTY'
        if state_1 == 'FULL' and state_2 == 'PARTIAL':
            return 'PARTIAL'
        if state_1 == 'PARTIAL' and state_2 == 'EMPTY':
            return 'PARTIAL'
        if state_1 == 'PARTIAL' and state_2 == 'FULL':
            return 'EMPTY'
        if state_1 == 'PARTIAL' and state_2 == 'PARTIAL':
            return 'PARTIAL'
    else:
        raise 
