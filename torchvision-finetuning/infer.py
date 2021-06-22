import torch
from fudan_dataset import PennFudanDataset
from fudan_model import  get_model_instance_segmentation, get_transform

def main():
    data_dir = '/data/datasets/PennFudanPed'
    dataset_test = PennFudanDataset(data_dir, get_transform(train=False))
    img, target = dataset_test.__getitem__(0)

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    # our dataset has two classes only - background and person
    num_classes = 2

    # get the model using our helper function
    model = get_model_instance_segmentation(num_classes)

    model.load_state_dict(torch.load('trained.pth'))
    model.eval()
    outputs = model([img])
    output = outputs[0]
    print(output.keys())


if __name__ == "__main__":
    main()
