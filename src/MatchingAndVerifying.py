# implementation: handle edge cases such as empty files and one hospital / one student
# also check if input is valid (student = hospital count)
# Task A: Matching Engine: Implement the hospital-proposing deferred acceptance algorithm 
#   Initially, all hospitals are unmatched and have not proposed to anyone.
#   While there exists an unmatched hospital that still has students left to propose to:
#   The hospital proposes to the next student on its preference list that it has not yet proposed to.
#   The student tentatively accepts the best hospital (according to the student's preferences) among its current tentative match (if any) and the new proposer, rejecting the other.
# n: number of hospital / students
# hospitals: list of lists preferences 2D array
# students: list of list preferences 2D array
# track pairs: two lists -> hospital_pairs and student_pairs where hospital_pairs[h] = student matched to hospital h

def GaleShapley(n, hospitals, students):
    hospital_pairs = [None] * n
    student_pairs = [None] * n
    
    free_hospitals = list((range(n))) # all hospitals start free from 0 ---> n hospitals, then are removed from this list once matched
    
    while len(free_hospitals) != 0:
        h = free_hospitals[0] #select first free hospital
        for s in hospitals[h]: # loop through current hospitals preferences and propose to that student on list
            if (student_pairs[s] is None):
                # match them
                hospital_pairs[h] = s
                student_pairs[s] = h
                free_hospitals.remove(h)
                break
            else:
                # student already matched, check if they prefer this hospital
                current_h = student_pairs[s]
                # if h index in student preference list < current_h index in preference list swap them
                if students[s].index(h) < students[s].index(current_h):
                    hospital_pairs[h] = s
                    student_pairs[s] = h
                    hospital_pairs[current_h] = None
                    free_hospitals.remove(h)
                    free_hospitals.append(current_h)
                    break
    return hospital_pairs

# reads file and converts to 0-based indexing due to the way I coded the algorithm
def parse_input(filename):
    # read the input example file
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        
        hospital_prefs = []
        for _ in range(n):
            prefs = [int(x) - 1 for x in f.readline().split()]
            hospital_prefs.append(prefs)
        
        student_prefs = []
        for _ in range(n):
            prefs = [int(x) - 1 for x in f.readline().split()]
            student_prefs.append(prefs)
    
    return n, hospital_prefs, student_prefs

# converts back to 1-based indexing for output as expected in the assignment instructions
def format_output(hospital_pairs):
    result = []
    for h, s in enumerate(hospital_pairs):
        result.append(f"{h + 1} {s + 1}")
    return result

# will check if input is valid / edge cases 
def validate_input(n, hospital_prefs, student_prefs):
    if n == 0:
        return True, "empty"
    if len(hospital_prefs) != n or len(student_prefs) != n:
        return False, "INVALID: hospital and student counts don't match n"
    return True, "valid"

# PART B: Verifier
def verify(n, hospitals, students, hospital_pairs):
    # check each hospital is matched to exactly one student
    if len(hospital_pairs) != n:
        return "INVALID: not all hospitals are matched"
    
    matched_students = []
    
    for h, s in enumerate(hospital_pairs):
        if s is None:
            return f"INVALID: hospital {h + 1} is not matched"
        if s < 0 or s >= n:
            return f"INVALID: hospital {h + 1} matched to invalid student {s + 1}"
        if s in matched_students:
            return f"INVALID: student {s + 1} is matched to multiple hospitals"
        matched_students.append(s)
    
    # check all students are matched (no missing)
    if len(matched_students) != n:
        return "INVALID: not all students are matched"
    
    # check no blocking pairs
    for h in range(n):
        current_s = hospital_pairs[h]
        h_rank_of_current = hospitals[h].index(current_s)
        
        # check all students prefer their current 
        for i in range(h_rank_of_current):
            s = hospitals[h][i]  # hospital h prefers this student over current match
            
            # Find which hospital this student is matched to
            other_h = None
            for h2, s2 in enumerate(hospital_pairs):
                if s2 == s:
                    other_h = h2
                    break
            
            # Does student s prefer hospital h over their current match?
            s_rank_of_h = students[s].index(h)
            s_rank_of_other = students[s].index(other_h)
            
            if s_rank_of_h < s_rank_of_other:
                return f"UNSTABLE: blocking pair hospital {h + 1} and student {s + 1}"
    
    return "VALID STABLE"
    
 
if __name__ == "__main__":
    n, hospital_prefs, student_prefs = parse_input("data/example.in")
    
    is_valid, message = validate_input(n, hospital_prefs, student_prefs)
    
    if not is_valid:
        print(message)
    elif n == 0:
        print("No matches (empty input)")
    else:
        hospital_pairs = GaleShapley(n, hospital_prefs, student_prefs)
        output = format_output(hospital_pairs)
        for line in output:
            print(line)
            
        # also write to file output, example.out
        with open("outputs/example.out", "w") as f:
            for line in output:
                f.write(line +"\n")
                
        # Run verifier
        result = verify(n, hospital_prefs, student_prefs, hospital_pairs)
        print(f"\nVerifier: {result}")
                
        