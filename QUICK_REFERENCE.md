# FFmpeg SOM Offset - Quick Reference

## Quick Command Generator

```bash
python3 ffmpeg_som_offset.py <input> <output> <offset_seconds> --mode <mode>
```

## Most Common Commands

### ✂️ Trim/Cut from Start
```bash
# Remove first 5 seconds
python3 ffmpeg_som_offset.py input.mp4 output.mp4 5 --mode trim

# Remove first 2.5 seconds (precise)
python3 ffmpeg_som_offset.py input.mp4 output.mp4 2.5 --mode trim --codec reencode
```

### ⬛ Add Black Frames
```bash
# Add 3 seconds of black (HD)
python3 ffmpeg_som_offset.py input.mp4 output.mp4 3 --mode black

# Add 5 seconds of black (4K, 60fps)
python3 ffmpeg_som_offset.py input.mp4 output.mp4 5 --mode black --resolution 3840x2160 --fps 60
```

### 🔇 Add Silence
```bash
# Add 2 seconds of silence
python3 ffmpeg_som_offset.py input.mp3 output.mp3 2 --mode silence

# Add 1.5 seconds of silence (96kHz)
python3 ffmpeg_som_offset.py input.wav output.wav 1.5 --mode silence --sample-rate 96000
```

### 🔄 Fix Sync Issues
```bash
# Delay entire stream by 0.5 seconds
python3 ffmpeg_som_offset.py input.mp4 output.mp4 0.5 --mode timestamp

# Advance stream by 0.3 seconds
python3 ffmpeg_som_offset.py input.mp4 output.mp4 -0.3 --mode timestamp
```

## Direct FFmpeg Commands

If you prefer to run FFmpeg directly, here are the most useful commands:

### Trim from Start
```bash
# Fast (stream copy)
ffmpeg -ss 5 -i input.mp4 -c copy output.mp4

# Accurate (re-encode)
ffmpeg -i input.mp4 -ss 5 output.mp4
```

### Add Black Frames (1920x1080, 30fps, 3 seconds)
```bash
ffmpeg -f lavfi -i color=c=black:s=1920x1080:r=30:d=3 -i input.mp4 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[outv]" \
  -map "[outv]" output.mp4
```

### Add Silence (48kHz, 2 seconds)
```bash
ffmpeg -f lavfi -i anullsrc=r=48000:d=2 -i input.mp3 \
  -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1[outa]" \
  -map "[outa]" output.mp3
```

### Offset Timestamps
```bash
# Delay by 0.5 seconds
ffmpeg -itsoffset 0.5 -i input.mp4 -c copy output.mp4

# Advance by 0.5 seconds
ffmpeg -itsoffset -0.5 -i input.mp4 -c copy output.mp4
```

## When to Use Each Mode

| Scenario | Mode | Command |
|----------|------|---------|
| Remove intro/beginning | `trim` | `... 5 --mode trim` |
| Add countdown/leader | `black` | `... 5 --mode black` |
| Add audio pause at start | `silence` | `... 2 --mode silence` |
| Audio is ahead of video | `timestamp` | `... 0.5 --mode timestamp` |
| Video is ahead of audio | `timestamp` | `... -0.5 --mode timestamp` |
| Complex sync issues | `pts` | `... 1.0 --mode pts` |

## Frame-Accurate Calculations

For frame-accurate offsets, calculate: **offset = frames / fps**

| FPS | 1 frame | 5 frames | 10 frames | 30 frames |
|-----|---------|----------|-----------|-----------|
| 24 | 0.0417 | 0.2083 | 0.4167 | 1.25 |
| 25 | 0.04 | 0.2 | 0.4 | 1.2 |
| 30 | 0.0333 | 0.1667 | 0.3333 | 1.0 |
| 60 | 0.0167 | 0.0833 | 0.1667 | 0.5 |

Example:
```bash
# Trim exactly 10 frames at 30fps (0.3333 seconds)
python3 ffmpeg_som_offset.py input.mp4 output.mp4 0.3333 --mode trim --codec reencode
```

## Common Resolutions

| Name | Resolution | Usage |
|------|------------|-------|
| 4K UHD | `3840x2160` | Ultra HD |
| 1080p | `1920x1080` | Full HD (most common) |
| 720p | `1280x720` | HD |
| 480p | `854x480` | SD |
| 4K DCI | `4096x2160` | Cinema 4K |

## Sample Rates

| Rate | Usage |
|------|-------|
| `48000` | Professional video (most common) |
| `44100` | CD quality, music |
| `96000` | High-res audio |
| `192000` | Studio quality |

## Pro Tips

1. **Always check your source specs first:**
   ```bash
   ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate input.mp4
   ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate input.mp4
   ```

2. **Use stream copy when possible:**
   - Faster processing
   - No quality loss
   - Default in this tool

3. **For broadcast/professional work:**
   - Use `--codec reencode` for frame accuracy
   - Match exact resolution and frame rate
   - Use `--mode black` or `--mode silence` to add leaders

4. **For quick edits:**
   - Use `--mode trim` with default settings
   - Stream copy is usually good enough
