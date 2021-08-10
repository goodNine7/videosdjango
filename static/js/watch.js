$(document).ready(function(){
    const video = document.getElementById("currentvideo");
    const key = window.location.href
    const videoId = video.querySelector("source").src
    let intervalHandle = null;
    video.volume=0.05
    video.play()

    video.addEventListener("play", () => {
        console.log('play')
        intervalHandle = setInterval(() => {
          savePosition(key, videoId, video.currentTime);
        }, 5000)
      })
      
      video.addEventListener("pause", () => {
        console.log('pause')
        clearInterval(intervalHandle);
        savePosition(key, videoId, video.currentTime)
      })
      
      const getPosition = (key, videoId) => {
        const defaultPosition = {
          videoId,
          position: 0
        }
      
        try {
          return JSON.parse(localStorage.getItem(key)) || defaultPosition;
        } catch (error) {
      
        }
      
        return defaultPosition;
      }
      
      const savePosition = (key, videoId, position) => {
        try {
          localStorage.setItem(key, JSON.stringify({
            videoId,
            position
          }));
        } catch (error) {}
      }
      
      const rs = getPosition(key, videoId);
      
      video.currentTime = rs.position;

})