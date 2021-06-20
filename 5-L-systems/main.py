import json
import os
from turtle import Screen, Turtle


def main():

    scr = Screen()
    pen = Turtle()
    system = LSystem(scr, pen, bg='#001035', fg='#FFFFFF')

    def clicked_screen(*_):
        system.draw_next()

    system.prepare()
    scr.onclick(clicked_screen)
    scr.mainloop()


class LSystem():
    _system_i = -1
    _systems = []
    _default_line_length = 8
    _default_recursion = 3

    def __init__(self, screen, turtle, **kwargs):
        self._scr = screen
        self._pen = turtle
        self._bg = kwargs['bg']
        self._fg = kwargs['fg']

        cwd = os.path.dirname(os.path.realpath(__file__))
        with open(cwd + '/lsystems.json', 'r') as file:
            self._systems = json.load(file)

    def prepare(self):
        self._scr.bgcolor(self._bg)
        self._pen.color(self._fg)
        self._pen.speed('fastest')
        self._pen.write('Click me to start!',
                        align='center', font=('Arial', 24, 'bold'))
        self._pen.pu()
        self._pen.right(90)
        self._pen.forward(50)
        self._pen.write('(maximize this window first)',
                        align='center', font=('Arial', 24, 'bold'))
        self._pen.color(self._bg)

    def draw_next(self):
        self._scr.reset()
        self._pen.reset()
        self._scr.delay(0)
        self._pen.speed('fastest')
        self._pen.color(self._fg)
        self._pen.ht()

        self._system_i += 1
        try:
            system = self._systems[self._system_i]
        except IndexError:
            self._scr.bye()
            print('Finished drawing last L-system!')
            return

        line_len, angle, name, pos, path = self._prepare_system(system)
        self._pen.pu()
        self._pen.goto(0, self._scr.window_height() / 2 - 50)
        self._pen.write(name, (0, 50), align='center', font=('Arial', 24, 'bold'))

        print('Drawing', name)
        self._draw_rule(line_len, angle, pos, path)

    def _prepare_system(self, system):
        if isinstance(system['angle'], str):
            angle = eval(system['angle'])
        else:
            angle = system['angle']
        try:
            line_len = system['line']
        except KeyError:
            line_len = self._default_line_length
        try:
            recursion = system['recursion']
        except KeyError:
            recursion = self._default_recursion
        try:
            name = system['name']
        except KeyError:
            name = 'System ' + str(self._system_i + 1)
        try:
            _pos = system['pos']
            _pos = (_pos[0] * self._scr.window_width() / 2,
                    _pos[1] * self._scr.window_height() / 2)
            pos = _pos
        except KeyError:
            pos = (-self._scr.window_width() / 2 + self._scr.window_width() / 4,
                   -self._scr.window_height() / 4)

        def get_rule_recursively(rules, rule, depth, _path=None):
            if _path is None:
                _path = []
            for sign in rules[rule]:
                if sign in ('+', '-', '[', ']'):
                    _path.append(sign)
                else:
                    if depth < recursion:
                        get_rule_recursively(rules, sign, depth + 1, _path)
                    else:
                        if sign == 'b':
                            _path.append('b')
                        else:
                            _path.append('F')
            return _path

        path = []
        for sign in system['axiom']:
            if sign in ('+', '-', '[', ']'):
                path.append(sign)
            else:
                path.extend(get_rule_recursively(system['rules'], sign, 0))
        return line_len, angle, name, pos, path

    def _draw_rule(self, line_len, angle, pos, path):
        self._pen.goto(pos[0], pos[1])
        self._pen.pd()
        last_pos = []

        for sign in path:
            if sign == '+':  # + clockwise turn
                self._pen.right(angle)
            elif sign == '-':  # counter-clockwise turn
                self._pen.left(angle)
            elif sign == '[':  # store current pos
                last_pos.append((self._pen.pos(), self._pen.heading()))
            elif sign == ']':  # pop the last pos
                pos, hdg = last_pos.pop()
                self._pen.pu()
                self._pen.goto(pos)
                self._pen.setheading(hdg)
                self._pen.pd()
            elif sign == 'b':  # move pen without leaving a trail
                self._pen.pu()
                self._pen.forward(line_len)
                self._pen.pd()
            else:  # move pen with a trail
                self._pen.forward(line_len)


if __name__ == '__main__':
    main()
