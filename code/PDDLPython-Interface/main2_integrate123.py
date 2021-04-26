
"""
The code might require additional python packages to install (for sure it needs the 'ply' package but could require more)

Additionally, you might need to recompile the planners

To recompile METRIC_FF_V21
Enter ./pddl/planners/ext_planners/MetricFF-v2.1
Remove the executable ff and all of the files ending in .o
Run from the terminal the command 'make'. Make creates a new ff program compiled for your system.

If you're using MacOS use the equivalent of make to compile plain C code .


I would suggest to use only METRIC_FF_V21 that has all of the requirements you need
"""


from pddl.planners import METRIC_FF_V21 # This package contains a bunch of PDDL planners.
from pddl.planners import VHPOP # This package contains a bunch of PDDL planners.
from pddl.domains.pucrs import load_pucrs_dataset, get_pucrs_instance # This package contains a dataset of pddl domains
from pddl.parser import PDDLParser
from pyswip import Prolog
prolog = Prolog()

prolog.consult("domain.pl")


gesture = []
for soln7 in prolog.query("gesture(X,_,E)"):
    #print(soln7["X"], soln7["E"])
    gesture.append(soln7["E"])

#c = ' '.join(gesture)
#c = gesture
c = gesture[0]
d = gesture[1]
e = gesture[2]
f = gesture[3]
g = gesture[4]


speech = []
#print("\n Rules for speech")
for soln5 in prolog.query("speech(X,_,E)"):
    print(soln5["X"], soln5["E"])
    speech.append(soln5["E"])
print(speech)
#c = ' '.join(gesture)
#c = gesture
h = speech[0]
i = speech[1]



#f = ['clear', 'polite', 'listen', 'gestures']
#g = ' '.join(f)


    #(:action check_medi
    #    :parameters (?p - human ?l - location ?r - robot ?pl - polite ?cl - clear)
    #    :precondition (human_asked ?p ?cl ?pl) 
    #    :effect (medichecked ?r ?p)
    #) 

    #(:action robot_respond
    #    :parameters (?p - human ?l - location ?r - robot ?cl - clear ?pl - polite ?c -cup)
    #    :precondition (and (at ?r ?l) (detected_human ?p ?l)) 
    #    :effect (and (when (human_asked ?p ?cl ?pl) (robot_responded ?r ?cl ?pl))
    #                 (when (detected_cup ?c ?l) (robot_responded ?r ?cl ?pl)))
    #)    


    #(:durative-action check_medi
    #    :parameters (?p - human ?l - location ?r - robot ?pl - polite ?cl - clear)
    #    :duration (= ?duration (medicheck_time ?r))
    #    :condition (and (at start (human_asked ?p ?cl ?pl))
    #                    (over all (at ?r ?l))
    #                    (at end (robot_responded ?r ?cl ?pl))) 
    #    :effect (and (over all (medichecked ?r ?p)) 
    #                 (at end (robot_responded ?r ?cl ?pl)))
    #)    
    #(human_asked ?p - human)

    #(:action human_ask
    #    :parameters (?p - human ?l - location ?r - robot ?s - speech)
    #    :precondition (and (detected_human ?p ?l) (greeted ?r ?p))
    #    :effect (and (cup_request ?s) (pending_answer ?s))
    #)  


domain_str = """
(define (domain sp1)
 (:requirements :typing :strips :adl)

 (:types    location agent item - object 
            robot human comm - agent 
            room - location
            fruit cup table - item
            speak gesture listen - comm)


(:predicates    

        (at ?o - object ?l - location)
        (detected_human ?p - human  ?l - room)
        (detected_cup ?c - cup  ?l - room)
        (holded ?c - cup ?p - human)
        (medichecked ?r - robot ?p - human)
        (human_asked ?p - human)
        (robot_responded ?r - robot ?s - speak ?g - gesture)
        (robot_responded_quest ?r - robot ?s - speak ?g - gesture)
        (robot_responded_caction ?r - robot ?s - speak ?g - gesture)
        (robot_responded_caction1 ?r - robot ?s - speak ?g - gesture)
        (robot_responded_caction2 ?r - robot ?s - speak ?g - gesture)
        (listening ?r - robot ?g - gesture)

)

(:action detect_human

        :parameters (?p - human ?r - robot ?l - location)
        :precondition (at ?r ?l)
        :effect (detected_human ?p ?l)

    )

 

    (:action detect_cup

        :parameters (?p - human ?c - cup ?r - robot ?l - location ?s - speak ?g - gesture)
        :precondition (and (medichecked ?r ?p) 
                           (robot_responded_quest ?r ?s ?g)
                           )
        :effect (and (detected_cup ?c ?l) (robot_responded_caction ?r ?s ?g) )
    )

 

    (:action greet

        :parameters (?r - robot ?p - human ?l - location ?s - speak ?g - gesture)
        :precondition (and (at ?r ?l) (detected_human ?p ?l)) 
        :effect  (robot_responded ?r ?s ?g)
    )

 

    (:action hold

        :parameters (?c - cup ?p - human ?l - location ?r - robot ?s - speak ?g - gesture)
        :precondition (and (detected_human ?p ?l) 
                           (detected_cup ?c ?l) 
                           (robot_responded_caction1 ?r ?s ?g) 
                           (medichecked ?r ?p) 
                           (listening ?r ?g)
                           ) 
        :effect (and (holded ?c ?p) (robot_responded_caction ?r ?s ?g) )

    )    

    

    (:action check_medi
        :parameters (?p - human ?l - location ?r - robot ?s - speak ?g - gesture)
        :precondition (and (human_asked ?p) (robot_responded_quest ?r ?s ?g) )
        :effect (medichecked ?r ?p)
    )  

    

 

    (:action human_ask
        :parameters (?p - human ?l - location ?r - robot ?s - speak ?g - gesture)
        :precondition (and (detected_human ?p ?l) (robot_responded ?r ?s ?g) )
        :effect (human_asked ?p) 
    )  

    

    (:action robot_greet
        :parameters (?p - human ?l - location ?r - robot ?s - speak ?g - gesture ?c -cup)
        :precondition (detected_human ?p ?l)
        :effect (robot_responded ?r ?s ?g)
    )

 

    (:action robot_ask_question
        :parameters (?p - human ?l - location ?r - robot ?s - speak ?g - gesture ?c -cup)
        :precondition (human_asked ?p) 
        :effect (robot_responded_quest ?r ?s ?g)
    )

 

    (:action robot_confirms_medicheck
        :parameters (?p - human ?l - location ?r - robot ?s - speak ?g - gesture ?c -cup)
        :precondition (medichecked ?r ?p)
        :effect (robot_responded_caction ?r ?s ?g)
    )  

 

    (:action robot_confirms_cupdetect
        :parameters (?p - human ?l - location ?r - robot ?s - speak ?g - gesture ?c -cup)
        :precondition (detected_cup ?c ?l) 
        :effect (robot_responded_caction1 ?r ?s ?g)
    )  

 

    (:action robot_confirms_humanwcup
        :parameters (?p - human ?l - location ?r - robot ?s - speak ?g - gesture ?c -cup)
        :precondition (holded ?c ?p) 
        :effect (robot_responded_caction2 ?r ?s ?g)
    )  

 

    (:action start_listening
        :parameters (?p - human ?l - location ?r - robot ?g - gesture)
        :precondition (detected_human ?p ?l)
        :effect (listening ?r ?g) 
    )

)


"""

problem_str = """
(define (problem test12)

(:domain sp1)

 

(:objects person0 - Human 
          pepper0 - Robot 
          apple - Fruit
          cup0 - Cup
          table0 - Table
          room0 - Room
          {i} - Speak
          {h} - Speak
          {c} - Gesture
          {d} - Gesture
          {e} - Gesture
          {f} - Gesture
          {g} - Gesture)

 

(:init
(at pepper0 room0)
)

(:goal (and  
(robot_responded pepper0 speakloud showhandsup)
(listening pepper0 showattention)
(robot_responded_quest pepper0 speaklowtone showexplain)
(robot_responded_caction pepper0 speakloud showexplain)
(robot_responded_caction1 pepper0 speakloud showexplain)
(robot_responded_caction2 pepper0 speakloud showexplain)
(holded cup0 person0) ) 
)
)
"""


#Planner if there is no cup

domain_ncup = """
(define (domain spncup)
 (:requirements :typing :strips :adl)


 (:types    location agent item - object 
            robot human speak - agent 
            room - location
            fruit cup table - item
            clear polite listenatt - speak)

(:predicates    
        (at ?o - object ?l - location)
        (detected_human ?p - human  ?l - room)
        (greeted ?r - robot ?p - human)
        (detected_cup ?c - cup  ?l - room)
        (holded ?c - cup ?p - human)
        (medichecked ?r - robot ?p - human)
        (human_asked ?p - human)
        (exit ?r - robot)
        (robot_responded ?r - robot ?cl - clear ?pl - polite)
)


    (:action detect_human
        :parameters (?p - human ?r - robot ?l - location)
        :precondition (at ?r ?l)
        :effect (detected_human ?p ?l)
    )

    (:action detect_cup
        :parameters (?p - human ?c - cup ?r - robot ?l - location )
        :precondition (and (detected_human ?p ?l) 
                           (human_asked ?p) 
                           (medichecked ?r ?p) 
                           )
        :effect (when (not (detected_cup ?c ?l))  (exit ?r))
    )

    (:action robot_exited_SP
        :parameters (?p - human ?c - cup ?r - robot ?l - location )
        :precondition (and 
                           (greeted ?r ?p)
                           (human_asked ?p)
                           (not (detected_cup ?c ?l)) ) 
        :effect (exit ?r)
    )

    (:action greet
        :parameters (?r - robot ?p - human ?l - location ?pl - polite ?cl - clear)
        :precondition (and (at ?r ?l) (detected_human ?p ?l)) 
        :effect (and (greeted ?r ?p) (robot_responded ?r ?cl ?pl))
    )

    (:action hold
        :parameters (?c - cup ?p - human ?l - location ?r - robot ?cl - clear ?pl - polite)
        :precondition (and (detected_human ?p ?l) 
                           (detected_cup ?c ?l) 
                           (robot_responded ?r ?cl ?pl) 
                           (medichecked ?r ?p) 

                           ) 
        :effect (holded ?c ?p)
    )    
    
    (:action check_medi
        :parameters (?p - human ?l - location ?r - robot)
        :precondition (human_asked ?p) 
        :effect (medichecked ?r ?p)
    )  
    
    (:action human_ask
        :parameters (?p - human ?l - location ?r - robot)
        :precondition (and (detected_human ?p ?l) (greeted ?r ?p))
        :effect (human_asked ?p)
    )  
    
    (:action robot_respond
        :parameters (?p - human ?l - location ?r - robot ?cl - clear ?pl - polite ?c -cup)
        :precondition (and (at ?r ?l) (detected_human ?p ?l)) 
        :effect (and (when (human_asked ?p) (robot_responded ?r ?cl ?pl))
                     (when (detected_cup ?c ?l) (robot_responded ?r ?cl ?pl)))
    )  
)


"""

problem_ncup = """
(define (problem test12)
(:domain spncup)

(:objects person0 - Human 
          pepper0 - Robot 
          apple - Fruit
          cup0 - Cup
          table0 - Table
          room0 - Room
          clear0 - Clear
          polite0 - Polite)

(:init
(at pepper0 room0)


)
(:goal (and 
(detected_human person0  room0)
(greeted pepper0 person0)
(exit pepper0))
)
)

"""

    
def MAIN(ptype=1):

    planner = METRIC_FF_V21
    #planner = VHPOP

    #dataset = load_pucrs_dataset()

    #domain, problems, observations = get_pucrs_instance(dataset, 'logistics', 0)

    #print(f'Planning for\nDOMAIN\n{domain}\nPROBLEM\n{problems[0]}')
    #d = domain_str.format(c = c)
    p = problem_str.format(c = c, d = d, e = e, f = f, g = g, h = h, i = i)

    """
    NB. the important thing about domain and problem is that calling str() on them returns valid PDDL domain and problem specifications.
    """
    #print(p)
    domain = PDDLParser.parse_string(domain_str)
    problem = PDDLParser.parse_string(p)

    domainncup = PDDLParser.parse_string(domain_ncup)
    problemncup = PDDLParser.parse_string(problem_ncup)


    a = ['planreal', 'planncup']
    pdict = {}
    for x in range(len(a)):
        pdict[x] = a[x]

    b = ['metricsreal', 'metricsncup']
    mdict = {}
    for x in range(len(b)):
        mdict[x] = b[x]


    if ptype == 1:
        pdict[0], mdict[0] = planner.make_plan(domain, problem)
        #rint(pdict.get(0)['outcome'])
        if pdict[0] is not None:
            for op in pdict[0]:
                print(op)
        else:
            print(str(pdict.get(0)['planner_output']))  # Print what went wrong
        return pdict[0]
    else:
        pdict[1], mdict[1] = planner.make_plan(domainncup, problemncup)
        #print(pdict.get(1)['outcome'])
        if pdict[1] is not None:
            for op in pdict[1]:
                print(op)
        else:
            print(str(pdict.get(1)['planner_output']))  # Print what went wrong
        return pdict[1]

    #print(problem)
    #plan, metrics = planner.make_plan(domain, problem)

    #return plan
    #print(plan)

    #print(metrics['outcome'])
    #if plan is not None:
    #    for op in plan:
    #        print(op)
    #else:
    #    print(str(metrics['planner_output']))  # Print what went wrong
    #return plan

if __name__ == '__main__':
    MAIN(2)






