import torch
import torch.nn as nn

class HTSModel(nn.Module):
    def __init__(self):
        super(HTSModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)

        # Fully connected layers for image features
        self.fc1 = nn.Linear(64 * 64 * 64, 128)  # Image features to 128 dimensions

        # Fully connected layers for thickness
        self.fc_thickness = nn.Linear(1, 16)  # Simple layer for thickness

        # Combined image features and thickness
        self.fc2 = nn.Linear(128 + 16, 64)  # Combine image features and thickness
        self.fc3 = nn.Linear(64, 1)  # Output critical current

    def forward(self, x, thickness):
        # CNN part: Feature extraction from the image
        x = self.pool(torch.relu(self.conv1(x)))  # Conv1 + Pooling
        x = self.pool(torch.relu(self.conv2(x)))  # Conv2 + Pooling
        
        # Flatten the CNN output
        x = x.view(x.size(0), -1)  # Flatten image features

        # Pass image features through first fully connected layer
        x = torch.relu(self.fc1(x))

        # Process thickness through a simple FC layer
        thickness = torch.relu(self.fc_thickness(thickness))  # Thickness to 16 dimensions

        # Concatenate image features with processed thickness
        combined = torch.cat((x, thickness), dim=1)

        # Pass combined features through remaining fully connected layers
        x = torch.relu(self.fc2(combined))
        x = self.fc3(x)  # Output critical current
        return x