
# Add this file Amygdala.py to Modules folder. 
# The amygdala subsystem models affective responses to the presence or absence of a spider.
# When the spider is visible, one of three fear-level productions can fire—high fear, medium fear, or low fear
# Each type of fear writes a different neural code into the emotional buffer.
# This is the sub-symbolic representation of emotion. 
# Because these three productions currently share the same match conditions and utility values, the selected fear response is random.
# When the spider is not visible, a separate production sets the emotional state back to calm.

# -------------------------
# Define Amygdala Productions
# -------------------------
# This list stores all productions belonging to the amygdala subsystem.
# Each production checks the current visual input and updates the emotional buffer
# with a sub symbolic "neural code" representing the current affective state.

AmygdalaProductions = []

# This production represents a HIGH fear response to seeing a spider.
def high_fear_spider(memories):
    # Update the emotional buffer with the neural code for high fear.
    # The emotional buffer acts as the amygdala's current affective output.
    memories['working_memory']['emotional_buffer']['emotion_state'] = '01001010' 
    print('amygdala is detecting a high fearful situation !!!!!!!!!!!!!!!!!!!!!!!!')

# Add the high-fear production to the amygdala production list.
AmygdalaProductions.append({
    # This production matches when the spider is visually represented in working memory as visible = yes.   
    'matches': {'working_memory': {'visual_representation_buffer': {'spider': {'visible':'yes'}}}},
    #No negative conditions are required for this production.
    # In other words, nothing has to be explicitly absent for it to fire.
    'negations': {},
    # Utility determines the priority of this production relative to other
    # productions in the same production system.
    'utility': 10,
    # The action executed when the match conditions are satisfied.
    'action': high_fear_spider,
    # A short label used in traces/debugging.
    'report': "high_fear_spider",
})

#Same thing for medium fear.
def medium_fear_spider(memories):
    # Update the emotional buffer with the neural code for medium fear.
    memories['working_memory']['emotional_buffer']['emotion_state'] = '02001010' 
    print('amygdala is detecting a medium fearful situation !!!!!!!!!!!!!!!!!!!!!!!!')
AmygdalaProductions.append({
    'matches': {'working_memory': {'visual_representation_buffer': {'spider': {'visible':'yes'}}}},
    'negations': {},
    # Same utility as the other spider-fear productions.
    # If multiple productions match with the same utility, the architecture choses at random. 
    'utility': 10,
    'action': medium_fear_spider,
    'report': "medium_fear_spider",
})

#Same thing for low fear. 
def low_fear_spider(memories):
    # Update the emotional buffer with the neural code for low fear.
    memories['working_memory']['emotional_buffer']['emotion_state'] = '011001010' 
    print('amygdala is detecting a low fearful situation !!!!!!!!!!!!!!!!!!!!!!!!')
AmygdalaProductions.append({
    'matches': {'working_memory': {'visual_representation_buffer': {'spider': {'visible':'yes'}}}},
    'negations': {},
    'utility': 10,
    'action': low_fear_spider,
    'report': "low_fear_spider",
})

# This production represents a CALM or reduced-threat response.
# It fires when the spider is not currently visible.
def spider_calm_down(memories):
    # Set the emotional buffer to the neural code representing calm.
    memories['working_memory']['emotional_buffer']['emotion_state'] = '00000000' 
    print('amygdala is detecting relatively calm situation &&&&&&&&&&&&&&&&&&&&&&&&&&&')

# Add the calm-down production to the amygdala production list.
AmygdalaProductions.append({
    # This production matches when the spider is represented as not visible.
    'matches': {'working_memory': {'visual_representation_buffer': {'spider': {'visible':'no'}}}},
    'negations': {},
    'utility': 10,
    'action': spider_calm_down,
    'report': "spider_calm_down",
})


# Optional “contract” / assumptions
REQUIRES = {
    "working_memory_buffers": ["visual_command_buffer", "visual_representation_buffer"],
    "memories_keys": ["environment", "working_memory"],
}
