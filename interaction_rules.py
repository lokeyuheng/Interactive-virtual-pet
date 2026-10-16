"""Initial motion thresholds; tune on validation recordings."""
from collections import deque
import numpy as np


def near(point, bounds, margin=35):
    x, y, w, h = bounds
    return x-margin <= point[0] <= x+w+margin and y-margin <= point[1] <= y+h+margin


class InteractionRules:
    def __init__(self):
        self.history = deque()
        self.last = {}
        self.feed_since = None

    def emit(self, action, now):
        if now - self.last.get(action, float("-inf")) < 2:
            return None
        self.last[action] = now
        self.history.clear()
        return {"action": action, "timestamp": now}

    def motion(self, point, bounds, now):
        if point is None:
            self.history.clear()
            return None
        self.history.append((now, *point))
        while self.history and now - self.history[0][0] > 1.0:
            self.history.popleft()
        if len(self.history) < 4:
            return None
        samples = np.array(self.history)
        duration = samples[-1, 0] - samples[0, 0]
        if duration < 0.6:
            return None
        # Ignore small steps, which are commonly tracker jitter.
        anchor = samples[0, 1]
        directions = []
        for x in samples[1:, 1]:
            if abs(x - anchor) >= 12:
                directions.append(np.sign(x - anchor))
                anchor = x
        reversals = sum(a != b for a, b in zip(directions, directions[1:]))
        span = np.ptp(samples[:, 1])
        if reversals >= 3 and span >= 90:
            return self.emit("ANGRY", now)
        if (reversals >= 1 and 20 <= span <= 100
                and all(near(p[1:], bounds) for p in samples)):
            speed = np.linalg.norm(np.diff(samples[:, 1:], axis=0), axis=1).sum() / duration
            if 25 <= speed <= 220:
                return self.emit("PET", now)
        return None

    def feeding(self, frame, bounds, now):
        import cv2
        # Designated green prop; adjust HSV range for your actual prop/lighting.
        mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HSV),
                           np.array([40, 100, 70]), np.array([85, 255, 255]))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        present = False
        for contour in contours:
            if cv2.contourArea(contour) >= 500:
                x, y, w, h = cv2.boundingRect(contour)
                if near((x+w/2, y+h/2), bounds):
                    present = True
        if not present:
            self.feed_since = None
        elif self.feed_since is None:
            self.feed_since = now
        elif now - self.feed_since >= 0.4:
            return self.emit("FEED", now)
        return None
