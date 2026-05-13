from pathlib import Path
import cv2
from ultralytics import YOLO
import deep_sort.deep_sort.deep_sort as ds
from main import extract_detections, putTextWithBackground


def run_yolo_tracking(input_video: Path, output_video: Path, detect_class: int, weight: str):
    model = YOLO(weight)
    tracker = ds.DeepSort('deep_sort/deep_sort/deep/checkpoint/ckpt.t7')

    cap = cv2.VideoCapture(str(input_video))
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter(str(output_video), fourcc, fps, (width, height), isColor=True)

    tracked_frames = 0
    unique_ids = set()

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        results = model(frame, stream=True)
        detections, confarray = extract_detections(results, detect_class)
        track_results = tracker.update(detections, confarray, frame)
        for x1, y1, x2, y2, track_id in track_results:
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            unique_ids.add(int(track_id))
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
            putTextWithBackground(frame, str(int(track_id)), (max(-10, x1), max(40, y1)), font_scale=1.2,
                                  text_color=(255, 255, 255), bg_color=(255, 0, 255))
        writer.write(frame)
        tracked_frames += 1

    writer.release()
    cap.release()

    return {
        'total_frames': total_frames,
        'tracked_frames': tracked_frames,
        'unique_ids': len(unique_ids),
        'output_video': output_video,
    }
