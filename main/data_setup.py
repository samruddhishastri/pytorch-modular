import os
import glob
from re import I
import cv2 as cv
import numpy as np

from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from torch.utils import data

NUM_WORKERS = os.cpu_count()

class CustomDatasetClass(data.Dataset):
    def __init__(self, dataset_path):
        super(CustomDatasetClass, self).__init__()
        self.img_files = glob.glob(os.path.join(dataset_path, "images", "*"))
        self.masks =  []
        for img in self.img_files:
            self.masks.append(os.path.join(dataset_path, "ground_truth", os.path.basename(img)))

    def __getitem__(self, index):
        img = cv.cvtColor(cv.imread(self.img_files[index]), cv.COLOR_BGR2GRAY)
        mask = cv.cvtColor(cv.imread(self.masks[index]), cv.COLOR_BGR2GRAY)
        img = cv.resize(img, (256, 256), interpolation = cv.INTER_NEAREST)
        mask = cv.resize(mask, (256, 256), interpolation = cv.INTER_NEAREST)
        img = np.expand_dims(img, 0)
        mask = np.expand_dims(mask, 0)
        return img, mask

    def __len__(self):
        return len(self.img_files)

def create_dataloaders(
    dataset: str,
    batch_size: int,
    num_workers: int=NUM_WORKERS
):
    train_dir = os.path.join(dataset, "train")
    val_dir = os.path.join(dataset, "val")
    test_dir = os.path.join(dataset, "test")

    train_data = CustomDatasetClass(train_dir)
    val_data = CustomDatasetClass(val_dir)
    test_data = CustomDatasetClass(test_dir)

    train_dataloader = DataLoader(
        train_data,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )

    val_dataloader = DataLoader(
        val_data,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )

    test_dataloader = DataLoader(
        test_data,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )

    return train_dataloader, test_dataloader, val_dataloader
