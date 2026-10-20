# Camera Integration

## Contents
- [Cameras and their roles](#cameras-and-their-roles)
- [ROS 2 camera pipeline](#ros-2-camera-pipeline)
- [Stable device naming](#stable-device-naming)
- [Gripper camera: gamma and white balance](#gripper-camera-gamma-and-white-balance)
- [Femto Bolt: finding the colour node](#femto-bolt-finding-the-colour-node)
- [Verification](#verification)
- [How the images are used](#how-the-images-are-used)

## Cameras and their roles

| | Scene camera | Gripper camera |
|---|---|---|
| Device | Orbbec Femto Bolt (F00364-152) | USB UVC camera ("HZ") |
| Mount | Fixed, overlooking the workspace | On the gripper, looking at the jaws and the table |
| Stream | Colour, 1280×720 | Colour, 640×480 |
| ROS topic | `/camera/color/image_raw/compressed` | `/gripper_camera/color/image_raw/compressed` |
| Dataset key | `observation.images.global` | `observation.images.gripper` |
| Information it gives the policy | Where the cube and tray are; where the arm is | Fine alignment of the jaws with the cube during the grasp |

The two views are complementary. The scene camera localizes the cube coarsely; the gripper camera is what makes the final approach and grasp observable. A related public SO-101 dataset reports that a front-camera-only policy missed grasps by 1–2 cm, an error the front camera could not see ([Dillonjohnson/pick_place_v2](https://huggingface.co/datasets/Dillonjohnson/pick_place_v2) dataset card). That is independent evidence for keeping a wrist or gripper view.

## ROS 2 camera pipeline

Both cameras are published by the ROS 2 [`v4l2_camera`](https://index.ros.org/p/v4l2_camera/) driver, launched by `~/start_cameras.sh`. The rewritten script:

1. Resolves each camera by a **stable path** (`/dev/v4l/by-id/...` or `/dev/v4l/by-path/...`) instead of `/dev/videoN`.
2. Checks that each device exists before launching, and fails loudly if not.
3. Launches the gripper camera with `gamma:=100`.
4. Uses `find_femto.sh` to select the Femto Bolt's colour node.

> The script source is not included in this repository yet (see [VERIFICATION_STATUS](../VERIFICATION_STATUS.md#missing-files-you-should-add)). The commands below show the equivalent manual steps.

```bash
# [CONTAINER] equivalent manual launch of the gripper camera (illustrative)
ros2 run v4l2_camera v4l2_camera_node --ros-args \
  -r __ns:=/gripper_camera \
  -p video_device:=/dev/v4l/by-id/<gripper-camera-id>-video-index0 \
  -p image_size:="[640,480]" \
  -p gamma:=100
```

The exact remappings that produce `/gripper_camera/color/image_raw` depend on the script. Check them with `ros2 topic list` after launch.

## Stable device naming

`/dev/videoN` numbers are assigned in enumeration order, so they change whenever a camera is replugged or the PC reboots. This swapped the two cameras at least once. Use:

```bash
# [HOST] stable names
ls -l /dev/v4l/by-id/ /dev/v4l/by-path/
# What formats does each node offer?
v4l2-ctl --list-devices
v4l2-ctl -d /dev/video0 --list-formats-ext
```

A UVC camera usually exposes **two** `/dev/video*` nodes: one for images, and one for metadata. Only the first (`...-video-index0`) streams frames.

## Gripper camera: gamma and white balance

**Gamma crash.** The camera reports a default gamma of 300, but its own valid range is 90–150. `v4l2_camera` tries to apply the default and crashes. The fix is to always pass `gamma:=100`.

```bash
# [HOST] inspect the control ranges yourself
v4l2-ctl -d /dev/v4l/by-id/<gripper-camera-id>-video-index0 --list-ctrls
```

**White balance (open issue).** The camera's automatic white balance makes the image colour shift with lighting and with what is in view. During inference attempt 3, the gripper image looked different from the training images, which is one of the suspected causes of the failed grasp. Recommended:

```bash
# [HOST] lock white balance (control names vary by camera; check --list-ctrls first)
v4l2-ctl -d <device> --set-ctrl=white_balance_automatic=0
v4l2-ctl -d <device> --set-ctrl=white_balance_temperature=4600
```

Apply the **same fixed values** when recording new data and when running inference. Older kernels name these controls `white_balance_temperature_auto`.

## Femto Bolt: finding the colour node

The Femto Bolt exposes several V4L2 nodes, including a depth node that streams `Y16` (16-bit greyscale). Opening that node with a colour pipeline crashed with an encoding error. The Femto Bolt also tended to come back on a different USB port after reconnecting.

`find_femto.sh` solves both problems by scanning the Femto Bolt's nodes and choosing the one that offers **YUYV** video. A minimal equivalent:

```bash
# [HOST] print the Femto Bolt node that offers YUYV
for d in /dev/video*; do
  if v4l2-ctl -d "$d" --info 2>/dev/null | grep -qi "femto" && \
     v4l2-ctl -d "$d" --list-formats 2>/dev/null | grep -q "YUYV"; then
    echo "$d"
  fi
done
```

"Femto Bolt not detected" turned out to be a physical problem: the camera was disconnected or under-powered. It works on a USB 3 port with its own power supply.

## Verification

```bash
# [CONTAINER]
ros2 topic list | grep -E "camera|gripper"
ros2 topic hz /camera/color/image_raw/compressed          # expect ~30 Hz
ros2 topic hz /gripper_camera/color/image_raw/compressed  # expect ~30 Hz
```

Verified status: both cameras stream at 30 Hz. In the 21-episode validation dataset, both camera views were checked in the dataset viewer and were not swapped.

## How the images are used

| Stage | Processing |
|-------|-----------|
| Recording | Compressed images are decoded and written to MP4 (libx264, yuv420p) at their native resolution |
| Training (Run 1) | Frames decoded with `pyav`, resized **with padding** to 512×512 (`resize_imgs_with_padding: [512, 512]`), no colour augmentation (`image_transforms.enable: false`) |
| Training (Run 2) | Renamed to `camera1` (global) and `camera2` (gripper); one empty camera slot added |
| Inference | The same topics feed the policy; resolution, naming, colour settings and camera placement must match training |

Because colour augmentation was off in Run 1, the model never saw brightness, contrast or hue variation during training. That makes it more sensitive to white-balance drift. Enabling `dataset.image_transforms.enable=true` is a cheap experiment for the next training run ([LeRobot dataset docs](https://huggingface.co/docs/lerobot/lerobot-dataset-v3)).
