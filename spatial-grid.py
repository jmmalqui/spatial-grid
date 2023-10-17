import pygame as pg
import random


def color_lerp(p1: pg.Vector3, p2: pg.Vector3, max, val):
    val = min(max, val)
    diff = p2 - p1
    step = diff / max
    res = p1 + (val * step)
    return res


class SpatialHash:
    def __init__(self, chunk_size: int) -> None:
        self.chunk_size = chunk_size
        self.chunks = {}

    def add(self, entity):
        if hasattr(entity, "pos") == False:
            raise ValueError("Entity must have a position component")
        key = self.get_entity_chunk(entity)
        if key not in self.chunks:
            self.chunks[key] = []
        self.chunks[key].append(entity)

    def get_entity_chunk(self, entity):
        chunk_x = int(entity.pos.x // self.chunk_size)
        chunk_y = int(entity.pos.y // self.chunk_size)
        key = (chunk_x, chunk_y)
        return key

    def get_pos_chunk(self, pos):
        chunk_x = int(pos.x // self.chunk_size)
        chunk_y = int(pos.y // self.chunk_size)
        key = (chunk_x, chunk_y)
        return key

    def remove(self, entity):
        key = self.get_entity_chunk(entity)
        if key not in self.chunks:
            raise ValueError("Chunk has not been created yet")
        self.chunks[key].remove(entity)

    def remove_from_chunk(self, chunk, entity):
        self.chunks[chunk].remove(entity)
        if len(self.chunks[chunk]) == 0:
            self.chunks.pop(chunk)

    def update(self, entity, entity_last_pos):
        chunk = self.get_pos_chunk(entity_last_pos)
        self.remove_from_chunk(chunk, entity)
        self.add(entity)

    def get(self, chunk_id):
        ...


class MockEntity:
    def __init__(self, pos) -> None:
        self.pos = pos
        self.vel = pg.Vector2(random.randint(-1, 1), random.randint(-1, 1))

    def update(self):
        self.last_pos = self.pos.copy()
        self.pos += self.vel
        if self.pos.x > 400:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = 400
        if self.pos.y > 400:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = 400
        sp_hash.update(self, self.last_pos)


sp_hash = SpatialHash(40)
ent_list = []
for i in range(15):
    point = pg.Vector2(random.randint(0, 400), random.randint(0, 400))
    ent = MockEntity(point)
    sp_hash.add(ent)
    ent_list.append(ent)


pg.init()
display = pg.display.set_mode([400, 400], pg.SRCALPHA)
clock = pg.time.Clock()

while True:
    clock.tick(60)
    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
    # upd
    for ent in ent_list:
        ent.update()
    # ren
    display.fill("black")
    for key in sp_hash.chunks.keys():
        color = color_lerp(
            pg.Vector3(0, 255, 0),
            pg.Vector3(255, 0, 0),
            3,
            len(sp_hash.chunks[key]),
        )
        pg.draw.rect(
            display,
            color,
            pg.Rect(
                key[0] * sp_hash.chunk_size,
                key[1] * sp_hash.chunk_size,
                sp_hash.chunk_size,
                sp_hash.chunk_size,
            ),
            0,
        )
    for ent in ent_list:
        pg.draw.circle(display, "white", ent.pos, 2, 0)
    pg.display.flip()
