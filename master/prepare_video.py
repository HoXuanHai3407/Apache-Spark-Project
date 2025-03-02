import cv2
import pickle

def read_video_in_batches(video_path, batch_size=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
        if len(frames) == batch_size:
            yield frames
            frames = []
    cap.release()

batches = list(read_video_in_batches('../video/video.mp4'))

with open('batches.pkl', 'wb') as f:
    pickle.dump(batches, f)

print(f"Video đã chia thành {len(batches)} batch.")
