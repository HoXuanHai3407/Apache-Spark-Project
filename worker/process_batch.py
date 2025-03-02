import sys
import cv2
import pickle
from ultralytics import YOLO
from tracker.tracker import Tracker

batch_id = int(sys.argv[1])

with open('../master/batches.pkl', 'rb') as f:
    batches = pickle.load(f)

frames = batches[batch_id]

yolo = YOLO('yolov8n.pt')
tracker = Tracker()

h, w, _ = frames[0].shape
out = cv2.VideoWriter(f'../video/output/output_chunk_{batch_id}.mp4',
                      cv2.VideoWriter_fourcc(*'mp4v'), 30, (w, h))

for frame in frames:
    results = yolo(frame)
    detections = []
    for r in results[0].boxes:
        x1, y1, x2, y2, conf, cls = map(float, r.xyxy[0].tolist() + [r.conf[0], r.cls[0]])
        detections.append(([x1, y1, x2, y2], conf, int(cls)))

    tracks = tracker.update_tracks(detections, frame)

    for track in tracks:
        if track.is_confirmed():
            x1, y1, x2, y2 = map(int, track.to_tlbr())
            track_id = track.track_id
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'ID:{track_id}', (x1, y1-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    out.write(frame)

out.release()
