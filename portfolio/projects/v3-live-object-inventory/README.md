# V3 · Live Object Inventory

> Point a camera at a room or a road: it names and counts the objects it sees.

![Live Object Inventory](../../images/v3-live-object-inventory.jpg)
<sub>Photo: "Seats and Table in Ton Sushi 20100808a.jpg" by 玄史生, CC0, via Wikimedia Commons; boxes and names drawn by the project’s object_inventory.py.</sub>

## What I built

I built a tool that names and counts everyday objects in photos, a video or a webcam, using a pre-trained detector that knows the 80 kinds of object in the COCO dataset, and writes the counts to a CSV file. The brief was a café owner who wants a quick count of chairs, cups and bottles at closing time, and an honest answer on how far to trust it.

A pre-trained PyTorch detector names and counts 80 kinds of everyday objects in photos, video or a webcam, and writes the counts to a CSV file. On a laptop CPU the same detector takes about a second a frame (measured in V4), so it suits photos and recorded video best.

## Tools

`Python` · `PyTorch` · `torchvision` · `OpenCV` · `Jupyter`

## Skills shown

- Object detection with PyTorch and torchvision
- Non-maximum suppression and IoU
- Measuring a pre-trained model on your own scene
- Turning detections into counts

## Data

- Five photographers, via Wikimedia Commons; each named in data/DATA-SOURCES.txt (CC0)
- "Motorway A40 - on bridge above the traffic" by Kathinka Engels, Wikimedia Commons (CC BY 3.0)

## Interview questions this project answers

<details>
<summary><b>What data did you use, and what are the licences?</b></summary>

I used 5 real photographs from Wikimedia Commons, all CC0, with no one's face in them, and a motorway video by Kathinka Engels under CC BY 3.0, whose credit line I keep. The detector is torchvision's Faster R-CNN, BSD-licensed code; its weights are downloaded from PyTorch on the first run and not shipped, and PyTorch notes they may carry terms from their COCO training data.
</details>

<details>
<summary><b>How does the detector turn a photo into a count?</b></summary>

Faster R-CNN with a MobileNetV3 backbone returns boxes, each with a label and a confidence score, and I keep only those scoring at least 0.5. Then non-maximum suppression, done separately for each kind, merges boxes that overlap by more than 0.5 so each object is counted once. Finally I count the boxes of each kind and write one row per photo and kind.
</details>

<details>
<summary><b>How did you measure it, and how good was it?</b></summary>

I counted by eye only the kinds whose number is clear in each photo, and left out books, bowls and jars because even by eye their count was unclear. Out of 12 checks it was right on 6. It counted 6 of 6 chairs and 6 of 6 cups in the sushi photo correctly, and it was right on these kinds: chair, cup, laptop, potted plant, spoon.
</details>

---

**The full project** (step-by-step guide, data, notebook, the finished solution and all ten interview questions) is on [compounza.in](https://compounza.in/projects/v3-live-object-inventory).

[← All projects](../../README.md)
