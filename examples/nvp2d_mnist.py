import numpy as np
import torch
import torch.utils.data as data
import torchvision.utils as utils
import torchvision.datasets as datasets
import torchvision.transforms as transforms

import deeprob.flows.models as flows
from deeprob.torch.datasets import WrappedDataset
from deeprob.torch.routines import train_model, test_model


if __name__ == '__main__':
    # Load the MNIST dataset and split the dataset
    in_shape = (1, 28, 28)
    in_features = np.prod(in_shape).item()
    data_train = datasets.MNIST('datasets', train=True, transform=transforms.ToTensor(), download=True)
    data_test = datasets.MNIST('datasets', train=False, transform=transforms.ToTensor(), download=True)
    n_val = int(0.1 * len(data_train))
    n_train = len(data_train) - n_val
    data_train, data_val = data.random_split(data_train, [n_train, n_val])

    # Wrap MNIST datasets for unsupervised setting
    data_train = WrappedDataset(data_train, unsupervised=True)
    data_val = WrappedDataset(data_val, unsupervised=True)
    data_test = WrappedDataset(data_test, unsupervised=True)

    # Instantiate a 2D RealNVP, implementing the multi-scale flows architecture
    realnvp = flows.RealNVP2d(
        in_shape,
        dequantize=True,   # Apply dequantization
        logit=1e-6,        # Apply logit transformation with a factor of 1e-6
        n_flows=1,         # The number of repetitions of the multi-scale flows architecture
        network='resnet',  # Use Residual Networks (ResNets) as conditioners.
        n_blocks=2,        # The number of blocks to use for the conditioners
        channels=32        # The number of channels for the convolutional layers of the conditioners
    )

    # Train the model using generative setting, i.e. by maximizing the log-likelihood
    train_model(
        realnvp, data_train, data_val, setting='generative',
        lr=1e-3, batch_size=128, epochs=20, patience=3,
        checkpoint='checkpoint-realnvp-2d-mnist.pt',
        optimizer_kwargs={'weight_decay': 5e-5},  # Introduce a small weight decay
    )

    # Test the model using generative setting
    # Also, compute bits-per-dimension
    mu_ll, sigma_ll = test_model(realnvp, data_test, setting='generative', batch_size=64)
    bpp = (-mu_ll / np.log(2)) / in_features
    print('Mean LL: {} - Two Stddev LL: {} - Bits per Dimension: {}'.format(
        round(mu_ll, 2), round(sigma_ll, 2), round(bpp, 3)
    ))

    # Sample some data points and plot them
    realnvp.eval()  # Make sure to switch to evaluation mode
    n_samples = 10
    images = realnvp.sample(n_samples ** 2).cpu()
    utils.save_image(images, 'realnvp-mnist-samples.png', nrow=n_samples, padding=0)

    # Save the model to file
    torch.save(realnvp.state_dict(), 'realnvp-mnist.pt')
