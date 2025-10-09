#!/usr/bin/env python3
"""
FFmpeg SOM (Start of Material) Offset Command Generator

This script generates FFmpeg commands to offset the SOM of video/audio assets.
"""

import argparse
import sys


def generate_trim_command(input_file, output_file, offset_seconds, codec='copy'):
    """
    Generate FFmpeg command to trim from the start (negative SOM offset).
    
    Args:
        input_file: Input video/audio file
        output_file: Output file path
        offset_seconds: Number of seconds to trim from start
        codec: Codec to use ('copy' for stream copy, 'reencode' to re-encode)
    """
    if codec == 'copy':
        cmd = f'ffmpeg -ss {offset_seconds} -i "{input_file}" -c copy "{output_file}"'
    else:
        cmd = f'ffmpeg -ss {offset_seconds} -i "{input_file}" "{output_file}"'
    
    return cmd


def generate_prepend_black_command(input_file, output_file, offset_seconds, resolution='1920x1080', fps=30):
    """
    Generate FFmpeg command to add black frames at the start (positive SOM offset).
    
    Args:
        input_file: Input video file
        output_file: Output file path
        offset_seconds: Duration of black frames to add
        resolution: Video resolution (WxH)
        fps: Frame rate
    """
    width, height = resolution.split('x')
    
    cmd = (
        f'ffmpeg -f lavfi -i color=c=black:s={resolution}:r={fps}:d={offset_seconds} '
        f'-i "{input_file}" '
        f'-filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[outv]" '
        f'-map "[outv]" '
        f'"{output_file}"'
    )
    
    return cmd


def generate_prepend_silence_command(input_file, output_file, offset_seconds, sample_rate=48000):
    """
    Generate FFmpeg command to add silence at the start for audio (positive SOM offset).
    
    Args:
        input_file: Input audio file
        output_file: Output file path
        offset_seconds: Duration of silence to add
        sample_rate: Sample rate in Hz
    """
    cmd = (
        f'ffmpeg -f lavfi -i anullsrc=r={sample_rate}:d={offset_seconds} '
        f'-i "{input_file}" '
        f'-filter_complex "[0:a][1:a]concat=n=2:v=0:a=1[outa]" '
        f'-map "[outa]" '
        f'"{output_file}"'
    )
    
    return cmd


def generate_timestamp_offset_command(input_file, output_file, offset_seconds):
    """
    Generate FFmpeg command to offset timestamps (for sync adjustment).
    
    Args:
        input_file: Input file
        output_file: Output file path
        offset_seconds: Timestamp offset in seconds (can be negative)
    """
    cmd = f'ffmpeg -itsoffset {offset_seconds} -i "{input_file}" -c copy "{output_file}"'
    
    return cmd


def generate_pts_offset_command(input_file, output_file, offset_seconds):
    """
    Generate FFmpeg command to offset PTS (Presentation Timestamp).
    
    Args:
        input_file: Input file
        output_file: Output file path
        offset_seconds: PTS offset in seconds
    """
    cmd = (
        f'ffmpeg -i "{input_file}" '
        f'-vf "setpts=PTS+{offset_seconds}/TB" '
        f'-af "asetpts=PTS+{offset_seconds}/TB" '
        f'"{output_file}"'
    )
    
    return cmd


def main():
    parser = argparse.ArgumentParser(
        description='Generate FFmpeg commands to offset SOM (Start of Material) of media assets'
    )
    
    parser.add_argument('input', help='Input file path')
    parser.add_argument('output', help='Output file path')
    parser.add_argument('offset', type=float, help='Offset in seconds (positive to add content, negative to trim)')
    
    parser.add_argument('--mode', choices=['trim', 'black', 'silence', 'timestamp', 'pts'], 
                        default='trim',
                        help='Offset mode: trim (remove from start), black (add black frames), '
                             'silence (add silence), timestamp (offset timestamps), pts (offset PTS)')
    
    parser.add_argument('--resolution', default='1920x1080', 
                        help='Video resolution for black frames (default: 1920x1080)')
    parser.add_argument('--fps', type=int, default=30, 
                        help='Frame rate for black frames (default: 30)')
    parser.add_argument('--sample-rate', type=int, default=48000, 
                        help='Sample rate for silence (default: 48000)')
    parser.add_argument('--codec', choices=['copy', 'reencode'], default='copy',
                        help='Codec mode for trim: copy (stream copy) or reencode (default: copy)')
    
    parser.add_argument('--execute', action='store_true', 
                        help='Execute the command immediately (default: just print)')
    
    args = parser.parse_args()
    
    # Generate appropriate command based on mode
    if args.mode == 'trim':
        if args.offset < 0:
            print("Error: For trim mode, use positive offset value", file=sys.stderr)
            sys.exit(1)
        cmd = generate_trim_command(args.input, args.output, args.offset, args.codec)
    
    elif args.mode == 'black':
        if args.offset <= 0:
            print("Error: For black mode, use positive offset value", file=sys.stderr)
            sys.exit(1)
        cmd = generate_prepend_black_command(args.input, args.output, args.offset, 
                                            args.resolution, args.fps)
    
    elif args.mode == 'silence':
        if args.offset <= 0:
            print("Error: For silence mode, use positive offset value", file=sys.stderr)
            sys.exit(1)
        cmd = generate_prepend_silence_command(args.input, args.output, args.offset, 
                                              args.sample_rate)
    
    elif args.mode == 'timestamp':
        cmd = generate_timestamp_offset_command(args.input, args.output, args.offset)
    
    elif args.mode == 'pts':
        cmd = generate_pts_offset_command(args.input, args.output, args.offset)
    
    # Print the command
    print("\nGenerated FFmpeg command:")
    print("-" * 80)
    print(cmd)
    print("-" * 80)
    
    # Execute if requested
    if args.execute:
        import subprocess
        print("\nExecuting command...")
        result = subprocess.run(cmd, shell=True)
        sys.exit(result.returncode)
    else:
        print("\nTo execute this command, run with --execute flag or copy the command above.")


if __name__ == '__main__':
    main()
