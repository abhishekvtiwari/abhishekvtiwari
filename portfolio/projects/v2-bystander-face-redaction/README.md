# V2 · Bystander Face Redaction

> Blur the faces in photos and videos before you share them.

![Bystander Face Redaction](../../images/v2-bystander-face-redaction.jpg)
<sub>Photo: New York Giants, 1913, Bain News Service, Library of Congress, via Wikimedia Commons (public domain); faces blurred by the project's face_redact.py.</sub>

## What I built

I built a Python and OpenCV tool that finds every face it can in photos, folders, videos or a webcam and blurs it before anything is shared. The brief was a school that posts event photos, where some parents do not want their family online. It writes blurred copies and never changes the originals.

A tool using the YuNet face detector finds faces in photos, videos or a webcam and blurs them, with a margin so nothing stays readable. The practice video is a pan across a still photo, so real moving people are not tested. It detects faces; it never identifies anyone.

## Tools

`Python` · `OpenCV` · `YuNet` · `Jupyter`

## Skills shown

- Face detection with OpenCV and YuNet
- Blurring regions safely
- Thresholds and measuring misses
- Processing photos and video

## Data

- Bain News Service, Library of Congress, via Wikimedia Commons (public domain)
- Made by Compounza from the 1911 photo (public domain)

## Interview questions this project answers

<details>
<summary><b>What data did you use, and what are the licences?</b></summary>

I used 3 public-domain photographs from the Library of Congress, Bain News Service, 1908 to 1913, via Wikimedia Commons, so no living person appears in the project. The test video was made by panning across one of them. The face detector is YuNet from the OpenCV model zoo, under the MIT licence, and its licence file ships with it.
</details>

<details>
<summary><b>How does the tool work?</b></summary>

YuNet looks at the picture and returns a box for each face it is sure enough about, at a default threshold of 0.6. I widen each box by a quarter on every side to cover hair, ears and chin, then apply a Gaussian blur whose size grows with the face, so even a large face is unreadable. The blurred copy is saved in a separate folder.
</details>

<details>
<summary><b>How does it handle video?</b></summary>

A video is just a series of pictures, so I read one frame, find the faces, blur them and write the frame to a new video, then repeat. On my test video it processed 120 frames, with up to 9 faces blurred in a single frame. Faces looking at the camera were blurred well; faces in profile or looking up were often missed.
</details>

---

**The full project** (step-by-step guide, data, notebook, the finished solution and all ten interview questions) is on [compounza.in](https://compounza.in/projects/v2-bystander-face-redaction).

[← All projects](../../README.md)
