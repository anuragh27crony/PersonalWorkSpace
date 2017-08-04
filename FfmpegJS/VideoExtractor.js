console.log("Process exited with code");
var ffmpeg = require("ffmpeg.js/ffmpeg-mp4");
// var ffmpeg_mp4_worker = require("ffmpeg.js/ffmpeg-worker-mp4.js")
var stdout = "";
var stderr = "";
// // Print FFmpeg's version.
// ffmpeg({
//   arguments: ["-version"],
//   print: function(data) { stdout += data + "\n"; },
//   printErr: function(data) { stderr += data + "\n"; },
//   onExit: function(code) {
//     console.log("Process exited with code " + code);
//     console.log(stdout);
//   },
// });


// var fs = require("fs");
// var testData = new Uint8Array(fs.readFileSync("test.webm"));
// // Encode test video to VP8.
// var result = ffmpeg({
//   MEMFS: [{name: "test.webm", data: testData}],
//   arguments: ["-i", "test.webm", "-c:v", "libvpx", "-an", "out.webm"],
//   // Ignore stdin read requests.
//   stdin: function() {},
// });
// // Write out.webm to disk.
// var out = result.MEMFS[0];
// fs.writeFileSync(out.name, Buffer(out.data));


// var fs = require("fs");
// var testData = new Uint8Array(fs.readFileSync("test.webm"));
// // Encode test video to VP8.
// var result = ffmpeg({
//   MEMFS: [{name: "test.webm", data: testData}],
//   arguments: ["-i", "test.webm", "-c:v", "libvpx", "-an", "out.webm"],
//   // Ignore stdin read requests.
//   stdin: function() {},
// });
// // Write out.webm to disk.
// var out = result.MEMFS[0];
// fs.writeFileSync(out.name, Buffer(out.data));

// *************************************

var ffmpeg = require("ffmpeg.js/ffmpeg-mp4");
var fs = require("fs");
var stdout = "";
var stderr = "";

var testData = new Uint8Array(fs.readFileSync("Sample.mp4"));

var result = ffmpeg({
  MEMFS: [{name: "Sample.mp4", data: testData}],
  stdin: function() {},
  arguments: ["-i", "Sample.mp4","-r","1", "output%d.png"],
});

console.log(result.MEMFS.length)
if(result.MEMFS.length>0){
    var out = result.MEMFS[0].data;
    fs.writeFileSync("test.jpg", Buffer(out.data));
    }

// *************************************


// var stdout = "";
// var stderr = "";
// var Worker = require('webworker-threads').Worker;
// var worker = new Worker("ffmpeg-worker-mp4.js");
// worker.onmessage = function(e) {
//   var msg = e.data;
//   switch (msg.type) {
//   case "ready":
//     worker.postMessage({type: "run", arguments: ["-version"]});
//     break;
//   case "stdout":
//     stdout += msg.data + "\n";
//     break;
//   case "stderr":
//     stderr += msg.data + "\n";
//     break;
//   case "exit":
//     console.log("Process exited with code " + msg.data);
//     console.log(stdout);
//     worker.terminate();
//     break;
//   }
// };

