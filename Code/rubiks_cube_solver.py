from vpython import *
import numpy as np
import random
import kociemba

def is_nearby(position, reference):
    noise = 0.2 + random.uniform(-0.01, 0.01)
    return (reference[0] - noise < position.x < reference[0] + noise and
            reference[1] - noise < position.y < reference[1] + noise and
            reference[2] - noise < position.z < reference[2] + noise)

def get_face_letter(rgb):
    rgb_tuple = (rgb.x, rgb.y, rgb.z)
    if rgb_tuple == (1, 0, 0):
        return 'F'
    elif rgb_tuple == (1, 1, 0):
        return 'R'
    elif rgb_tuple == (1, 0.5, 0):
        return 'B'
    elif rgb_tuple == (1, 1, 1):
        return 'L'
    elif rgb_tuple == (0, 0, 1):
        return 'U'
    elif rgb_tuple == (0, 1, 0):
        return 'D'
    return None

def extract_cube_state(blocks):
    """F = red, R = yellow, B = orange, L = white, U = blue, D = green"""
    stickers = ['0'] * 54
    for cubie in blocks:
        pos = cubie.pos
        col = get_face_letter(cubie.color)
        # U face
        if is_nearby(pos, (-1, 1.5, -1)): stickers[0] = col
        elif is_nearby(pos, (0, 1.5, -1)): stickers[1] = col
        elif is_nearby(pos, (1, 1.5, -1)): stickers[2] = col
        elif is_nearby(pos, (-1, 1.5, 0)): stickers[3] = col
        elif is_nearby(pos, (0, 1.5, 0)): stickers[4] = col
        elif is_nearby(pos, (1, 1.5, 0)): stickers[5] = col
        elif is_nearby(pos, (-1, 1.5, 1)): stickers[6] = col
        elif is_nearby(pos, (0, 1.5, 1)): stickers[7] = col
        elif is_nearby(pos, (1, 1.5, 1)): stickers[8] = col
        # R face
        elif is_nearby(pos, (1.5, 1, 1)): stickers[9] = col
        elif is_nearby(pos, (1.5, 1, 0)): stickers[10] = col
        elif is_nearby(pos, (1.5, 1, -1)): stickers[11] = col
        elif is_nearby(pos, (1.5, 0, 1)): stickers[12] = col
        elif is_nearby(pos, (1.5, 0, 0)): stickers[13] = col
        elif is_nearby(pos, (1.5, 0, -1)): stickers[14] = col
        elif is_nearby(pos, (1.5, -1, 1)): stickers[15] = col
        elif is_nearby(pos, (1.5, -1, 0)): stickers[16] = col
        elif is_nearby(pos, (1.5, -1, -1)): stickers[17] = col
        # F face
        elif is_nearby(pos, (-1, 1, 1.5)): stickers[18] = col
        elif is_nearby(pos, (0, 1, 1.5)): stickers[19] = col
        elif is_nearby(pos, (1, 1, 1.5)): stickers[20] = col
        elif is_nearby(pos, (-1, 0, 1.5)): stickers[21] = col
        elif is_nearby(pos, (0, 0, 1.5)): stickers[22] = col
        elif is_nearby(pos, (1, 0, 1.5)): stickers[23] = col
        elif is_nearby(pos, (-1, -1, 1.5)): stickers[24] = col
        elif is_nearby(pos, (0, -1, 1.5)): stickers[25] = col
        elif is_nearby(pos, (1, -1, 1.5)): stickers[26] = col
        # D face
        elif is_nearby(pos, (-1, -1.5, 1)): stickers[27] = col
        elif is_nearby(pos, (0, -1.5, 1)): stickers[28] = col
        elif is_nearby(pos, (1, -1.5, 1)): stickers[29] = col
        elif is_nearby(pos, (-1, -1.5, 0)): stickers[30] = col
        elif is_nearby(pos, (0, -1.5, 0)): stickers[31] = col
        elif is_nearby(pos, (1, -1.5, 0)): stickers[32] = col
        elif is_nearby(pos, (-1, -1.5, -1)): stickers[33] = col
        elif is_nearby(pos, (0, -1.5, -1)): stickers[34] = col
        elif is_nearby(pos, (1, -1.5, -1)): stickers[35] = col
        # L face
        elif is_nearby(pos, (-1.5, 1, -1)): stickers[36] = col
        elif is_nearby(pos, (-1.5, 1, 0)): stickers[37] = col
        elif is_nearby(pos, (-1.5, 1, 1)): stickers[38] = col
        elif is_nearby(pos, (-1.5, 0, -1)): stickers[39] = col
        elif is_nearby(pos, (-1.5, 0, 0)): stickers[40] = col
        elif is_nearby(pos, (-1.5, 0, 1)): stickers[41] = col
        elif is_nearby(pos, (-1.5, -1, -1)): stickers[42] = col
        elif is_nearby(pos, (-1.5, -1, 0)): stickers[43] = col
        elif is_nearby(pos, (-1.5, -1, 1)): stickers[44] = col
        # B face
        elif is_nearby(pos, (1, 1, -1.5)): stickers[45] = col
        elif is_nearby(pos, (0, 1, -1.5)): stickers[46] = col
        elif is_nearby(pos, (-1, 1, -1.5)): stickers[47] = col
        elif is_nearby(pos, (1, 0, -1.5)): stickers[48] = col
        elif is_nearby(pos, (0, 0, -1.5)): stickers[49] = col
        elif is_nearby(pos, (-1, 0, -1.5)): stickers[50] = col
        elif is_nearby(pos, (1, -1, -1.5)): stickers[51] = col
        elif is_nearby(pos, (0, -1, -1.5)): stickers[52] = col
        elif is_nearby(pos, (-1, -1, -1.5)): stickers[53] = col
    return stickers

def get_solution(blocks):
    state_str = ''.join(extract_cube_state(blocks))
    answer = kociemba.solve(state_str)
    print('solution is \n' + answer)
    return answer

class Cube3D:
    def __init__(self):
        self.active = True
        self.cubies = []
        self.step_angle = np.pi / 40
        self.solution_label = None

        scene.background = color.white
        scene.width = 1500
        scene.height = 600
        scene.range = 7
        scene.center = vector(0, 0, 0)

        sphere(pos=vector(0, 0, 0), size=vector(3, 3, 3), color=vector(0, 0, 0))
        tile_layout = [
            [vector(-1, 1, 1.5), vector(0, 1, 1.5), vector(1, 1, 1.5),
             vector(-1, 0, 1.5), vector(0, 0, 1.5), vector(1, 0, 1.5),
             vector(-1, -1, 1.5), vector(0, -1, 1.5), vector(1, -1, 1.5)],
            [vector(1.5, 1, -1), vector(1.5, 1, 0), vector(1.5, 1, 1),
             vector(1.5, 0, -1), vector(1.5, 0, 0), vector(1.5, 0, 1),
             vector(1.5, -1, -1), vector(1.5, -1, 0), vector(1.5, -1, 1)],
            [vector(-1, 1, -1.5), vector(0, 1, -1.5), vector(1, 1, -1.5),
             vector(-1, 0, -1.5), vector(0, 0, -1.5), vector(1, 0, -1.5),
             vector(-1, -1, -1.5), vector(0, -1, -1.5), vector(1, -1, -1.5)],
            [vector(-1.5, 1, -1), vector(-1.5, 1, 0), vector(-1.5, 1, 1),
             vector(-1.5, 0, -1), vector(-1.5, 0, 0), vector(-1.5, 0, 1),
             vector(-1.5, -1, -1), vector(-1.5, -1, 0), vector(-1.5, -1, 1)],
            [vector(-1, 1.5, -1), vector(0, 1.5, -1), vector(1, 1.5, -1),
             vector(-1, 1.5, 0), vector(0, 1.5, 0), vector(1, 1.5, 0),
             vector(-1, 1.5, 1), vector(0, 1.5, 1), vector(1, 1.5, 1)],
            [vector(-1, -1.5, -1), vector(0, -1.5, -1), vector(1, -1.5, -1),
             vector(-1, -1.5, 0), vector(0, -1.5, 0), vector(1, -1.5, 0),
             vector(-1, -1.5, 1), vector(0, -1.5, 1), vector(1, -1.5, 1)],
        ]
        face_colors = [
            vector(1, 0, 0), vector(1, 1, 0), vector(1, 0.5, 0),
            vector(1, 1, 1), vector(0, 0, 1), vector(0, 1, 0)
        ]
        face_angles = [
            (0, vector(0, 0, 0)), (np.pi / 2, vector(0, 1, 0)),
            (0, vector(0, 0, 0)), (np.pi / 2, vector(0, 1, 0)),
            (np.pi / 2, vector(1, 0, 0)), (np.pi / 2, vector(1, 0, 0))
        ]
        for idx, face in enumerate(tile_layout):
            for pos in face:
                tile = box(pos=pos, size=vector(0.98, 0.98, 0.1), color=face_colors[idx])
                tile.rotate(angle=face_angles[idx][0], axis=face_angles[idx][1])
                self.cubies.append(tile)
        self.faces = {'front': [], 'right': [], 'back': [], 'left': [], 'top': [], 'bottom': []}
        self.rotation = [None, 0, 0]
        self.move_queue = []

    def update_faces(self):
        self.faces = {'front': [], 'right': [], 'back': [], 'left': [], 'top': [], 'bottom': []}
        for cubie in self.cubies:
            if cubie.pos.z > 0.4:
                self.faces['front'].append(cubie)
            if cubie.pos.x > 0.4:
                self.faces['right'].append(cubie)
            if cubie.pos.z < -0.4:
                self.faces['back'].append(cubie)
            if cubie.pos.x < -0.4:
                self.faces['left'].append(cubie)
            if cubie.pos.y > 0.4:
                self.faces['top'].append(cubie)
            if cubie.pos.y < -0.4:
                self.faces['bottom'].append(cubie)
        for k in self.faces:
            self.faces[k] = set(self.faces[k])

    def animate(self):
        rot = self.rotation
        dA = self.step_angle
        if rot[0] == 'front_ccw':
            for cubie in self.faces['front']:
                cubie.rotate(angle=dA, axis=vector(0, 0, 1), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'right_ccw':
            for cubie in self.faces['right']:
                cubie.rotate(angle=dA, axis=vector(1, 0, 0), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'back_ccw':
            for cubie in self.faces['back']:
                cubie.rotate(angle=dA, axis=vector(0, 0, -1), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'left_ccw':
            for cubie in self.faces['left']:
                cubie.rotate(angle=dA, axis=vector(-1, 0, 0), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'top_ccw':
            for cubie in self.faces['top']:
                cubie.rotate(angle=dA, axis=vector(0, 1, 0), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'bottom_ccw':
            for cubie in self.faces['bottom']:
                cubie.rotate(angle=dA, axis=vector(0, -1, 0), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'front_cw':
            for cubie in self.faces['front']:
                cubie.rotate(angle=-dA, axis=vector(0, 0, 1), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'right_cw':
            for cubie in self.faces['right']:
                cubie.rotate(angle=-dA, axis=vector(1, 0, 0), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'back_cw':
            for cubie in self.faces['back']:
                cubie.rotate(angle=-dA, axis=vector(0, 0, -1), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'left_cw':
            for cubie in self.faces['left']:
                cubie.rotate(angle=-dA, axis=vector(-1, 0, 0), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'top_cw':
            for cubie in self.faces['top']:
                cubie.rotate(angle=-dA, axis=vector(0, 1, 0), origin=vector(0, 0, 0))
            rot[1] += dA
        elif rot[0] == 'bottom_cw':
            for cubie in self.faces['bottom']:
                cubie.rotate(angle=-dA, axis=vector(0, -1, 0), origin=vector(0, 0, 0))
            rot[1] += dA
        if abs(rot[1] - rot[2]) < dA / 2:
            self.rotation = [None, 0, 0]
            self.update_faces()

    def rotate_front_ccw(self):
        if self.rotation[0] is None:
            self.rotation = ['front_ccw', 0, np.pi / 2]

    def rotate_right_ccw(self):
        if self.rotation[0] is None:
            self.rotation = ['right_ccw', 0, np.pi / 2]

    def rotate_back_ccw(self):
        if self.rotation[0] is None:
            self.rotation = ['back_ccw', 0, np.pi / 2]

    def rotate_left_ccw(self):
        if self.rotation[0] is None:
            self.rotation = ['left_ccw', 0, np.pi / 2]

    def rotate_top_ccw(self):
        if self.rotation[0] is None:
            self.rotation = ['top_ccw', 0, np.pi / 2]

    def rotate_bottom_ccw(self):
        if self.rotation[0] is None:
            self.rotation = ['bottom_ccw', 0, np.pi / 2]

    def rotate_front_cw(self):
        if self.rotation[0] is None:
            self.rotation = ['front_cw', 0, np.pi / 2]

    def rotate_right_cw(self):
        if self.rotation[0] is None:
            self.rotation = ['right_cw', 0, np.pi / 2]

    def rotate_back_cw(self):
        if self.rotation[0] is None:
            self.rotation = ['back_cw', 0, np.pi / 2]

    def rotate_left_cw(self):
        if self.rotation[0] is None:
            self.rotation = ['left_cw', 0, np.pi / 2]

    def rotate_top_cw(self):
        if self.rotation[0] is None:
            self.rotation = ['top_cw', 0, np.pi / 2]

    def rotate_bottom_cw(self):
        if self.rotation[0] is None:
            self.rotation = ['bottom_cw', 0, np.pi / 2]

    def do_move(self):
        moves = ["F", "R", "B", "L", "U", "D", "F'", "R'", "B'", "L'", "U'", "D'"]
        if self.rotation[0] is None and self.move_queue:
            move = self.move_queue.pop(0)
            if move == "F":
                self.rotate_front_cw()
            elif move == "R":
                self.rotate_right_cw()
            elif move == "B":
                self.rotate_back_cw()
            elif move == "L":
                self.rotate_left_cw()
            elif move == "U":
                self.rotate_top_cw()
            elif move == "D":
                self.rotate_bottom_cw()
            elif move == "F'":
                self.rotate_front_ccw()
            elif move == "R'":
                self.rotate_right_ccw()
            elif move == "B'":
                self.rotate_back_ccw()
            elif move == "L'":
                self.rotate_left_ccw()
            elif move == "U'":
                self.rotate_top_ccw()
            elif move == "D'":
                self.rotate_bottom_ccw()

    def randomize(self):
        moves = ["F", "R", "B", "L", "U", "D", "F'", "R'", "B'", "L'", "U'", "D'"]
        for _ in range(25):
            self.move_queue.append(random.choice(moves))

    def show_solution(self):
        sol = get_solution(self.cubies)
        if self.solution_label:
            self.solution_label.visible = False
        self.solution_label = text(
            text=f'Solution: {sol}',
            pos=vector(-4, -3, 0),
            height=0.25,
            font='sans',
            color=color.black,
            align='left'
        )

    def auto_solve(self):
        sol = get_solution(self.cubies)
        for move in sol.split():
            if move.endswith('2'):
                base = move[:-1]
                self.move_queue.append(base)
                self.move_queue.append(base)
            else:
                self.move_queue.append(move)

    def controls(self):
        button(text='F', bind=self.rotate_front_cw)
        button(text="F'", bind=self.rotate_front_ccw)
        button(text='R', bind=self.rotate_right_cw)
        button(text="R'", bind=self.rotate_right_ccw)
        scene.append_to_caption("""
</div>
<div style='position: absolute; top: 0; right: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-top: 8px;'>
""")
        button(text='B', bind=self.rotate_back_cw)
        button(text="B'", bind=self.rotate_back_ccw)
        button(text='L', bind=self.rotate_left_cw)
        button(text="L'", bind=self.rotate_left_ccw)
        scene.append_to_caption("""
</div>
<div style='position: absolute; top: 0; right: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-top: 8px;'>
""")
        button(text='U', bind=self.rotate_top_cw)
        button(text="U'", bind=self.rotate_top_ccw)
        button(text='D', bind=self.rotate_bottom_cw)
        button(text="D'", bind=self.rotate_bottom_ccw)
        scene.append_to_caption("""
</div>
<div style='position: absolute; top: 0; right: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-top: 8px;'>
""")
        button(text='🎲 Scramble', bind=self.randomize)
        button(text='💡 Show Solution', bind=self.show_solution)
        button(text='🤖 Auto Solve', bind=self.auto_solve)

    def tick(self):
        rate(90)
        self.animate()
        self.do_move()

    def run(self):
        self.update_faces()
        self.controls()
        while self.active:
            self.tick()

if __name__ == "__main__":
    cube_solve = Cube3D()
    cube_solve.run()