import actions

p = [0.7, 0.1, 0.0, 0.2]

def defineProbabilityArray(action):
    if action == actions.UP:
        return [
            (actions.UP, p[0]),
            (actions.RIGHT, p[1]),
            (actions.DOWN, p[2]),
            (actions.LEFT, p[3])
        ]
    
    if action == actions.RIGHT:
        return [
            (actions.UP, p[3]),
            (actions.RIGHT, p[0]),
            (actions.DOWN, p[1]),
            (actions.LEFT, p[2])
        ]
    
    if action == actions.DOWN:
        return [
            (actions.UP, p[2]),
            (actions.RIGHT, p[3]),
            (actions.DOWN, p[0]),
            (actions.LEFT, p[1])
        ]
    
    if action == actions.LEFT:
        return [
            (actions.UP, p[1]),
            (actions.RIGHT, p[2]),
            (actions.DOWN, p[3]),
            (actions.LEFT, p[0])
        ]