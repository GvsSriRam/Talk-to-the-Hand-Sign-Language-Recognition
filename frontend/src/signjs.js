import {
  HandLandmarker,
  FilesetResolver
} from "@mediapipe/tasks-vision";

const demosSection = document.getElementById("demos");

let handLandmarker = undefined;
let runningMode = "IMAGE";
let enableWebcamButton;
let webcamRunning = false;

const createHandLandmarker = async () => {
  const vision = await FilesetResolver.forVisionTasks(
    "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm"
  );
  handLandmarker = await HandLandmarker.createFromOptions(vision, {
    baseOptions: {
      modelAssetPath: `https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task`,
      delegate: "GPU"
    },
    runningMode: runningMode,
    numHands: 1
  });
  demosSection.classList.remove("invisible");
};
createHandLandmarker();

/********************************************************************
// Continuously grab image from webcam stream and detect it.
********************************************************************/

const video = document.getElementById("webcam");
const canvasElement = document.getElementById("output_canvas");
const canvasCtx = canvasElement.getContext("2d");

// Check if webcam access is supported.
const hasGetUserMedia = () => !!navigator.mediaDevices?.getUserMedia;

// If webcam supported, add event listener to button for when user
// wants to activate it.
if (hasGetUserMedia()) {
  enableWebcamButton = document.getElementById("webcamButton");
  enableWebcamButton.addEventListener("click", enableCam);
} else {
  console.warn("getUserMedia() is not supported by your browser");
}

// Enable the live webcam view and start detection.
function enableCam(event) {
  if (!handLandmarker) {
    console.log("Wait! objectDetector not loaded yet.");
    return;
  }

  if (webcamRunning === true) {
    webcamRunning = false;
    enableWebcamButton.innerText = "ENABLE PREDICTIONS";
  } else {
    webcamRunning = true;
    enableWebcamButton.innerText = "DISABLE PREDICTIONS";
  }

  // getUsermedia parameters.
  const constraints = {
    video: true
  };

  // Activate the webcam stream.
  navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
    video.srcObject = stream;
    video.addEventListener("loadeddata", predictWebcam);
  });
}

const predictionElement = document.getElementById('prediction');
predictionElement.style.display = 'none';

const fullPredictionElement = document.getElementById('fullPrediction');
fullPredictionElement.style.display = 'none';

let lastVideoTime = -1;
let results = undefined;
let predictionString = ""; // Initialize a string to store predictions
let lastPredictionTime = 0; // Track the last prediction time

console.log(video);
async function predictWebcam() {
  canvasElement.style.width = video.videoWidth;;
  canvasElement.style.height = video.videoHeight;
  canvasElement.width = video.videoWidth;
  canvasElement.height = video.videoHeight;
  
  // Now let's start detecting the stream.
  if (runningMode === "IMAGE") {
    runningMode = "VIDEO";
    await handLandmarker.setOptions({ runningMode: "VIDEO" });
  }
  let startTimeMs = performance.now();
  if (lastVideoTime !== video.currentTime) {
    lastVideoTime = video.currentTime;
    results = handLandmarker.detectForVideo(video, startTimeMs);
  }
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  if (results.landmarks) {
    for (const landmarks of results.landmarks) {
      await drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {
        color: "#00FF00",
        lineWidth: 5
      });
      await drawLandmarks(canvasCtx, landmarks, { color: "#FF0000", lineWidth: 2 });
    }

    if (results.landmarks.length > 0) {
      // Convert results.landmarks array into json object
      const landmarks = results.landmarks

      // Send the landmarks to external endpoint for prediction
      const myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");
      const raw = JSON.stringify({
        "landmarks": landmarks
      });

      const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow"
      };

      const res = await fetch("https://ttth-uzgq5aihvq-uc.a.run.app/ttth/pred", requestOptions)
            .then((response) => response.json())
            .then((result) => {
              console.log(result);
              if (predictionElement) {
                predictionElement.textContent = result.pred; 
                predictionElement.style.display = 'block';
              } else {
                console.error("Prediction element not found!");
              }
              if (fullPredictionElement && Date.now() - lastPredictionTime >= 2000) {
                lastPredictionTime = Date.now();
                let predChar = result.pred[3];

                if (result.pred === "x0_space") {
                  predChar = " "; // Replace with a space
                } else if (result.pred === "x0_del" && predictionString.length > 0) {
                  predictionString = predictionString.slice(0, -1); // Remove the last character
                } else {
                  predictionString += predChar; // Append the 4th character
                }
  
                fullPredictionElement.textContent = predictionString; // Update the text content
                fullPredictionElement.style.display = 'block';
              } else {
                console.error("FUll Prediction element not found!");
              }
            })
            .catch((error) => console.error(error));
      
    }

  }
  canvasCtx.restore();

  // Call this function again to keep predicting when the browser is ready.
  if (webcamRunning === true) {
    window.requestAnimationFrame(predictWebcam);
  }
}
