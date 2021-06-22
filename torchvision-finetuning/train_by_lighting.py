import torch
from utils.engine import train_one_epoch, evaluate
import utils.utils as utils

from fudan_dataset import PennFudanDataset
from fudan_model import  get_model_instance_segmentation, get_transform

from pytorch_lightning import LightningModule, Trainer


class FudanLitModel(LightningModule):

    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        images, targets = batch
        loss_dict = self.model(images, targets)
        losses = sum(loss for loss in loss_dict.values())
        return {'loss': losses}

    def validation_step(self, batch, batch_idx):
        images, targets = batch
        loss_dict = self.model(images, targets)
        losses = sum(loss for loss in loss_dict.values())
        return {'loss': losses}

    def configure_optimizers(self):
        optimizer = torch.optim.SGD(self.parameters(), lr=0.005,
                                    momentum=0.9, weight_decay=0.0005)
        return optimizer




def main():
    data_dir = '/data/datasets/PennFudanPed'

    # train on the GPU or on the CPU, if a GPU is not available
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    # our dataset has two classes only - background and person
    num_classes = 2

    # use our dataset and defined transformations
    dataset = PennFudanDataset(data_dir, get_transform(train=True))
    dataset_test = PennFudanDataset(data_dir, get_transform(train=False))

    # split the dataset in train and test set
    indices = torch.randperm(len(dataset)).tolist()
    dataset = torch.utils.data.Subset(dataset, indices[:-50])
    dataset_test = torch.utils.data.Subset(dataset_test, indices[-50:])

    # define training and validation data loaders
    data_loader = torch.utils.data.DataLoader(
        dataset, batch_size=2, shuffle=True, num_workers=4,
        collate_fn=utils.collate_fn)

    data_loader_test = torch.utils.data.DataLoader(
        dataset_test, batch_size=1, shuffle=False, num_workers=4,
        collate_fn=utils.collate_fn)

    # get the model using our helper function
    model = get_model_instance_segmentation(num_classes)
    litmodel = FudanLitModel(model)

    trainer = Trainer(fast_dev_run=True) # , accelerator="ddp", gpus=2
    trainer.fit(litmodel, data_loader, data_loader_test)

    torch.save(model.state_dict(), 'trained_lit.pth')
    print("That's it!")


if __name__ == "__main__":
    main()
