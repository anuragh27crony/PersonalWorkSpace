function fetchData(url) {
  return new Promise(function(resolve, reject) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.responseType = "arraybuffer";
    xhr.onload = function() {
      if (this.status >= 200 && this.status < 400) {
        console.log(this.response);
        resolve(new Uint8Array(this.response));
      } else {
        reject(new Error(this.responseText));
      }
    };
    xhr.onerror = reject;
    xhr.send();
  });
}

Promise.all([
  fetchData("./1.jpg"),
  fetchData("./2.jpg"),
]).then(blobs => {
  var res = ffmpeg({
    MEMFS: blobs.map((data, i) => ({name: `${i}.jpg`, data})),
    stdin: function() {},
    arguments: [
      "-framerate", "10",
      "-i", "%d.jpg",
      "out.webm",
    ],
  });
  var videoBlob = new Blob([res.MEMFS[0].data]);
  var videoUrl = URL.createObjectURL(videoBlob);
  document.getElementById("video").src = videoUrl;
  document.getElementById("link").href = videoUrl;
});