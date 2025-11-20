import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from model import SimpleCNN

CLASSES = ["0", "1", "2", "3"]

MODEL_PATH = os.getenv("CNN_MODEL_PATH")

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

def train():
    train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    mask = train_dataset.targets < 4
    train_dataset.targets = train_dataset.targets[mask]
    train_dataset.data = train_dataset.data[mask]
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)

    model = SimpleCNN(num_classes=4)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for _ in range(5):
        for images, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    torch.save(model.state_dict(), MODEL_PATH)

if __name__ == "__main__":
    train()