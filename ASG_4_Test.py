student_name = "जगदीप सिंह"
submitted_to = "वैशाली इंगळे"
print("STUDENT NAME:", student_name)
print("SUBMITTED TO:", submitted_to)


KB = {
    "Vehicle Fault Diagnosis": {
        "facts": ["engine_not_starting", "battery_low", "headlights_dim", "starter_clicking",
                  "engine_overheating", "coolant_low", "oil_low", "vehicle_old"],
        "rules": [
            (["battery_low", "headlights_dim"], "electrical_system_weak"),
            (["battery_low", "starter_clicking"], "electrical_system_weak"),
            (["electrical_system_weak", "engine_not_starting"], "starting_system_fault"),
            (["starting_system_fault", "vehicle_old"], "battery_replacement_required"),
            (["engine_overheating", "coolant_low"], "cooling_system_fault"),
            (["engine_overheating", "oil_low"], "lubrication_system_fault"),
            (["cooling_system_fault", "lubrication_system_fault"], "severe_engine_risk"),
        ],
    }
}


def show(case):
    print("FACTS:")
    facts = KB[case]["facts"]
    for i in range(len(facts)):
        print(f"  F{i+1}. {facts[i]}")

    print("\nRULES:")
    rules = KB[case]["rules"]
    for i in range(len(rules)):
        cond, concl = rules[i]
        print(f"  R{i+1}. IF {' AND '.join(cond)} THEN {concl}")


def forward_chaining(facts, rules):
    known = list(facts)          # copy of facts
    changed = True

    while changed:
        changed = False
        for conditions, conclusion in rules:
            all_true = True
            for x in conditions:
                if x not in known:
                    all_true = False

            if all_true and conclusion not in known:
                known.append(conclusion)
                print("Rule fired:", conditions, "->", conclusion)
                changed = True

    new_facts = []
    for f in known:
        if f not in facts:
            new_facts.append(f)
    return new_facts


def backward_chaining(goal, facts, rules):
    if goal in facts:
        print("Fact found:", goal)
        return True

    for conditions, conclusion in rules:
        if conclusion == goal:
            print("To prove", goal, "we need", conditions)
            all_proved = True
            for x in conditions:
                if not backward_chaining(x, facts, rules):
                    all_proved = False
            if all_proved:
                return True

    return False


case = "Vehicle Fault Diagnosis"
rules = KB[case]["rules"]
show(case)

facts = input("Enter facts (comma separated): ").replace(" ", "").split(",")
goal = input("Enter goal for backward chaining: ").strip()

print("Given facts:", facts)
print("\n--- FORWARD CHAINING ---")
print("New facts inferred:", forward_chaining(facts, rules))

print("\n--- BACKWARD CHAINING:", goal, "---")
print("Result:", backward_chaining(goal, facts, rules))
