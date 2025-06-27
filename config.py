import os
import traceback
ASSETS_DIR = "Assets"
DICE_FOLDER = os.path.join(ASSETS_DIR, "Dice_Outcomes")
BOARD_IMAGE = os.path.join(ASSETS_DIR, "ludoboard.jpg")
DICE_SOUND = os.path.join(ASSETS_DIR, "Sounds", "Dice_Rolling.mp3")
DICE_ROLLED = 0
CURRENT_PLAYER = "blue"
DICE_FINAL_VALUE = 0
MAX_POSITIONS = 52              # TOTAL NUMBER OF INDEXES IN LUDOBOARD, IF YOU MAKE ANY EDITS TO LUDOBOARD IMAGE, CHANGE THIS NUMBER AS WELL
SHOULD_SWITCH_TURN = True       # New flag to control turn switching



                
def switch_player_turn():
    traceback.print_stack()
    players = list(PLAYER_PAWNS.keys())
    current_index = players.index(CURRENT_PLAYER)
    next_index = (current_index + 1) % len(PLAYER_ORDER)

    globals()['CURRENT_PLAYER'] = PLAYER_ORDER[next_index]
    globals()['DICE_ROLLED'] = 0
    globals()['DICE_FINAL_VALUE'] = 0
    print("✅ TURN SWITCH TRIGGERED")
    print(f"🔄 Turn switched. Now it's {CURRENT_PLAYER}'s turn")


PLAYER_ORDER = ["blue", "red", "green", "yellow"]  #ORDER OF THE TURNS




PLAYER_PAWNS = {
    "blue": [-1, -2, -3, -4],
    "red": [-11,-12,-13,-14],
    "green": [-21, -22, -23, -24],
    "yellow": [-31,-32,-33,-34]
}

PAWN_COORDINATES = {

    -34:(0.815, 0.235),
    -33:(0.815, 0.125),
    -32:(0.695, 0.125),
    -31:(0.695, 0.235),
    -24:(0.13, 0.235),
    -23:(0.13, 0.125),
    -22:(0.25, 0.125),
    -21: (0.25, 0.235),                    # OTHER COLOR PAWN SPAWNING PENDING, TURN EXCHANGE IN pawn.py On_Click
    -14: (0.13 , 0.82),
    -13: (0.25 , 0.82),
    -12: (0.25 , 0.71),
    -11: (0.13 , 0.71),
    -4: (0.695, 0.82),
    -3: (0.815, 0.82),
    -2: (0.815, 0.71),
    -1: (0.695, 0.71),    
     0: (0.85, 0.54),
     1: (0.79, 0.54),
     2: (0.725, 0.54),
     3: (0.6625, 0.54),
     4: (0.6, 0.54),
     5: (0.537, 0.605),
     6: (0.537, 0.670),
     7: (0.537, 0.735),
     8: (0.537, 0.8),
     9: (0.537, 0.865),
    10: (0.537, 0.929),
    11: (0.477, 0.929),
    12: (0.412, 0.929),
    13: (0.412, 0.865), #RED STARTING POINT
    14: (0.412, 0.8),
    15: (0.412, 0.735),
    16: (0.412, 0.670),
    17: (0.412, 0.605),
    18: (0.352, 0.54),
    19: (0.289, 0.54),
    20: (0.225, 0.54),
    21: (0.165, 0.54),
    22: (0.100, 0.54),
    23: (0.038, 0.54),
    24: (0.038, 0.475),
    25: (0.038, 0.410),
    26: (0.100, 0.410), #GREEN STARTING POINT
    27: (0.165, 0.410),
    28: (0.225, 0.410),
    29: (0.289, 0.410),
    30: (0.352, 0.410),
    31: (0.412, 0.342),
    32: (0.412, 0.278),
    33: (0.412, 0.212),
    34: (0.412, 0.146),
    35: (0.412, 0.08),
    36: (0.412, 0.014),
    37: (0.475, 0.014),
    38: (0.535, 0.014),
    39: (0.535, 0.08), #YELLOW STARTING POINT
    40: (0.535, 0.146),
    41: (0.535, 0.212),
    42: (0.535, 0.278),
    43: (0.535, 0.342),
    44: (0.6, 0.410),
    45: (0.6625, 0.410),
    46: (0.725, 0.410),
    47: (0.79, 0.410),
    48: (0.85, 0.410),
    49: (0.91, 0.410),
    50: (0.91, 0.475), # YAHAAN SE BLUE PAWN ANDAR LEKE JAANA HAI
    51: (0.91, 0.54)
}

SAFE_ZONES = [0, 13, 26, 39]


"""

PAWN K ANDAR LEKAR JAANE KI POSITIONS FOR BLUE 



X = 0.85
Y = 0.475



"""