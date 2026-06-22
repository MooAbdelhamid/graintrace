# ========================================
# PyTorch Core
# ========================================
import torch.nn as nn
import torch.nn.functional as F

# ========================================
# TorchVision
# ========================================
from torchvision import models


class ConResNet50(nn.Module):
    def __init__(self, projection_dim=256, freeze_backbone=True):
        super().__init__()

        self.encoder = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)

        # Remove classification head
        feature_dim = self.encoder.fc.in_features  # 2048
        self.encoder.fc = nn.Identity()

        if freeze_backbone:
            # freeze everything first
            for param in self.encoder.parameters():
                param.requires_grad = False

            # unfreeze layer3
            for param in self.encoder.layer3.parameters():
                param.requires_grad = True

            # unfreeze layer4
            for param in self.encoder.layer4.parameters():
                param.requires_grad = True

        self.projector = nn.Sequential(
            nn.Linear(feature_dim, 1024),
            nn.LayerNorm(1024),
            nn.GELU(),
            nn.Dropout(0.2),
            nn.Linear(1024, projection_dim, bias=False),
        )

    def forward(self, x):
        # Backbone feature extraction
        x = self.encoder(x)  # [B, 2048]

        # Projection head
        x = self.projector(x)  # [B, projection_dim]

        # Normalize for contrastive learning
        x = F.normalize(x, dim=1)

        return x
