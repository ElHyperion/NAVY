import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from samples import PICS_SAMPLE as p_sample, PICS_DAMAGED as p_damaged


def prepare_sample(sample):
    sample = sample.flatten()
    sample[sample == 0] = -1
    return sample.reshape(1, len(sample))


def main():

    row, col = p_sample[0].shape

    # Memorize the samples
    stored_samples = []
    for sample in p_sample:

        sample_prepared = prepare_sample(sample)
        sample_t = sample_prepared.reshape(-1, 1)
        weighted_matrix = np.dot(sample_t, sample_prepared)
        np.fill_diagonal(weighted_matrix, 0)
        stored_samples.append(weighted_matrix)

    stored_weighted = np.sum(stored_samples, axis=0)

    # Recover damaged samples
    recovered_samples = []
    for sample in p_damaged:
        to_recover = prepare_sample(sample)

        for i in range(row * col):
            value = np.dot(to_recover, stored_weighted[:, i])
            to_recover[0][i] = np.sign(value)

        # Reshape into 2D array
        recovered = np.asarray(to_recover)
        recovered = np.reshape(recovered, (row, col))
        recovered[recovered == -1] = 0
        recovered_samples.append(recovered)

    # Plot drawing
    plt.style.use('dark_background')
    cmap = ListedColormap(['grey', 'b'])

    for i, recovered in enumerate(recovered_samples):
        _, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 8))
        ax1.set_axis_off()
        ax2.set_axis_off()
        ax3.set_axis_off()
        ax1.set_title('To recover')
        ax1.matshow(p_sample[i], cmap=cmap)
        ax2.set_title('Damaged')
        ax2.matshow(p_damaged[i], cmap=cmap)
        ax3.set_title('After recovering')
        ax3.matshow(recovered, cmap=cmap)

    plt.show()


if __name__ == '__main__':
    main()
