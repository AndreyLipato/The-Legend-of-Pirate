class Settings:
    # width = 1920
    # height = 1080
    width = 720
    height = 405
    fps = 60
    overlay_height = 184
    folder_data = "data"
    folder_saves = "saves"
    folder_images = "images"
    folder_worlds = "worlds"
    screen_width = 15
    screen_height = 7
    demageDelay = 400
    fullscreen = False
    tileSize = 1
    drawHitboxes = True


Settings.tileSize = Settings.width / Settings.screen_width
Settings.overlay_height = Settings.height - Settings.screen_height * Settings.tileSize