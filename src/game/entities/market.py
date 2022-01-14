import pygame
from functions import load_image, multPos, renderText, scaleImg
from game.entity import Entity
from settings import Settings

coinImg = scaleImg(load_image("coin.png"), 0.25, 0.3)
font = pygame.font.Font(Settings.path_font, int(Settings.tileSize * 0.4) + 1)


class EntityMarket(Entity):
    def __init__(self, screen, data: dict = None):
        self.item = None
        self.priceImg = None
        self.price = 0
        super().__init__(screen, data)
        self.hidden = True
        self.ghostE = True
        self.ghostT = True
        self.width = 1
        self.height = 1
        self.buyZone = (0, 0, 1, 2)

    def applyData(self, data: dict):
        super().applyData(data)
        if ("price" in data):
            self.price = data["price"]
        if ("item id" in data):
            self.setItem(data["item id"])

    def setItem(self, id: str):
        self.item = Entity.createById(id, self.screen).image
        self.priceImg = renderText(font, 1, (Settings.tileSize, Settings.tileSize), str(self.price), "black")

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        if (Settings.drawHitboxes):
            self.draw_rect(surface, "pink", self.buyZone, False, True, True)

        if (not self.item):
            return
        itemX = self.x * Settings.tileSize + (self.width * Settings.tileSize - self.item.get_width()) / 2
        itemY = self.y * Settings.tileSize
        surface.blit(self.item, (itemX, itemY))
        surface.blit(coinImg, multPos((self.x, self.y + self.height * 0.7), Settings.tileSize))
        if (self.priceImg):
            surface.blit(self.priceImg, multPos((self.x + 0.3, self.y + self.height * 0.65), Settings.tileSize))

    def update(self):
        super().update()
        if (self.is_inRectD(self.buyZone, self.screen.player)):
            pass
            # self.screen.player.message = self.speech


Entity.registerEntity("market", EntityMarket)
