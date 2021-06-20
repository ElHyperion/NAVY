import copy
import numpy as np
import matplotlib.pyplot as plt


D_UP = 0
D_DOWN = 1
D_LEFT = 2
D_RIGHT = 3


# Map definition and the required parameters.
# Try uncommenting the map below, along with the higher episodes count!

LEARNING_RATE = 0.05
GAMMA = 0.8
EPISODES = 100

ENV = np.array([
    [0,   0,   0,   0,   0],
    [0,  -1,   0,   0,  -1],
    [0,   0,   0,   0,   0],
    [0,   0,   0,  10,   0],
    [0,   0,   0,   0,   0],
])


# EPISODES = 350

# ENV = np.array([
#     [0,   0,   0,   0,   0],
#     [0,  -1,   0,  -1,   0],
#     [0,   0,   0,   0,  -1],
#     [0,  -1,  -1,   0,   0],
#     [0,  -1,  10,  -1,   0],
#     [0,  -1,   0,   0,   0],
#     [0,   0,   0,  -1,   0],
# ])


def generate_starting_point():
    row, col = ENV.shape
    x = np.random.randint(col)
    valid_y = np.where(ENV[:, x] == 0)
    y = np.random.choice(valid_y[0], 1)[0]
    return (y, x)


def move(direction, pos):
    if direction == D_UP:
        return (pos[0] - 1, pos[1])
    elif direction == D_DOWN:
        return (pos[0] + 1, pos[1])
    elif direction == D_LEFT:
        return (pos[0], pos[1] - 1)
    elif direction == D_RIGHT:
        return (pos[0], pos[1] + 1)


def main():

    row, col = ENV.shape

    # Initialize empty Q-matrix (a matrix of all 4 directions for every pos)
    q_matrix = np.zeros((row * col, 4))

    # Set environmental restrictions (map boundaries)
    for x in range(col):
        for y in range(row):
            q_pos = col * y + x
            if y == 0:
                q_matrix[q_pos][D_UP] = -100
            if y == row - 1:
                q_matrix[q_pos][D_DOWN] = -100
            if x == 0:
                q_matrix[q_pos][D_LEFT] = -100
            if x == col - 1:
                q_matrix[q_pos][D_RIGHT] = -100

    # 1 - TRAINING PHASE
    for _ in range(EPISODES):
        pos = generate_starting_point()

        for _ in range(50):
            q_pos = pos[0] * col + pos[1]

            directions = np.where(q_matrix[q_pos] >= -1)
            direction = np.random.choice(directions[0], 1)[0]
            new_pos = move(direction, pos)

            reward = ENV[new_pos[0]][new_pos[1]]
            new_q_pos = new_pos[0] * col + new_pos[1]
            new_value = LEARNING_RATE * (reward + GAMMA * max(q_matrix[new_q_pos]))
            q_matrix[q_pos][direction] += new_value
            pos = new_pos

            # Mouse reached either a trap or a cheese
            if reward != 0:
                break

    # Prepare the plot
    plt.style.use('dark_background')
    plt.axis('off')

    # 2 - TESTING PHASE
    positions = []

    for _ in range(20):
        trail = []

        pos = generate_starting_point()

        for _ in range(20):
            trail.append(copy.deepcopy(pos))
            img = copy.deepcopy(ENV)
            for pos_past in trail:
                img[pos_past[0]][pos_past[1]] = 6
            img[pos[0]][pos[1]] = 8
            img = plt.imshow(np.reshape(img, (row, col)))
            img.set_cmap('inferno')
            plt.pause(0.14)

            q_pos = pos[0] * col + pos[1]
            direction = np.argmax(q_matrix[q_pos])
            new_pos = move(direction, pos)
            reward = ENV[new_pos[0]][new_pos[1]]

            if reward == 10:
                print(f'Found the cheese in {len(trail)} steps! c:')
                break
            if reward == -1:
                print('The mouse died :c')
                break
            pos = new_pos
        else:
            print('The mouse got lost! :o')
        positions.append(trail)


if __name__ == '__main__':
    main()
