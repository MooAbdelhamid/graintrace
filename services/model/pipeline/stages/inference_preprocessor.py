from torchvision import transforms


def transform(image):

    transform_resize = transforms.Resize((224 * 4, 224 * 4))
    transform_normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    )

    transform_1 = transforms.Compose(
        [transform_resize, transforms.ToTensor(), transform_normalize]
    )

    return transform_1(image)
