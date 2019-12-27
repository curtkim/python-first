#https://github.com/ReactiveX/RxPY/blob/master/examples/chess/chess.py
import sys
from os.path import dirname, join

import pygame

from rx import operators as ops
from rx.subject import Subject
from rx.scheduler.mainloop import PyGameScheduler


def main():
    pygame.init()

    size = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Rx for Python rocks")

    black = 0, 0, 0
    background = pygame.Surface(screen.get_size())
    background.fill(black)             # fill the background black
    background = background.convert()  # prepare for faster blitting

    color = "white"
    base = dirname(__file__)
    files = [join(base, img % color) for img in [
        "chess_rook_%s.png",
        "chess_knight_%s.png",
        "chess_bishop_%s.png",
        "chess_king_%s.png",
        "chess_queen_%s.png",
        "chess_bishop_%s.png",
        "chess_knight_%s.png",
        "chess_rook_%s.png"
    ]]
    images = [pygame.image.load(image).convert_alpha() for image in files]

    def accumulator(acc, ev):
        new_arr = []
        for i, rect in enumerate(acc):
            new_rect = rect.copy()
            new_rect.top = ev[1]
            new_rect.left = ev[0] + i * 32
            new_arr.append(new_rect)
        return new_arr

    def on_error(err):
        print("Got error: %s" % err)
        sys.exit()

    def render(arr_pair):
        (erase, draw) = arr_pair #tuple destruction
        for rect in erase:
            screen.blit(background, (rect.x, rect.y), rect)

        for idx, rect in enumerate(draw):
            screen.blit(images[idx], rect)

        pygame.display.update(erase+draw)
        pygame.display.flip()

    scheduler = PyGameScheduler(pygame)
    mousemove = Subject()

    mousemove.pipe(
        #ops.delay(0.1 * i, scheduler=scheduler),
        ops.scan(accumulator, [image.get_rect() for image in images]),
        ops.pairwise(),
        ops.observe_on(scheduler)
    ).subscribe(render, on_error)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                pos = event.pos
                mousemove.on_next(pos)
            elif event.type == pygame.QUIT:
                sys.exit()

        scheduler.run()

if __name__ == '__main__':
    main()