
import pygame
import itertools


class Bird(pygame.sprite.Sprite):
    def __init__(self, images, idx, position, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = list(images.values())[idx]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position

        self.is_flapped = False
        self.down_speed = 0
        self.up_speed = 9

        self.bird_idx = idx
        self.bird_idx_cycle = itertools.cycle([0, 1, 2, 1])
        self.bird_idx_change_count = 0

    def update(self, boundary_values, time_passed):

        if self.is_flapped:
            self.up_speed -= 60 * time_passed
            self.rect.top -= self.up_speed
            if self.up_speed <= 0:
                self.unsetFlapped()
                self.up_speed = 9
                self.down_speed = 0
        else:
            self.down_speed += 40 * time_passed
            self.rect.bottom += self.down_speed

        is_dead = False
        if self.rect.bottom > boundary_values[1]:
            is_dead = True
            self.up_speed = 0
            self.down_speed = 0
            self.rect.bottom = boundary_values[1]
        if self.rect.top < boundary_values[0]:
            is_dead = True
            self.up_speed = 0
            self.down_speed = 0
            self.rect.top = boundary_values[0]

        self.bird_idx_change_count += 1
        if self.bird_idx_change_count % 5 == 0:
            self.bird_idx = next(self.bird_idx_cycle)
            self.image = list(self.images.values())[self.bird_idx]
            self.bird_idx_change_count = 0
        return is_dead

    def setFlapped(self):
        if self.is_flapped:
            self.up_speed = max(12, self.up_speed+1)
        else:
            self.is_flapped = True

    def unsetFlapped(self):
        self.is_flapped = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)