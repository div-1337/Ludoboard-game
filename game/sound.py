from pygame import mixer
from config import DICE_SOUND

def play_dice_sound():
    mixer.init()
    sound = mixer.Sound(DICE_SOUND)
    sound.play()
    sound.set_volume(0.2)
