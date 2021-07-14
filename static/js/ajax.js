$(document).ready(function(){
    
    String.prototype.format = function() {
        var formatted = this;
        for( var arg in arguments ) {
            formatted = formatted.replace("{" + arg + "}", arguments[arg]);
        }
        return formatted;
    };

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
                if(response.login_required){
                    window.location.href=response.login_required
                }
                else{
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
                    favorite=Math.round(100/(response.like_count+response.dislike_count))*response.like_count
                    if(isNaN(favorite)){
                        favorite=parseInt(0)
                        $('.love-text').text("0%")
                    }
                    else{
                        favorite=parseInt(favorite)
                        $('.love-text').text(favorite + "%")
                    }
                    document.getElementById('love-bar').style.width=favorite + "%"
                }
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
                if(response.login_required){
                    window.location.href=response.login_required
                }
                else{
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
                    favorite=Math.round(100/(response.like_count+response.dislike_count))*response.like_count
                    if(isNaN(favorite)){
                        favorite=parseInt(0)
                        $('.love-text').text("0%")
                    }
                    else{
                        favorite=parseInt(favorite)
                        $('.love-text').text(favorite + "%")
                    }
                    document.getElementById('love-bar').style.width=favorite + "%"
                } 
            },
            error:function(response){
                console.log("Failed ", response)
            }
        })
    });

    $('.subcriber-form').submit(function(e){
        e.preventDefault()
        const channel_id=$('.sub-btn').val()
        const token=$('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')
        $.ajax({
            method:"POST",
            url:url,
            headers:{'X-CSRFToken':token},
            data:{
                channel_id:channel_id
            },
            success:function(response){
                if(response.login_required){
                    window.location.href=response.login_required
                }
                else{
                    if(response.Subcribed==true){
                        $('#sub-btn').removeClass('bg-red-700')
                        $('#sub-btn').addClass('bg-gray-500')
                        $('#sub-text').text('Subcribed')
                        $('.sub-icon').removeClass('hidden')
                    }
                    else{
                        $('#sub-btn').addClass('bg-red-700')
                        $('#sub-btn').removeClass('bg-gray-500')
                        $('#sub-text').text('Subcribe')
                        $('.sub-icon').addClass('hidden')
                    }
                    subcriber=$('#sub-count').text(response.subcriber + ' Subcribers')
                    parseInt(subcriber)
                }
            },
            error:function(response){
                console.log("Failed ", response)
            }
        })
    });

    $('.playlist-form').submit(function(e){
        e.preventDefault()
        const video_id=$('.playlist-btn').val()
        const token=$('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')

        $.ajax({
            method:"POST",
            url:url,
            headers:{'X-CSRFToken':token},
            data:{
                video_id:video_id
            },
            success:function(response){
                if(response.login_required){
                    window.location.href=response.login_required
                }
                else{
                    if(response.added==true){
                        $('.playlist-btn').addClass('text-red-500')
                        $('.playlist-btn').removeClass('text-black')
                        $('.playlist-icon').removeClass('hidden')
                        $('.playlist-text').text('Playlist')
                    }
                    else{
                        $('.playlist-btn').addClass('text-black')
                        $('.playlist-icon').addClass('hidden')
                        $('.playlist-btn').removeClass('text-red-500')
                        $('.playlist-text').text('Add to Playlist')
                    }
                }
            },
            error:function(response){
                console.log("Failed ", response)
            }
        })
    })

    $('.cmt-form').submit(function(e){
        e.preventDefault()
        const video_id=$('#cmt-btn').val()
        const comment=$('#comment').val()
        const token=$('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')

        $.ajax({
            method:"POST",
            url:url,
            headers:{'X-CSRFToken':token},
            data:{
                video_id:video_id,
                comment:comment
            },
            success:function(response){
                console.log(response)
                $('#total-cmt').text(response.total_cmt + ' comments')
                $('#comment').val('')
                let cmt_content=document.getElementById('comment-content')
                let current_content=cmt_content.innerHTML
                let new_content='<div class="flex space-x-4 mb-8"><div class="rounded-full overflow-hidden flex-shrink-0"><a href="/channel/{0}/"><img src="{1}" alt="" class="w-12 h-12 object-cover"></a></div><div class="break-all"><div class="flex space-x-2 items-center"><h2 class="capitalize font-semibold text-xl">{2}</h2><span>0&nbsp;minutes ago</span></div><span class="py-1">{3}</span></div></div>'.format(response.channel_slug, response.channel_avatar, response.channel_name, comment)
                console.log(current_content)
                console.log(new_content)
                cmt_content.innerHTML=new_content+current_content
                
            },
            error:function(response){
                console.log('Failed ', response)
            }
        })
    })

});