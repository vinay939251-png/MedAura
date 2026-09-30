/**
 * Lightweight Object Tracker (Simulating ByteTrack for Web)
 * Tracks bounding boxes across frames using IoU (Intersection over Union).
 */
export class ByteTracker {
  constructor(maxLost = 30, iouThreshold = 0.3) {
    this.maxLost = maxLost;
    this.iouThreshold = iouThreshold;
    this.tracks = [];
    this.nextId = 1;
  }

  /**
   * Update tracker with new detections.
   * @param {Array} detections - [{bbox: [x,y,w,h], confidence: float}]
   * @returns {Array} - Active tracks [{id: int, bbox: [x,y,w,h], confidence: float, age: int}]
   */
  update(detections) {
    if (detections.length === 0) {
      this.tracks.forEach(track => track.lost++);
      this.tracks = this.tracks.filter(track => track.lost <= this.maxLost);
      return this.tracks;
    }

    // Very simple greedy IoU matching
    const matches = [];
    const unmatchedDetections = new Set(detections.map((_, i) => i));
    const unmatchedTracks = new Set(this.tracks.map((_, i) => i));

    for (let t = 0; t < this.tracks.length; t++) {
      let bestIoU = 0;
      let bestDetIdx = -1;

      for (let d = 0; d < detections.length; d++) {
        if (!unmatchedDetections.has(d)) continue;
        const iou = this.calculateIoU(this.tracks[t].bbox, detections[d].bbox);
        if (iou > bestIoU) {
          bestIoU = iou;
          bestDetIdx = d;
        }
      }

      if (bestIoU > this.iouThreshold) {
        matches.push({ trackIdx: t, detIdx: bestDetIdx });
        unmatchedDetections.delete(bestDetIdx);
        unmatchedTracks.delete(t);
      }
    }

    // Update matched tracks
    for (const match of matches) {
      const track = this.tracks[match.trackIdx];
      const det = detections[match.detIdx];
      track.bbox = det.bbox;
      track.confidence = det.confidence;
      track.age++;
      track.lost = 0;
    }

    // Mark unmatched tracks as lost
    for (const t of unmatchedTracks) {
      this.tracks[t].lost++;
    }

    // Remove tracks lost for too long
    this.tracks = this.tracks.filter(track => track.lost <= this.maxLost);

    // Create new tracks for unmatched detections
    for (const d of unmatchedDetections) {
      const det = detections[d];
      this.tracks.push({
        id: this.nextId++,
        bbox: det.bbox,
        confidence: det.confidence,
        age: 1,
        lost: 0
      });
    }

    return this.tracks.filter(track => track.lost === 0);
  }

  calculateIoU(boxA, boxB) {
    // box: [x, y, w, h] -> convert to [x1, y1, x2, y2]
    const a = [boxA[0], boxA[1], boxA[0] + boxA[2], boxA[1] + boxA[3]];
    const b = [boxB[0], boxB[1], boxB[0] + boxB[2], boxB[1] + boxB[3]];

    const xA = Math.max(a[0], b[0]);
    const yA = Math.max(a[1], b[1]);
    const xB = Math.min(a[2], b[2]);
    const yB = Math.min(a[3], b[3]);

    const interArea = Math.max(0, xB - xA) * Math.max(0, yB - yA);
    if (interArea === 0) return 0;

    const boxAArea = (a[2] - a[0]) * (a[3] - a[1]);
    const boxBArea = (b[2] - b[0]) * (b[3] - b[1]);

    const iou = interArea / parseFloat(boxAArea + boxBArea - interArea);
    return iou;
  }
}
