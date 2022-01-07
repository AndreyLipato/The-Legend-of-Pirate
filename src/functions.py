import pygame
import os
import json
from settings import Settings


class GameExeption(Exception):
    pass


def load_image(name, color_key=None):
    fullname = joinPath(Settings.folder_data, Settings.folder_images, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        raise GameExeption(f'Cannot load image: {name}\n{message}')

    if color_key is None:
        image = image.convert_alpha()
    else:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)

    return image


def joinPath(*path: list[str]):
    return str(os.path.join(*path))


def createSprite(img: pygame.Surface, scale: int, group: pygame.sprite.Group, x=0, y=0):
    sprite = pygame.sprite.Sprite(group)
    sprite.rect = pygame.Rect(x, y, img.get_width() * scale, img.get_height() * scale)
    sprite.image = pygame.transform.scale(img, (sprite.rect.width, sprite.rect.height))
    return sprite


def loadJSON(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def rectIntersection(rect1: tuple[int, int, int, int], rect2: tuple[int, int, int, int]):
    return (
        rect1[0] + rect1[2] > rect2[0] and
        rect2[0] + rect2[2] > rect1[0] and
        rect1[1] + rect1[3] > rect2[1] and
        rect2[1] + rect2[3] > rect1[1]
    )
