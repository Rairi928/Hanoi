import pygame
import sys
import time

# ----------------------------------------
# ① はじめにディスク数を入力（1～10）
# ----------------------------------------
while True:
    try:
        NUM_DISKS = int(input("ディスクの数を入力 (1～7): "))
        if 1 <= NUM_DISKS <= 7:
            break
    except:
        pass

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")

WHITE = (255, 255, 255)
GRAY = (180, 180, 180)

PEG_X = [200, 400, 600]
PEG_Y = 450

DISK_HEIGHT = 25
COLORS = [
    (220, 20, 60),
    (34, 139, 34),
    (100, 149, 237),
    (255, 215, 0),
    (128, 0, 128),
    (255, 105, 180),
    (0, 255, 255),
    (255, 140, 0),
    (154, 205, 50),
    (199, 21, 133),
]

disk_widths = [40 + i * 30 for i in range(NUM_DISKS)]

# pegs[i] = 下から上へディスク番号を積む（大→小）
pegs = [
    list(reversed(range(NUM_DISKS))),
    [],
    [],
]

dragging_disk = None
dragging_src = None
move_count = 0


def draw():
    screen.fill(WHITE)

    for x in PEG_X:
        pygame.draw.rect(screen, GRAY, (x - 5, PEG_Y - 200, 10, 200))

    for peg_index, peg_stack in enumerate(pegs):
        base_y = PEG_Y
        for level, disk in enumerate(peg_stack):
            if disk == dragging_disk:
                continue
            width = disk_widths[disk]
            x = PEG_X[peg_index] - width // 2
            y = base_y - (level + 1) * DISK_HEIGHT
            pygame.draw.rect(screen, COLORS[disk], (x, y, width, DISK_HEIGHT))

    if dragging_disk is not None:
        mx, my = pygame.mouse.get_pos()
        width = disk_widths[dragging_disk]
        pygame.draw.rect(screen, COLORS[dragging_disk],
                         (mx - width // 2, my - DISK_HEIGHT // 2, width, DISK_HEIGHT))

    pygame.display.flip()


def can_place(peg_index, disk):
    peg = pegs[peg_index]
    if not peg:
        return True
    return disk < peg[-1]


def reset_all():
    global pegs, dragging_disk, dragging_src, move_count
    pegs = [
        list(reversed(range(NUM_DISKS))),
        [],
        [],
    ]
    dragging_disk = None
    dragging_src = None
    move_count = 0


def animate_move(disk, src, dst):
    global move_count
    pegs[src].pop()
    draw()
    time.sleep(0.15)

    pegs[dst].append(disk)
    move_count += 1
    print("移動回数:", move_count)

    draw()
    time.sleep(0.15)


def solve_hanoi(n, src, dst, aux):
    if n == 0:
        return
    solve_hanoi(n - 1, src, aux, dst)
    animate_move(n - 1, src, dst)
    solve_hanoi(n - 1, aux, dst, src)


clock = pygame.time.Clock()

while True:
    clock.tick(60)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ESCキー → 入力画面に戻る
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                reset_all()
                draw()
                time.sleep(0.5)
                solve_hanoi(NUM_DISKS, 0, 2, 1)

        # 掴む
        if event.type == pygame.MOUSEBUTTONDOWN and dragging_disk is None:
            mx, my = pygame.mouse.get_pos()
            for peg_index, peg_stack in enumerate(pegs):
                if not peg_stack:
                    continue
                disk = peg_stack[-1]
                width = disk_widths[disk]
                x = PEG_X[peg_index] - width // 2
                y = PEG_Y - DISK_HEIGHT
                if x <= mx <= x + width and y - 120 <= my <= PEG_Y:
                    dragging_disk = disk
                    dragging_src = peg_index
                    break

        # 離す
        if event.type == pygame.MOUSEBUTTONUP and dragging_disk is not None:
            mx, my = pygame.mouse.get_pos()
            dst_peg = min(range(3), key=lambda p: abs(mx - PEG_X[p]))

            if can_place(dst_peg, dragging_disk):
                pegs[dragging_src].pop()
                pegs[dst_peg].append(dragging_disk)
                move_count += 1
                print("移動回数:", move_count)

            dragging_disk = None
