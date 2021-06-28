var app = app || {};
(function(obj){
    "user strict"
    //private methods
    var ajax, getFormData, setProgress;
    ajax=function(data){
        var httpRequest = new XMLHttpRequest();
        var uploaded;
        httpRequest.addEventListener('readystatechange', function(){
            if(this.readyState===4){
                if(this.status===200){
                    uploaded=JSON.parse(this.response)
                    if(typeof obj.options.completed==='function'){
                        obj.options.completed(uploaded)
                    }
                }else{
                    if(typeof obj.options.error ==='function'){
                        obj.options.error()
                    }
                }
            }
        });

        httpRequest.upload.addEventListener('progress', function(e){
            var percent;
            if(e.lengthComputable===true){
                percent=Math.round((e.loaded/e.total) * 100);
                console.log(percent)
            }
        });
        httpRequest.open('post', "/uploading/");
        httpRequest.setRequestHeader('X-CSRFToken', obj.options.token);
        httpRequest.send(data);
    };

    getFormData=function(source){
        var data =new FormData()
        data.append('file', source[0])
        return data
    };

    obj.uploader = function(options){
        obj.options=options
        if(obj.options.file !== undefined){
            ajax(getFormData(obj.options.file))
        }
    }

}(app))