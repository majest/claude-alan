# The AI toolbox

Ways to put AI into a project here. Everything on this page runs **inside the
player's own browser** — no server, no account, no key, no cost, and nothing
anyone types or says ever leaves their computer.

Pick from this list rather than inventing something. These were all tested on
12 September 2026; the sizes and times are measured, not guessed.

| What it does | Size | Ready in | How |
| --- | --- | --- | --- |
| [Hear what someone says](#hear-what-someone-says) | 0 MB | instant | built into the browser |
| [Say something out loud](#say-something-out-loud) | 0 MB | instant | built into the browser |
| [Follow hands](#follow-hands) | 7.4 MB | ~0.6 s | MediaPipe |
| [Spot a gesture](#spot-a-gesture) | 7.9 MB | ~0.3 s | MediaPipe |
| [Follow the whole body](#follow-the-whole-body) | 5.5 MB | ~0.6 s | MediaPipe |
| [Follow a face](#follow-a-face) | 3.5 MB | ~0.5 s | MediaPipe |
| [Cut the person out](#cut-the-person-out) | 0.2 MB | ~0.3 s | MediaPipe |
| [Work out a mood from writing](#work-out-a-mood-from-writing) | 64 MB | ~3 s | Transformers.js |
| [Say what is in a picture](#say-what-is-in-a-picture) | 84 MB | ~4 s | Transformers.js |
| [Make up words](#make-up-words) | 81 MB | ~4 s | Transformers.js |

**Start at the top of that table.** The first seven are small and fast. The last
three are heavy — a 64 MB download is a long wait on a phone.

---

## The one rule this changes

The project rules say nothing may be fetched from the internet except Google
Fonts. **AI models are the exception**, because a model cannot be written by
hand and cannot live inside `index.html`.

Only these are allowed, and only with the version pinned:

```
https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.7.6
https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.0.1
https://huggingface.co/...          (model files)
https://storage.googleapis.com/mediapipe-models/...
```

Nothing else. No other CDN, no other library, no API that needs a key.

---

## Things that are true of all of them

- **The first load downloads the model.** After that the browser keeps it, so
  it is quick next time. The first time is the slow time.
- **Always show that it is loading.** A page that sits still for four seconds
  looks broken. Say "waking up…" and show it.
- **The camera and microphone need permission.** The player gets asked. They
  can say no — the project has to still work if they do.
- **Camera and microphone only work on `https://` or `localhost`.** The website
  is `https://`, so it works there. Opening `index.html` by double-clicking it
  gives `file://`, where they do **not** work. Test those bits by running:
  ```sh
  python3 -m http.server 8000
  ```
  and opening `http://localhost:8000`.
- **It needs the internet the first time.** Say so if a project depends on it.

---

## Hear what someone says

Free, instant, no download. The browser does it.

```html
<button id="talk">Say something</button>
<p id="heard"></p>

<script>
const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!Rec) {
  document.getElementById('heard').textContent =
    "This browser can't listen. Try Chrome.";
} else {
  const rec = new Rec();
  rec.lang = 'en-GB';
  rec.continuous = false;

  rec.onresult = (e) => {
    const words = e.results[0][0].transcript;
    document.getElementById('heard').textContent = words;
    // do something with `words` here
  };
  rec.onerror = (e) => {
    document.getElementById('heard').textContent = "Didn't catch that.";
  };

  document.getElementById('talk').onclick = () => rec.start();
}
</script>
```

Good for: saying a spell out loud to cast it, answering a quiz by speaking,
telling a character where to go.

---

## Say something out loud

Also free and instant.

```js
function say(text) {
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'en-GB';
  u.rate = 1;      // 0.5 slow, 2 fast
  u.pitch = 1;     // 0 deep, 2 squeaky
  speechSynthesis.speak(u);
}

say("You found the treasure!");
```

A squeaky voice for a small creature, a slow deep one for a giant. Changing
`pitch` and `rate` is the cheapest character work there is.

**Careful:** voices load late. If you want a specific voice, wait for
`speechSynthesis.onvoiceschanged` before picking one.

---

## Follow hands

21 points on each hand, up to two hands, straight from the camera. 7.4 MB.

```html
<video id="cam" autoplay playsinline muted></video>
<canvas id="paper"></canvas>

<script type="module">
import { FilesetResolver, HandLandmarker }
  from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.0.1";

const files = await FilesetResolver.forVisionTasks(
  "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.0.1/wasm");

const hands = await HandLandmarker.createFromOptions(files, {
  baseOptions: {
    modelAssetPath: "https://storage.googleapis.com/mediapipe-models/" +
      "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
    delegate: "GPU",
  },
  runningMode: "VIDEO",
  numHands: 2,
});

const cam = document.getElementById('cam');
cam.srcObject = await navigator.mediaDevices.getUserMedia({ video: true });
await cam.play();

function frame() {
  const result = hands.detectForVideo(cam, performance.now());
  for (const hand of result.landmarks) {
    const tip = hand[8];          // 8 is the tip of the index finger
    // tip.x and tip.y are 0 to 1 across the picture
    // tip.z is how near the camera it is
  }
  requestAnimationFrame(frame);
}
frame();
</script>
```

The 21 points are numbered. The useful ones: **4** thumb tip, **8** index
finger tip, **12** middle, **16** ring, **20** little finger, **0** wrist.

Good for: drawing in the air, steering, pinching to grab a thing, a hand that
moves a puppet on screen.

---

## Spot a gesture

Same as above but it names the gesture for you. 7.9 MB.

```js
import { FilesetResolver, GestureRecognizer }
  from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.0.1";

const files = await FilesetResolver.forVisionTasks(
  "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.0.1/wasm");

const gestures = await GestureRecognizer.createFromOptions(files, {
  baseOptions: {
    modelAssetPath: "https://storage.googleapis.com/mediapipe-models/" +
      "gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
    delegate: "GPU",
  },
  runningMode: "VIDEO",
});

// in your frame loop:
const r = gestures.recognizeForVideo(cam, performance.now());
const name = r.gestures?.[0]?.[0]?.categoryName;   // e.g. "Thumb_Up"
```

It knows: `Closed_Fist`, `Open_Palm`, `Pointing_Up`, `Thumb_Down`, `Thumb_Up`,
`Victory`, `ILoveYou`, and `None`.

Good for: thumbs up to say yes, an open palm to stop, a fist to punch.

---

## Follow the whole body

33 points — shoulders, elbows, hips, knees. 5.5 MB. Swap `HandLandmarker` for
`PoseLandmarker` and use this model:

```
https://storage.googleapis.com/mediapipe-models/pose_landmarker/
pose_landmarker_lite/float16/1/pose_landmarker_lite.task
```

Good for: jump to make the character jump, wave to fly, copy-the-dance.

---

## Follow a face

478 points, and it reports expressions as numbers too. 3.5 MB. Use
`FaceLandmarker` with:

```
https://storage.googleapis.com/mediapipe-models/face_landmarker/
face_landmarker/float16/1/face_landmarker.task
```

Set `outputFaceBlendshapes: true` and you get values for things like
`mouthSmileLeft` and `eyeBlinkRight`, each 0 to 1.

Good for: smile to make the sun come out, blink to shoot, a face that copies
yours.

---

## Cut the person out

Separates a person from their background. Only 0.2 MB — the smallest useful
model here. Use `ImageSegmenter` with:

```
https://storage.googleapis.com/mediapipe-models/image_segmenter/
selfie_segmenter/float16/1/selfie_segmenter.tflite
```

Good for: putting yourself inside the game, a green-screen effect with no
green screen.

---

## Work out a mood from writing

Tells you whether something sounds happy or sad. 64 MB — a real wait.

```js
import { pipeline }
  from "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.7.6";

const mood = await pipeline('sentiment-analysis',
  'Xenova/distilbert-base-uncased-finetuned-sst-2-english');

const out = await mood("I love making games!");
// [{ label: "POSITIVE", score: 0.9997 }]
```

Measured: about 3 seconds to load, then **56 ms** per answer. So the wait is
all at the start.

Good for: a creature whose face changes with how you talk to it, sorting
friendly messages from grumpy ones.

---

## Say what is in a picture

Names what is in a photo or a drawing. 84 MB.

```js
const eyes = await pipeline('image-classification', 'Xenova/vit-base-patch16-224');
const guess = await eyes(someImageElement);
// [{ label: "golden retriever", score: 0.87 }, ...]
```

Good for: "draw a cat and I'll guess what it is", a scavenger hunt where you
photograph things.

---

## Make up words

Writes a few words on from what you give it. 81 MB.

```js
const writer = await pipeline('text-generation', 'Xenova/distilgpt2');
const out = await writer("The dragon opened the door and", { max_new_tokens: 20 });
```

**Be honest about this one.** A small model like this rambles and repeats. It
is fun for silly names and daft sentences. It is not good at writing a story,
and pretending otherwise sets a child up to be disappointed.

For anything that has to read *well*, make the words ahead of time on the
computer at home and save them in a `.json` file — see `CLAUDE.md`.

---

## Making it faster

For the three big ones, add `{ device: 'webgpu' }` and modern browsers use the
graphics card:

```js
const mood = await pipeline('sentiment-analysis', 'Xenova/...', { device: 'webgpu' });
```

Tested and working. If a browser has no WebGPU it falls back on its own, so
this is safe to leave in.

---

## Showing the wait properly

Every big model should show progress. Transformers.js will tell you:

```js
const mood = await pipeline('sentiment-analysis', 'Xenova/...', {
  progress_callback: (p) => {
    if (p.status === 'progress') {
      bar.style.width = Math.round(p.progress) + '%';
    }
  },
});
```

Put something on screen to look at while it loads. A wobbling character beats
a progress bar, and both beat a frozen page.

---

## Choosing

- **Camera or microphone?** Use the top of the table. Small, fast, brilliant.
- **Does it need the internet on first run?** Everything here does, except
  speech in and speech out.
- **Does it have to read well?** Don't use `make up words`. Make the words
  ahead of time.
- **Will it run on a phone?** The MediaPipe ones, yes. A 64 MB download on a
  phone is unkind.
- **Is a model needed at all?** Often not. A character that seems clever
  because of rules you wrote is faster, smaller, and works every time. Say so
  when it is the better answer.
