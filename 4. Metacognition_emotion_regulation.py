# This agent will enact Type-1 and Type-2 metacognitive monitoring of the emotion fear, and Type-2 metacognitive regulation of this emotion. 
# This model simulates a simple task (i.e., sandwich-making). The agent will feel fear upon their visual system seeing a spider. 
# The amygdala evaluates whether the current situation is calm or fear-inducing based on spider visibility which is the sub-symbolic representation/
# The emotion system interprets that affective state into an understood emotion label which is the symbolic representation
# This agent will then enact Type-1 and Type-2 metacognitive monitoring of the various fear states (calm, low, medium, high - see amydala.py). 
# If the agent detects 'high fear', they will engage Type-2 metacognitive control by using a breathing technique to down-regulate emotion from 'high fear' to 'calm'.  

# import modules
from modules.visual_productions import VisualProductions
from modules.motor_productions import MotorProductions
from modules.dm_symbolic import DM_Symbolic_Productions
from modules.dm_subsymbolic import DM_Subsymbolic_Productions
from modules.trace_manager import Trace_Productions
from modules.amygdala_2 import AmygdalaProductions


# import environment actors
from environment_actors.spiderProductions import spider_productions

# import production cycle
from computational_architecture.production_cycle import ProductionCycle

# -------------------------
# Initialize Memories (Default values)
# -------------------------
working_memory = {
    'focusbuffer': {'state': 'bread1','emotion':'calm'}, #symbolic representation of emotion 
    'motor_buffer': {'state': 'no_action'},  # Initially, no motor action is scheduled.
    'visual_representation_buffer': {},
    'visual_command_buffer': {'state': 'scan'},  # Command to continuously scan the environment.
    'DM_output_buffer': {},
    'DM_retieval_buffer': {'matches': {'side_order': 'yes', 'condition': 'good'},'negations': {'condition': 'bad'}},
    'DM_command_buffer': {'state': 'normal'},
    'emotional_buffer': {'emotion_state': '00000000'} # neural code for calm state
    #sub symbolic representation of emotion 
}

middle_memory = { #This is not needed. Just to keep track of states. Can be removed for simpler output. 
    'lag0': {'state': None},
    'lag1': {'state': None},
    'lag2': {'state': None}
}

declarative_memory = {'fries': {'name': 'fries',
                                'condition': 'good',
                                'side_order': 'yes',
                                'utility':4},
                      'house_salad': {'name': 'house_salad',
                                      'condition': 'good',
                                      'side_order': 'no',
                                      'utility':1},
                      'poutine': {'name': 'poutine',
                                  'condition': 'good',
                                  'side_order': 'yes',
                                  'utility':5},
                      'ceasar_salad': {'name': 'ceasar_salad',
                                       'condition': 'bad',
                                       'side_order': 'no',
                                       'utility':10},


                      }


environment = {
    'bread1': {'location': 'counter'},
    'cheese': {'location': 'counter'},
    'ham': {'location': 'counter'},
    'bread2': {'location': 'counter'},
    'breath': {'location': 'out'}, #added breathing technique 
    'spider': {'visible': 'no'}
}
memories = {
    'working_memory': working_memory,
    'middle_memory': middle_memory,
    'declarative_memory': declarative_memory,
    'environment': environment  # Motor productions still update the actual environment.
}

# -------------------------
# Define Procedural Productions (Sandwich Steps) and Emotion Productions (Understanding Emotion).
# -------------------------

ProceduralProductions = []
EmotionProductions = []
#Original code did not have emotion productions which caused the detection of emotion and sandwhich making productions to compete due to utility.
#Created emotion productions to seperate the two so both productions fire and not just one or the other. 


# This production interprets the amygdala's calm code.
# When the emotional buffer is set to calm, that is understood and placed in the focus buffer
# This is sub-symbolic representation of emotion from emotion state / emotion buffer going to symbolic representation within focus buffer
def calmness_monitor(memories):
    memories['working_memory']['focusbuffer']['emotion'] = 'calm'
    print('understanding current emotion as calm @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
EmotionProductions.append({
    'matches': {'working_memory': {'emotional_buffer': {'emotion_state': '00000000'}}},
    'negations': {},
    'utility': 5,
    'action': calmness_monitor,
    'report': "calm",
})

# When the focus buffer understands the emotion as high fear, a breath is applied to change high fear to calm in both focus buffer and emotion state 
def fear_monitor(memories):
    print('understanding current emotion as high fear ########################################')
    #Using fear1 for now to represent high fear but its just a name can be changed to whatever
    memories['working_memory']['focusbuffer']['emotion'] = 'fear1'

    # do the breath immediately once understanding emotion as high fear
    # changes breath location in environnement from out to in (this can be changed to anything, just to represent the technique for now)
    memories['environment']['breath']['location'] = 'in'
    print("breath executed immediately: breath moved from out to in.")

    # breathing changes emotion to calm
    memories['working_memory']['emotional_buffer']['emotion_state'] = '00000000'
    memories['working_memory']['focusbuffer']['emotion'] = 'calm'

    print("breathing changed emotion to calm.")

    # put breath back to out 
    memories['environment']['breath']['location'] = 'out'

# Fire when the emotional buffer contains the high-fear code.
EmotionProductions.append({
    'matches': {'working_memory': {'emotional_buffer': {'emotion_state': '01001010'}}},
    'negations': {},
    'utility': 5,
    'action': fear_monitor,
    'report': "fear",
})


#Same thing for medium fear but without breathing technique
def fear_monitor2(memories):
    memories['working_memory']['focusbuffer']['emotion'] = 'fear2'
    print('understanding current emotion as medium fear ########################################')

# Fire when the emotional buffer contains the medium-fear code.
EmotionProductions.append({
    'matches': {'working_memory': {'emotional_buffer': {'emotion_state': '02001010'}}},
    'negations': {},
    'utility': 5,
    'action': fear_monitor2,
    'report': "fear2",
})

#Same thing for low fear but without breathing technique
def fear_monitor3(memories):
    memories['working_memory']['focusbuffer']['emotion'] = 'fear3'
    print('understanding current emotion as low fear ########################################')

# Fire when the emotional buffer contains the low-fear code.
EmotionProductions.append({
    'matches': {'working_memory': {'emotional_buffer': {'emotion_state': '011001010'}}},
    'negations': {},
    'utility': 5,
    'action': fear_monitor3,
    'report': "fear3",
})


# ---------------



def bread1(memories):
    # Set up motor action to move bread1 from 'counter' to 'plate'
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'bread1',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 4
    })
    # Update the focus for the next production.
    memories['working_memory']['focusbuffer']['state'] = 'cheese'
    print("bread1 production executed: focus updated to 'cheese'; motor action scheduled for bread1.")


ProceduralProductions.append({
    'matches': {
        'working_memory': {
             'focusbuffer': {'state': 'bread1'},
             'visual_representation_buffer': {'bread1': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': bread1,
    'report': "bread1",
})
# -------------------------

def cheese(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'cheese',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 4
    })
    memories['working_memory']['focusbuffer']['state'] = 'ham'
    print("cheese production executed: focus updated to 'ham'; motor action scheduled for cheese.")

ProceduralProductions.append({
    'matches': {
        'working_memory':
            {'focusbuffer': {'state': 'cheese'},
            'visual_representation_buffer': {'bread1': {'location': 'plate'},
                                             'cheese': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': cheese,
    'report': "cheese",
})
# -------------------------

def ham(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'ham',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 4
    })
    memories['working_memory']['focusbuffer']['state'] = 'bread2'
    print("ham production executed: focus updated to 'bread2'; motor action scheduled for ham.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {'focusbuffer': {'state': 'ham'},
        'visual_representation_buffer': {
            'cheese': {'location': 'plate'},
            'ham': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': ham,
    'report': "ham",
})
# -------------------------

def bread2(memories):
    motorbuffer = memories['working_memory']['motor_buffer']
    motorbuffer.update({
        'state': 'do_action',
        'env_object': 'bread2',
        'slot': 'location',
        'newslotvalue': 'plate',
        'delay': 4
    })
    memories['working_memory']['focusbuffer']['state'] = 'done'
    print("bread2 production executed: focus updated to 'done'; motor action scheduled for bread2.")

ProceduralProductions.append({
    'matches': {
        'working_memory': {'focusbuffer': {'state': 'bread2'},
        'visual_representation_buffer': {
            'ham': {'location': 'plate'},
            'bread2': {'location': 'counter'}}}},
    'negations': {},
    'utility': 10,
    'action': bread2,
    'report': "bread2",
})


def announce_sandwich(memories):
    print("Ham and cheese sandwich is almost ready, just adding the bread")
    print("while I am adding the bread I will recall if there was a side order")
    memories['working_memory']['focusbuffer']['state'] = 'sandwich_done'
    # Set retrieval conditions
    memories['working_memory']['DM_retieval_buffer']['matches'] = {'side_order': 'no', 'condition': 'good'}
    memories['working_memory']['DM_retieval_buffer']['negations'] = {'condition': 'bad'}
    # tell DM to work on the retrival
    #memories['working_memory']['DM_command_buffer']['state'] = 'retrieve'
    memories['working_memory']['DM_command_buffer']['state'] = 'retrieve_partial'

ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'done'}}},
    'negations': {},
    'utility': 10,
    'action': announce_sandwich,
    'report': "announce_sandwich",
})

def announce_side(memories):
    print("I recall the side order was")
    print(memories['working_memory']['DM_output_buffer'])
    memories['working_memory']['focusbuffer']['state'] = 'end'
ProceduralProductions.append({
    'matches': {'working_memory': {'focusbuffer': {'state': 'memory_retrieved'}}},
    'negations': {},
    'utility': 10,
    'action': announce_side,
    'report': "announce_side",
})


# -------------------------
# Production Systems Setup
# -------------------------
ProductionSystem1_Countdown = 1  # For procedural productions.
ProductionSystem2_Countdown = 1  # For motor productions.
ProductionSystem3_Countdown = 1  # For visual productions (vision system).
ProductionSystem4_Countdown = 1  # For DM symbolic productions.
ProductionSystem5_Countdown = 1  # For DM sub symbolic productions.
ProductionSystem6_Countdown = 1  # For spider productions.
ProductionSystem7_Countdown = 1  # For trace manager.
ProductionSystem8_Countdown = 1  # For trace manager.
ProductionSystem9_Countdown = 1 #for emotions
#added 9th production system for understanding emotions so it is not competing with sandwhich 




DelayResetValues = {
    'ProductionSystem1': ProductionSystem1_Countdown,
    'ProductionSystem2': ProductionSystem2_Countdown,
    'ProductionSystem3': ProductionSystem3_Countdown,
    'ProductionSystem4': ProductionSystem4_Countdown,
    'ProductionSystem5': ProductionSystem5_Countdown,
    'ProductionSystem6': ProductionSystem6_Countdown,
    'ProductionSystem7': ProductionSystem7_Countdown,
    'ProductionSystem8': ProductionSystem8_Countdown,
    'ProductionSystem9': ProductionSystem9_Countdown
}
#added 9th production system for understanding emotions so it is not competing with sandwhich 

AllProductionSystems = {
    'ProductionSystem1': [ProceduralProductions, ProductionSystem1_Countdown],
    'ProductionSystem2': [MotorProductions, ProductionSystem2_Countdown],
    'ProductionSystem3': [VisualProductions, ProductionSystem3_Countdown],
    'ProductionSystem4': [DM_Symbolic_Productions, ProductionSystem4_Countdown],
    'ProductionSystem5': [DM_Subsymbolic_Productions, ProductionSystem5_Countdown],
    'ProductionSystem6': [spider_productions, ProductionSystem6_Countdown],
    'ProductionSystem7': [Trace_Productions, ProductionSystem7_Countdown],
    'ProductionSystem8': [AmygdalaProductions, ProductionSystem8_Countdown],
    'ProductionSystem9': [EmotionProductions, ProductionSystem9_Countdown]

}
#added 9th production system for understanding emotions so it is not competing with sandwhich 


# -------------------------
# Initialize and Run the Production Cycle
# -------------------------
ps = ProductionCycle()
ps.run_cycles(memories, AllProductionSystems, DelayResetValues, cycles=24, millisecpercycle=50)
