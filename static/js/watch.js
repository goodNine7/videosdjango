$(document).ready(function(){
    const video = document.getElementById("currentvideo");
    const key = window.location.href
    const videoId = video.querySelector("source").src
    let intervalHandle = null;
    video.volume=0.05

    setTimeout(() => {
        video.play()
        video.addEventListener("play", () => {
            console.log('play')
            intervalHandle = setInterval(() => {
              savePosition(key, videoId, video.currentTime);
            }, 1000)
        })
      }, 100);
    
      
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
            if(video.duration == position){
                position = 0
            }
            localStorage.setItem(key, JSON.stringify({
            videoId,
            position
            }));
        } catch (error) {}
    }
      
    const rs = getPosition(key, videoId);
      
    video.currentTime = rs.position;

})