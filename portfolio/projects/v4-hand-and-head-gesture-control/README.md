# V4 · Hand and Head Gesture Control

> Run a timer, turn slides and pause music with your hands and head, through a webcam.

![Hand and Head Gesture Control](../../images/v4-hand-and-head-gesture-control.jpg)
<sub>Video: "Finger-counting in Dutch" by S. Perquin, CC BY-SA 4.0, via Wikimedia Commons; hand points and readings drawn by the project's gesture_control.py. This picture is CC BY-SA 4.0.</sub>

## What I built

It lets you control a computer with your hands and head through an ordinary webcam. Hold up one to five fingers and it offers a timer of that many minutes; nod to start it, shake your head to say no, and a fist cancels it. A swipe turns slides and a thumbs up plays or pauses music. The brief was a teacher who presents and wants to run a timer and move slides without walking back to the laptop.

A swipe turns slides and a thumbs up plays or pauses music. Runs on any laptop with a webcam.

## Tools

`Python` · `MediaPipe` · `OpenCV` · `Jupyter`

## Skills shown

- Hand and face landmarks with MediaPipe
- Rule-based gestures from angles
- Testing on people you did not tune on
- A small state machine for actions

## Data

- Measured from HaGRID photos (SberDevices) via the hagrid-sample-30k-384p sample (HaGRID licence (a CC BY-SA 4.0 variant))
- "Woman counting on fingers" by Mvolz, Wikimedia Commons (CC0)
- "Finger-counting in Dutch" by S. Perquin, Wikimedia Commons (CC BY-SA 4.0)
- "Head Shake" by NMu11er, Wikimedia Commons (CC BY-SA 4.0)

## Interview questions this project answers

<details>
<summary><b>How does it see your hand and face?</b></summary>

Google’s MediaPipe finds 21 points on a hand and 478 on a face in every frame, on the computer itself, with models that ship with the project under the Apache 2.0 licence. Everything after that is my own logic on those points: which fingers are up, how long a gesture is held, whether the wrist swept sideways, and how the head is turned and tilted.
</details>

<details>
<summary><b>How do you decide that a finger is up?</b></summary>

A finger is up when its joints lie close to a straight line: the two top bends together come to less than 60 degrees. The thumb also has to point away from the hand, or a thumb tucked against the palm would count. Angles do not change with the hand’s size or distance from the camera, which is why I used them rather than pixel distances.
</details>

<details>
<summary><b>How did you check that the finger counting is right?</b></summary>

On HaGRID, a public set of labelled gesture photos. I measured the hand points in 3,000 photos, tuned the three thresholds on half of the people, and tested only on the other half, people the thresholds had never seen. It read 1210 of 1369 test photos right, 88%. Splitting by person matters: testing on the same people you tuned on flatters the result.
</details>

---

**The full project** (step-by-step guide, data, notebook, the finished solution and all ten interview questions) is on [compounza.in](https://compounza.in/projects/v4-hand-and-head-gesture-control).

[← All projects](../../README.md)
