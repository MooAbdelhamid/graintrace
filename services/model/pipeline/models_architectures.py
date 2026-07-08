# ========================================
# PyTorch Core
# ========================================
import torch
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


class DINOv2EmbeddingModel(nn.Module):
    def __init__(
        self,
        embedding_dim=256,
        model_name="dinov2_vits14",
        pretrained=True,
        unfreeze_last_backbone_layer=True,
    ):
        super().__init__()

        # Load DINOv2 backbone from torch hub
        # Options:
        # dinov2_vits14  -> small, lighter
        # dinov2_vitb14  -> bigger
        # dinov2_vitl14  -> large, heavy
        # dinov2_vitg14  -> giant, very heavy
        self.backbone = torch.hub.load(
            "facebookresearch/dinov2", model_name, pretrained=pretrained
        )

        # DINOv2 embedding dimension depends on model size
        if model_name == "dinov2_vits14":
            in_features = 384
        elif model_name == "dinov2_vitb14":
            in_features = 768
        elif model_name == "dinov2_vitl14":
            in_features = 1024
        elif model_name == "dinov2_vitg14":
            in_features = 1536
        else:
            raise ValueError(f"Unknown DINOv2 model name: {model_name}")

        # Freeze the entire backbone first
        for param in self.backbone.parameters():
            param.requires_grad = False

        # Unfreeze only the last transformer block
        if unfreeze_last_backbone_layer:
            for param in self.backbone.blocks[-2].parameters():
                param.requires_grad = True

            # Also unfreeze final norm layer
            for param in self.backbone.norm.parameters():
                param.requires_grad = True

        # Projection head for metric learning
        self.embedding_head = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.LayerNorm(512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, embedding_dim),
        )

    def forward(self, x):
        """
        x shape: (B, 3, H, W)
        output shape: (B, embedding_dim)
        """

        # DINOv2 returns image-level CLS embedding
        features = self.backbone(x)

        embeddings = self.embedding_head(features)

        # L2-normalized embeddings for triplet/contrastive loss
        embeddings = F.normalize(embeddings, p=2, dim=1)

        return embeddings
