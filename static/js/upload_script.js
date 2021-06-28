(function(){
    let standardUpload = document.getElementById('standard-upload')
    let dropzone = document.getElementById('drop-zone')
    let token = document.getElementsByName("csrfmiddlewaretoken")[0].value
    let progressbar = document.getElementById('bar-fill')
    let progressText = document.getElementById('bar-text')
    let uploadArea = document.getElementById('upload-area')
    let uploadInfo = document.getElementById('upload-info')
    let finished = document.getElementById('upload-finish')
    let fileField = document.getElementById('video_id')
    let category = document.getElementById('category')
    let optionCategory = ''

    String.prototype.format = function() {
        var formatted = this;
        for( var arg in arguments ) {
            formatted = formatted.replace("{" + arg + "}", arguments[arg]);
        }
        return formatted;
    };

    startUpload = function(file){
        app.uploader({
            file:file,
            token:token,
            progressbar:progressbar,
            progressText:progressText,
            completed:function(data){
                for(let i=0; i<data.category.length; i++){
                    optionCategory += '<option value="{0}">'.format(data.category[i]['id'])+data.category[i]['nameCategory']+'</option>'
                }
                var uploadedElement, uploadedVideo, videoSource
                uploadedElement=document.createElement('div')
                uploadedElement.className='w-1/2 flex-shink-0'
                uploadedVideo=document.createElement('video')
                uploadedVideo.controls=true
                videoSource=document.createElement('source')
                videoSource.src=data.video_path
                videoSource.type='video/mp4'
                uploadedVideo.appendChild(videoSource)
                uploadedElement.appendChild(uploadedVideo)
                finished.appendChild(uploadedElement)
                finished.className="upload-completed flex justify-center"
                category.innerHTML=optionCategory
                uploadArea.className='hidden'
                uploadInfo.className='video-info'
                fileField.value=data.video_id
            },
            error:function(){
                console.log('upload was not successfully')
            },
        })
    }

    standardUpload.addEventListener('click', function(e){
        e.preventDefault()
        let filetoUpload = document.getElementById('file-upload').files
        if(filetoUpload.length){
            startUpload(filetoUpload)
        }
    })

    dropzone.ondrop=function(e){
        e.preventDefault(e)
        startUpload(e.dataTransfer.files)
    }

    dropzone.ondragover = function(){
        this.className = "upload-drop drop"
        return false
    }

    dropzone.ondragleave = function(){
        this.className = "upload-drop"
        return false
    }

}())