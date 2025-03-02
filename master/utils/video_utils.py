def merge_videos(chunks, output_file):
    with open('file_list.txt', 'w') as f:
        for chunk in chunks:
            f.write(f"file '{chunk}'\n")
    os.system(f'ffmpeg -f concat -safe 0 -i file_list.txt -c copy {output_file}')
