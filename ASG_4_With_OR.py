# Generated from: ASG_4_With_OR.ipynb
# Converted at: 2026-11-04T18:00:54.403Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

rules=[(("And",["fever","cough"]),"flu"),
       (("And",["flu","body pain"]),"see doctor"),
       (("Or",["sneez","running nose"]),"cold"),
       (("And",[("Or",["fever","flu"]),"sneez"]),"infection")
      ]
facts=["fever","cough","body pain"]
print(facts)
def show_condition(condition):
    if isinstance(condition,str):
        return condition
    operator,parts=condition
    return "("+(" "+operator+" ").join(show_condition(part) for part in parts)+")"

for condition,conclusion in rules:
    print("IF",show_condition(condition),"THEN",conclusion)

def condition_is_true(condition,known):
    if isinstance(condition,str):
        return condition in known
    operator,parts=condition
    if operator=="And":
        return all(condition_is_true(part,known) for part in parts)
    elif operator=="Or":
        return any(condition_is_true(part,known) for part in parts)

def forward(goal,rules,facts):
    changed=True
    known=list(facts)
    while changed:
        changed=False
        for condition,conclusion in rules:
            if condition_is_true(condition,known) and conclusion not in known:
                known.append(conclusion)
                print("IF",show_condition(condition) ,"THEN", conclusion)
                changed=False
    print(known)
    return goal in known

print(forward("see doctor",rules,facts))

def proved_condition(condition,rules,facts,checking):
    if isinstance(condition,str):
        return backward(condition,rules,facts,checking)
    operator,parts=condition
    if operator=="And":
        return all(proved_condition(part,rules,facts,checking) for part in parts)
    elif operator=="Or":
        return any(proved_condition(part,rules,facts,checking) for part in parts)
    else:
        return False

def backward(goal,rules,facts,checking=None):
    if checking is None:
        checking=set()

        ###these two lines dekh lena 
    if goal in facts:
        print("Fact",goal)
        return True
    if goal in checking:
        return False

    checking=checking|{goal} ##
    for condition,conclusion in rules:
        if conclusion==goal:
            print("we need to prove",goal,"we check",show_condition(condition))
            if proved_condition(condition,rules,facts,checking):
                return True
    return False

print(backward("see doctor",rules,facts))