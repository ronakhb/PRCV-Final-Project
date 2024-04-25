# encoding: utf-8
from .triplet_loss import TripletLoss, CrossEntropyLabelSmooth, CrossEntropy
from .center_loss import CenterLoss



def make_loss():    
    xent = CrossEntropy()

    def loss_func(score, feat, target):      # [64, 751],  [64, 512], [64,]
        loss = xent(score, target)         # 6.618
        return loss

    return loss_func


def make_loss_with_triplet_entropy(cfg, num_classes):    
    triplet = TripletLoss(cfg.margin)  # triplet loss
    xent = CrossEntropyLabelSmooth(num_classes=num_classes)

    def loss_func(score, feat, target):      # [64, 751],  [64, 512], [64,]
        loss_x = xent(score, target)         # 6.618
        loss_t = triplet(feat, target)[0]    # 3.2403
        loss = loss_x + loss_t         # 11.1710
        return loss

    return loss_func


def make_loss_with_center(cfg, num_classes, feat_dim=2048):    
    triplet = TripletLoss(cfg.margin)  # triplet loss
    center_criterion = CenterLoss(num_classes=num_classes, feat_dim=feat_dim, use_gpu=True)  # center loss
    xent = CrossEntropyLabelSmooth(num_classes=num_classes)

    def loss_func(score, feat, target):      # [64, 751],  [64, 512], [64,]
        loss_x = xent(score, target)         # 6.618
        loss_t = triplet(feat, target)[0]    # 3.2403
        loss_c = center_criterion(feat, target)         # 2625.2329
        loss = loss_x + loss_t + cfg.center_loss_weight * loss_c         # 11.1710
        return loss

    return loss_func, center_criterion




