#https://github.com/ReactiveX/RxPY/blob/master/examples/chess/chess.py
import sys
from os.path import dirname, join

import pygame

import rx
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

    scheduler = PyGameScheduler(pygame)
    mousemove = Subject()

    def convert_rec(origin, ev, idx):
        (old_idx, old_rect) = origin
        new_rect = old_rect.copy()
        new_rect.top = ev[1]
        new_rect.left = ev[0] + idx * 32
        return (idx, new_rect)

    def image2update(image, idx):
        mousemove.pipe(
            ops.delay(0.1 * idx, scheduler=scheduler),
            ops.scan(lambda origin, ev: convert_rec(origin, ev, idx), (idx, images[idx].get_rect())),
            ops.pairwise()
        )

    def on_error(err):
        print("Got error: %s" % err)
        sys.exit()

    def render(arr):
        for item in arr:
            (idx, rect) = item[0]
            screen.blit(background, (rect.x, rect.y), rect)
            (idx, rect) = item[1]
            screen.blit(images[idx], rect)

        list = [item[0].rect for item in arr] + [item[1].rect for item in arr]
        pygame.display.update(list)
        pygame.display.flip()

    rx.from_(images).pipe(
        ops.flat_map_indexed(image2update),
        ops.merge_all(),
        ops.buffer(rx.interval(1.0/30))
    ).subscribe(render)

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