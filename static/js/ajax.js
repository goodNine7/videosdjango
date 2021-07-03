$(document).ready(function(){
    $('.like-form').submit(function(e){
        e.preventDefault();
        const video_id=$('.like-btn').val()
        const token=$('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')

        $.ajax({
            method: "POST",
            url:url,
            headers:{'X-CSRFToken':token},
            data:{
                'video_id':video_id
            },
            success:function(response){
                if(response.liked==true){
                    $('#like-icon').addClass("text-blue-700")
                    $('#dislike-icon').removeClass("text-blue-700")
                }
                else{
                    $('#like-icon').removeClass("text-blue-700")
                }

                like=$('#like-count').text(response.like_count)
                parseInt(like)
                dislike=$('#dislike-count').text(response.dislike_count)
                parseInt(dislike)
            },
            error:function(response){
                console.log("Failed ", response)
            }
        })
    });
    
    $('.dislike-form').submit(function(e){
        e.preventDefault();
        const video_id=$('.dislike-btn').val()
        const token=$('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')

        $.ajax({
            method: "POST",
            url:url,
            headers:{'X-CSRFToken':token},
            data:{
                'video_id':video_id
            },
            success:function(response){
                if(response.disliked==true){
                    $('#dislike-icon').addClass("text-blue-700")
                    $('#like-icon').removeClass("text-blue-700")
                }
                else{
                    $('#dislike-icon').removeClass("text-blue-700")
                }

                dislike=$('#dislike-count').text(response.dislike_count)
                parseInt(dislike)
                like=$('#like-count').text(response.like_count)
                parseInt(like)
            },
            error:function(response){
                console.log("Failed ", response)
            }
        })
    })
});