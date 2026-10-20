# Vision-Based Manipulation and Multimodal Observations

## Contents
- [Introduction](#introduction)
- [Why it matters here](#why-it-matters-here)
- [What each observation contributes](#what-each-observation-contributes)
- [Fixed vs wrist-mounted cameras](#fixed-vs-wrist-mounted-cameras)
- [Image pre-processing in SmolVLA](#image-pre-processing-in-smolvla)
- [Camera calibration and coordinate frames](#camera-calibration-and-coordinate-frames)
- [Visual distribution shift](#visual-distribution-shift)
- [Connection to this project](#connection-to-this-project)
- [Lessons](#lessons)
- [Further reading](#further-reading)

## Introduction

**Vision-based manipulation** uses camera images, rather than known object poses, to decide how to move. End-to-end visuomotor policies map pixels (plus proprioception) directly to motor commands, an approach popularized for real robots by Levine et al. (2016), who trained deep visuomotor policies end to end ([references](../research/references.bib)).

## Why it matters here

The policy never receives the cube's coordinates. It must infer where the cube is, whether the jaws are aligned, and whether the grasp succeeded, entirely from two RGB images and six joint values.

## What each observation contributes

| Input | Shape | Provides | Weakness |
|-------|-------|----------|----------|
| Scene camera (`global`) | 720×1280×3 | Cube and tray location; arm configuration in context | Small objects occupy few pixels after resizing to 512×512 |
| Gripper camera (`gripper`) | 480×640×3 | Close-up alignment of jaws and cube; grasp confirmation | Field of view changes as the arm moves; sensitive to colour settings |
| Joint state | 6 | Exact arm configuration; gripper opening | Says nothing about the object |
| Instruction | text | Task goal | Constant in this project |

These are **multimodal observations**: different sensors with different units, rates and noise. SmolVLA handles them by projecting each into a common token space (images through the vision encoder, state through a linear layer, text through the tokenizer) and processing them jointly ([SmolVLA architecture](smolvla-architecture.md)).

## Fixed vs wrist-mounted cameras

| | Fixed (third-person) | Wrist / gripper |
|---|---|---|
| Viewpoint | Constant | Moves with the end effector |
| Best for | Global localization, transport, placement | Final approach, grasp alignment, contact |
| Typical failure without it | Cannot find objects outside the wrist view | Misses grasps by a few cm that the fixed view cannot resolve |

The SmolVLA authors standardized community data into top, wrist and side camera slots for pretraining. A public SO-101 dataset card reports that a front-camera-only policy missed grasps by 1–2 cm and motivated adding a wrist camera (dataset card, not a peer-reviewed result). This project already records both views.

## Image pre-processing in SmolVLA

From the verified Run 1 configuration:

1. **Resize with padding** to 512×512. The 1280×720 scene image is scaled to 512×288, then padded. The cube therefore shrinks by a factor of 2.5 in each dimension.
2. **No tiling, global image only**, with pixel shuffle limiting each frame to **64 visual tokens** (paper, §3.1).
3. **Normalization:** images use IDENTITY normalization in the policy config (pixel scaling is handled inside the model); state and action use mean/std.

**Interpretation:** at 64 tokens for a padded 512×512 image, fine geometric detail in the scene view is limited, which is one reason the gripper view is important for the grasp.

## Camera calibration and coordinate frames

Classical pipelines need two kinds of calibration:

- **Intrinsic calibration**: focal lengths, principal point and lens distortion, usually estimated by photographing a checkerboard from several angles ([Zhang, 2000](../research/references.bib)).
- **Extrinsic (hand–eye) calibration**: the rigid transform between the camera frame and the robot base (fixed camera) or the end effector (wrist camera).

With these, a pixel and a depth value can be mapped to a 3-D point in the robot base frame, and a grasp can be planned by inverse kinematics.

```mermaid
flowchart LR
    PX["Pixel (u, v) + depth"] -- "intrinsics K" --> CAM["Point in camera frame"]
    CAM -- "extrinsics T_base_cam" --> BASE["Point in robot base frame"]
    BASE -- "inverse kinematics" --> Q["Joint angles"]
```

**End-to-end policies skip all of this.** The network learns the mapping from images to joint targets implicitly, for the specific camera placement it was trained on. That has two practical consequences in this project:

1. **No calibration was needed** for the cameras, which saved effort.
2. **Camera placement becomes part of the model.** Moving or rotating a camera after training is equivalent to changing the calibration, and the policy has no way to adapt. Camera mounts must be rigid and unchanged.

The Femto Bolt also provides depth, which this project does not use.

## Visual distribution shift

| Shift | Example here | Mitigation |
|-------|-------------|------------|
| Colour / white balance | Gripper camera auto WB | Lock camera controls; colour augmentation in training |
| Distractors | Extra red cubes on the table | Clean scene; or collect data with distractors |
| Lighting | Different time of day | Consistent lighting; brightness augmentation |
| Viewpoint | Bumped camera mount | Rigid mounts; mark positions |
| Background | New objects in view | Keep the workspace consistent |

## Connection to this project

Attempt 3's failure coincided with two visual shifts (distractor cubes, different gripper-camera colour). Run 1 trained **without** image augmentation (`image_transforms.enable: false`). LeRobot supports ColorJitter and SharpnessJitter augmentations at training time ([LeRobot dataset docs](https://huggingface.co/docs/lerobot/lerobot-dataset-v3)).

## Lessons

1. Lock every automatic camera control (exposure, white balance, focus) before recording, and use the same values at inference.
2. Treat camera mounts as part of the model.
3. Keep a wrist or gripper view for any task that needs grasp precision.

## Further reading

- Levine, S., Finn, C., Darrell, T., Abbeel, P. (2016). *End-to-End Training of Deep Visuomotor Policies.* JMLR 17. arXiv:1504.00702.
- Zhang, Z. (2000). *A Flexible New Technique for Camera Calibration.* IEEE TPAMI 22(11). DOI 10.1109/34.888718.
- Shukor, M. et al. (2025). SmolVLA, §3.1 (visual token reduction) and §3.2 (camera viewpoint normalization).
