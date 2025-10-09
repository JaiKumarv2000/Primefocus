# FFmpeg SOM Offset Command Generator

A Python utility to generate FFmpeg commands for offsetting the SOM (Start of Material) of video and audio assets.

## What is SOM?

SOM (Start of Material) refers to the point where actual content begins in a media file. Offsetting the SOM allows you to:
- **Trim content from the beginning** (negative offset)
- **Add black frames or silence at the start** (positive offset)
- **Adjust timestamps for synchronization**

## Installation

No installation required! Just ensure you have:
- Python 3.x
- FFmpeg installed on your system

## Usage

```bash
python3 ffmpeg_som_offset.py <input> <output> <offset> [options]
```

### Basic Examples

#### 1. Trim 5 seconds from the start (remove first 5 seconds)
```bash
python3 ffmpeg_som_offset.py input.mp4 output.mp4 5 --mode trim
```

**Generated command:**
```bash
ffmpeg -ss 5 -i "input.mp4" -c copy "output.mp4"
```

#### 2. Add 3 seconds of black frames at the beginning
```bash
python3 ffmpeg_som_offset.py input.mp4 output.mp4 3 --mode black --resolution 1920x1080 --fps 30
```

**Generated command:**
```bash
ffmpeg -f lavfi -i color=c=black:s=1920x1080:r=30:d=3 -i "input.mp4" -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[outv]" -map "[outv]" "output.mp4"
```

#### 3. Add 2 seconds of silence at the beginning (audio)
```bash
python3 ffmpeg_som_offset.py input.mp3 output.mp3 2 --mode silence --sample-rate 48000
```

**Generated command:**
```bash
ffmpeg -f lavfi -i anullsrc=r=48000:d=2 -i "input.mp3" -filter_complex "[0:a][1:a]concat=n=2:v=0:a=1[outa]" -map "[outa]" "output.mp3"
```

#### 4. Offset timestamps by -1.5 seconds
```bash
python3 ffmpeg_som_offset.py input.mp4 output.mp4 -1.5 --mode timestamp
```

**Generated command:**
```bash
ffmpeg -itsoffset -1.5 -i "input.mp4" -c copy "output.mp4"
```

#### 5. Offset PTS (Presentation Timestamp)
```bash
python3 ffmpeg_som_offset.py input.mp4 output.mp4 2.5 --mode pts
```

**Generated command:**
```bash
ffmpeg -i "input.mp4" -vf "setpts=PTS+2.5/TB" -af "asetpts=PTS+2.5/TB" "output.mp4"
```

## Modes Explained

### `--mode trim` (Default)
- **Purpose:** Remove content from the start of the file
- **Offset:** Positive value (seconds to remove)
- **Use case:** Skip intro, remove unwanted beginning
- **Speed:** Fast (stream copy by default)

### `--mode black`
- **Purpose:** Add black video frames at the beginning
- **Offset:** Positive value (duration of black frames)
- **Use case:** Add leader, create intro space
- **Options:** `--resolution`, `--fps`

### `--mode silence`
- **Purpose:** Add silent audio at the beginning
- **Offset:** Positive value (duration of silence)
- **Use case:** Audio sync, add audio leader
- **Options:** `--sample-rate`

### `--mode timestamp`
- **Purpose:** Offset container timestamps
- **Offset:** Any value (positive or negative)
- **Use case:** Fix A/V sync issues
- **Speed:** Fast (stream copy)

### `--mode pts`
- **Purpose:** Offset presentation timestamps
- **Offset:** Any value (positive or negative)
- **Use case:** Advanced sync adjustment
- **Note:** Requires re-encoding

## Command Options

| Option | Description | Default |
|--------|-------------|---------|
| `--mode` | Operation mode (trim/black/silence/timestamp/pts) | `trim` |
| `--resolution` | Video resolution for black frames (WxH) | `1920x1080` |
| `--fps` | Frame rate for black frames | `30` |
| `--sample-rate` | Audio sample rate for silence | `48000` |
| `--codec` | Codec mode for trim (copy/reencode) | `copy` |
| `--execute` | Execute command immediately | `False` |

## Common Use Cases

### Scenario 1: Remove unwanted intro
```bash
# Remove first 10 seconds
python3 ffmpeg_som_offset.py video.mp4 trimmed.mp4 10 --mode trim
```

### Scenario 2: Add countdown leader
```bash
# Add 5 seconds of black frames at 24fps
python3 ffmpeg_som_offset.py main.mp4 with_leader.mp4 5 --mode black --fps 24
```

### Scenario 3: Fix audio sync (audio ahead by 0.5s)
```bash
# Delay audio by 0.5 seconds
python3 ffmpeg_som_offset.py input.mp4 synced.mp4 0.5 --mode timestamp
```

### Scenario 4: Precise frame-accurate trimming
```bash
# Trim exactly 2.5 seconds with re-encoding for accuracy
python3 ffmpeg_som_offset.py input.mp4 output.mp4 2.5 --mode trim --codec reencode
```

## Execute Commands Directly

To execute the generated command immediately instead of just printing it:

```bash
python3 ffmpeg_som_offset.py input.mp4 output.mp4 5 --mode trim --execute
```

## Tips

1. **Stream Copy vs Re-encode:**
   - Use `--codec copy` (default) for speed and lossless operation
   - Use `--codec reencode` for frame-accurate cutting

2. **Offset Values:**
   - Can use decimals: `2.5`, `0.033` (1 frame at 30fps)
   - For frame-accurate offsets: `1/fps` (e.g., 0.0333 for 30fps)

3. **Video Resolution:**
   - Match your source video resolution when adding black frames
   - Common values: `1920x1080`, `1280x720`, `3840x2160` (4K)

4. **Sample Rate:**
   - Match your source audio sample rate when adding silence
   - Common values: `48000`, `44100`, `96000`

## Troubleshooting

**Command fails with codec error:**
- Try `--codec reencode` for trim mode
- Check if FFmpeg supports your input format

**Black frames have wrong aspect ratio:**
- Specify correct `--resolution` matching your video

**Audio sync issues after offset:**
- Try `--mode pts` instead of `--mode timestamp`
- Consider re-encoding with `--codec reencode`

## Examples by File Type

### Video Files (MP4, MOV, AVI)
```bash
# Trim
python3 ffmpeg_som_offset.py video.mp4 out.mp4 3 --mode trim

# Add black frames
python3 ffmpeg_som_offset.py video.mp4 out.mp4 2 --mode black
```

### Audio Files (MP3, WAV, AAC)
```bash
# Trim
python3 ffmpeg_som_offset.py audio.mp3 out.mp3 1.5 --mode trim

# Add silence
python3 ffmpeg_som_offset.py audio.mp3 out.mp3 1.5 --mode silence
```

### High-Resolution Video
```bash
# 4K video with black frames
python3 ffmpeg_som_offset.py 4k_video.mp4 out.mp4 5 --mode black --resolution 3840x2160 --fps 60
```

## License

Free to use and modify as needed.
