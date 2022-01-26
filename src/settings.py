import sys
from ntpath import join


class Settings:
    version = "v1.0"
    width = 1920
    height = 1080
    fps = 60
    overlay_height = 184
    folder_data = "data"
    folder_saves = "saves"
    folder_images = "images"
    folder_entities = "entities"
    folder_tiles = "tiles"
    folder_worlds = "worlds"
    folder_sounds = "sounds"
    path_font = None
    screen_width = 15
    screen_height = 7
    damageDelay = 400
    damageDelayPlayer = 1600
    fullscreen = True
    tileSize = 1
    drawHitboxes = False
    drawNoneImgs = False
    disableAI = False
    moveScreenOnNumpad = False


try:
    # Если программа запущена как exe файл, то данные храняться по такому пути
    newPath = join(sys._MEIPASS, Settings.folder_data)
    Settings.folder_data = newPath
except Exception:
    pass

Settings.tileSize = Settings.width / Settings.screen_width
Settings.overlay_height = Settings.height - Settings.screen_height * Settings.tileSize
Settings.path_font = join(Settings.folder_data, "fonts", "Fifaks10Dev1.ttf")
