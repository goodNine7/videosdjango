$(document).ready(function(){

    // $(document).on('click', function (e) {
    //     if ($(e.target).closest("#report-area").length === 0) {
    //         $("#report-area").addClass('hidden');
    //     }
    // });

    // $("[data-link]").click(function() {
    //     window.location.href = $(this).attr("data-link");
    //     return false;
    //   });

    // $('.toggle-password').click(function(){
    //     let input = $($(this).attr("toggle"));
    //     if (input.attr("type") == "password") {
    //         input.attr("type", "text");
    //         $(this).empty()
    //         let icon = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" /><path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" /></svg>'
    //         $(this).append(icon)
    //     } else {
    //         input.attr("type", "password");
    //         $(this).empty()
    //         let icon = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z" /><path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" /></svg>'
    //         $(this).append(icon)
    //     }
    // })

    // textarea comment
    $('textarea').bind('keypress', function(e) {
        if ((e.keyCode || e.which) == 13) {
          event.preventDefault();
        }
      });

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
        let target=$(this)

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
                        $('.love-text-vid').text("0%")
                    }
                    else{
                        favorite=parseInt(favorite)
                        $('.love-text-vid').text(favorite + "%")
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
        let target=$(this)

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
                        $('.love-text-vid').text("0%")
                    }
                    else{
                        favorite=parseInt(favorite)
                        $('.love-text-vid').text(favorite + "%")
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
        const ban_list = ['dcm', 'dmm', 'dm']
        let filter_cmt
        let rs = []
        filter_cmt = comment.split(' ')
        if (!comment.trim()) {
            $('#comment').val('')
       }
       else{
        for (let i = 0; i < filter_cmt.length; i++) {
            if (ban_list.indexOf(filter_cmt[i]) > -1) {
                rs.push(filter_cmt[i])
            }
          }
        if(rs.length){
            alert("Your comment contains BANNED words ({0}) !!!".format(rs.join(', ')))
        }
        else{
            $.ajax({
                method:"POST",
                url:url,
                headers:{'X-CSRFToken':token},
                data:{
                    video_id:video_id,
                    comment:comment
                },
                success:function(response){
                    if(response.login_required){
                        window.location.href=response.login_required
                    }
                    else if(response.blocked){
                        $('#comment').val('')
                        alert(response.blocked)
                    }
                    else{
                        $('#total-cmt').text(response.total_cmt + ' comments')
                        $('#comment').val('')
                        let cmt_content=document.getElementById('comment-content')
                        let current_content=cmt_content.innerHTML
                        let new_content='<div class="flex space-x-4 mb-8 bg-white px-2 py-4 rounded-2xl"><div class="rounded-full overflow-hidden flex-shrink-0"><a href="/channel/{0}/"><img src="{1}" alt="" class="w-12 h-12 object-cover"></a></div><div class="break-all"><div class="flex space-x-2 items-center"><a href="/channel/{2}/" class="hover:underline"><h2 class="capitalize font-semibold text-xl">{3}</h2></a><span>0&nbsp;minutes ago</span></div><span class="py-1">{4}</span></div></div>'.format(response.channel_slug, response.channel_avatar, response.channel_slug, response.channel_name, comment)
                        cmt_content.innerHTML=new_content+current_content
                    }
                },
                error:function(response){
                    console.log('Failed ', response)
                }
            })
        }
       } 
    })

    $('.report-mes').click(function(e){
        e.preventDefault()
        $('.report-mes').addClass('hidden')
    })

    $('#close-report-form').click(function(e){
        e.preventDefault()
        $('#report-area').addClass('hidden')
    })

    $('#open-report-form').click(function(e){
        e.preventDefault()
        $('#report-area').removeClass('hidden')
    })

    $('.report-form #report-reason').on('change', function(){
        if($(this).attr("value") == "Other"){
            $('#other-reason').removeClass('hidden')
        }
        else{
            $('#other-reason').addClass('hidden')
        }
    })

    $('.report-form').submit(function(e){
        e.preventDefault()
        const channel=$('#btn-send-report').val() 
        const url=$(this).attr('action')
        const token=$('input[name=csrfmiddlewaretoken]').val()
        let report_reason=$('#report-reason:checked').val()
        if(report_reason == 'Other'){
            report_reason=$('#other-reason').val()
        }
        $.ajax({
            method: "POST",
            url: url,
            headers: {'X-CSRFToken': token},
            data: {
                channel: channel,
                report_reason: report_reason
            },
            success:function(response){
                if(response.login_required){
                    window.location.href=response.login_required
                }
                else{
                    if(response.text_required){
                        $('.report-mes').removeClass('hidden bg-green-300')
                        $('.report-mes').addClass('bg-red-300')
                        $('.report-mes').text(response.text_required)
                    }
                    else{
                        $('#other-reason').val('')
                        $('.report-mes').removeClass('hidden')
                        $('.report-mes').addClass('bg-green-300')
                        $('.report-mes').text(response.success_mes)
                    }
                }
            },
            error:function(response){
                console.log('Failed', response)
            }
        })
    })

    $('.form-remove-videos-playlist').submit(function(e){
        e.preventDefault()
        const video_id=$(this).find('.id-videos-playlist').val()
        const token=$(this).find('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')
        const target=$(this).find('.id-videos-playlist')
        if(confirm('Remove ?')){
            $.ajax({
                method:"POST",
                url:url,
                headers:{'X-CSRFToken':token},
                data:{
                    video_id:video_id
                },
                success:function(response){
                    alert(response.success_message)
                    target.closest('.items').remove()
                    location.reload();
                },
                error:function(response){
                    console.log('Failed', response)
                }
            })
        }
    })

    $('.form-del-myvideos').submit(function(e){
        e.preventDefault()
        const video_id=$(this).find('.id-myvideos').val()
        const token=$(this).find('input[name=csrfmiddlewaretoken]').val()
        const url=$(this).attr('action')
        const target=$(this).find('.id-myvideos')
        const target_in_playlist=$('.id-videos-playlist').filter(function(){
            return this.value == video_id
        })

        if(confirm('Delete ?')){
            $.ajax({
                method:"POST",
                url:url,
                headers:{'X-CSRFToken':token},
                data:{
                    video_id:video_id
                },
                success:function(response){
                    alert(response.success_message)
                    target.closest('.items').remove()
                    if(target_in_playlist.length){
                        target_in_playlist.closest('.items').remove()
                    }
                    location.reload();
                },
                error:function(response){
                    console.log('Failed', response)
                }
            })
        }
    })

    $('.form-edit-myvideos').submit(function(e){
        e.preventDefault()
        var form_data = new FormData();
        const title=$(this).find('#title').val()
        const description=$(this).find('#description').val()
        const thumbnail=$(this).find('#thumbnail').prop('files')
        const category=$(this).find('#category option:selected').val()
        const visibility=$(this).find('#visibility option:selected').val()
        const url=$(this).attr('action')
        const token=$('input[name=csrfmiddlewaretoken]').val()
        form_data.append('title', title)
        form_data.append('description', description)
        form_data.append('thumbnail', thumbnail[0])
        form_data.append('category', category)
        form_data.append('visibility', visibility)
        
        $.ajax({
            method: "POST",
            url:url,
            headers:{'X-CSRFToken': token},
            processData: false,
            contentType: false,
            data:form_data,
            success:function(response){
                $('ul.messages').removeClass('hidden')
                setTimeout(() => {
                    $('ul.messages').addClass('hidden')
                }, 2500);
            },
            error:function(response){
                console.log('Failed', response)
            }
        })
    })

    //close messages
    $('ul.messages').click(function(){
        $(this).addClass('hidden')
    })


});