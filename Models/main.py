import numpy as np
from torch.utils.data import DataLoader, SubsetRandomSampler, ConcatDataset
import time
from Models.GTSRBDataset import GTSRBDataset
from Models.GTSRBModel import GTSRBModel
from Models.Transforms import transformations, DEFAULT_TRANSFORM
from Models.util.Consts import *


def print_time(time_taken: float) -> None:
    """
    Utility function for time printing
    :param time_taken: the time we need to print
    """
    hours, rem = divmod(time_taken, 3600)
    minutes, seconds = divmod(rem, 60)
    print("\tTime taken: {:0>2}:{:0>2}:{:05.2f}\n".format(int(hours), int(minutes), seconds))


def main():
    # dataset initialization
    def_dataset = GTSRBDataset(transform=DEFAULT_TRANSFORM)
    datasets = [def_dataset]

    special_transforms_ratio = 0.2

    train_set_size = len(def_dataset)
    indices = list(range(train_set_size))
    for data_transform in transformations.values():
        np.random.shuffle(indices)
        split = int(np.floor(special_transforms_ratio * train_set_size))
        transform_sample = indices[:split]

        special_dataset = GTSRBDataset(transform_sample, transform=data_transform)
        datasets.append(special_dataset)

    trainDataset = ConcatDataset(datasets)
    oldTrainDataset = GTSRBDataset(transform=DEFAULT_TRANSFORM)
    testDataset = GTSRBDataset(train=False, transform=DEFAULT_TRANSFORM)

    print(f'old data size: {len(oldTrainDataset)}, new size: {len(trainDataset)}')

    validationRatio = 0.2

    indices = list(range(len(trainDataset)))
    np.random.shuffle(indices)
    split = int(np.floor(validationRatio * len(trainDataset)))
    trainSample = SubsetRandomSampler(indices[:split])
    validSample = SubsetRandomSampler(indices[split:])

    batch_size = 128
    num_workers = 4

    dataLoaders = {
        TRAIN: DataLoader(trainDataset, batch_size=batch_size, num_workers=num_workers, sampler=trainSample),
        VALID: DataLoader(trainDataset, batch_size=batch_size, num_workers=num_workers, sampler=validSample),
        TEST: DataLoader(testDataset, batch_size=batch_size, num_workers=num_workers)
    }

    epochs = 1

    # 1st model
    print('\n------------------------1st Model------------------------')
    start_time = time.time()
    model1 = GTSRBModel(1)
    print(model1)
    print(f'number of parameters: {model1.count_parameters()}')
    model1.train_model(epochs, dataLoaders)
    end_time = time.time()
    print_time(end_time - start_time)

    # 2nd model
    print('\n------------------------2nd Model-----------------------')
    start_time = time.time()
    model2 = GTSRBModel(2, dropout=True, batch_normalization=True)
    print(model2)
    print(f'number of parameters: {model2.count_parameters()}')
    model2.train_model(epochs, dataLoaders)
    end_time = time.time()
    print_time(end_time - start_time)

    # 3rd model
    print('\n------------------------3rd Model------------------------')
    start_time = time.time()
    model3 = GTSRBModel(3, dropout=True, batch_normalization=True, fully_connected_nn=False)
    print(model3)
    print(f'number of parameters: {model3.count_parameters()}')
    model3.train_model(epochs, dataLoaders)
    end_time = time.time()
    print_time(end_time - start_time)


if __name__ == '__main__':
    main()
