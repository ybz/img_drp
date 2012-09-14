window.putz ?= {}
window.putz.drop = ns =
    image_sent : false
    event_list : {}
    events : (id) ->
        ev = id and ns.event_list[id]
        if not ev
            callbacks = $.Callbacks()
            ev =
                publish : callbacks.fire
                subscribe : callbacks.add
                unsubscribe : callbacks.remove
            if id
                ns.event_list[id] = ev
        return ev
    attachDropHandler : (dom_el, handler) ->
        el = $(dom_el)
        console.log 'attachFileDropHandler el: ', el
        if not el.length
            throw TypeError 'invalid dom_el'
        el.on 'dragenter', false
        el.on 'dragover', false
        el.on 'drop', (e) ->
            e.stopPropagation()
            e.preventDefault()
            handler(e)
    dropHandler : (ev) ->
        data_transfer = ev.originalEvent.dataTransfer
        files = data_transfer.files
        console.log 'a file was dropped, data_transfer ', data_transfer, ' files ', files
        console.log "x1 you have seemed to drop #{files.length} files"
        if not files
            return
        for file in files
            if !!file.type.match /^image/
                file_to_send = file
                break
        if not file_to_send
            return
        console.log 'got file to send ', file_to_send
        ns.sendImageForDetection file_to_send
    sendImageForDetection : (img_file) ->
        console.log 'about to send an image for detection'
        file_data = new FormData()
        file_data.append 'image', img_file
        ajax_params =
            url : putz.urls.face_detect_post
            data : file_data
            processData : false
            contentType : false
            type : 'POST'
            success : ->
                ns.events('face_ajax_returned').publish.apply ns.events('face_ajax_returned'), arguments
        console.log 'sending file with params: ', ajax_params
        ns.face_image = img_file
        xhr = $.ajax ajax_params
        ns.events('face_ajax_sent').publish()
    parseFaceDetectResponse : ->
        console.log 'returned from post, arguments ', arguments
        res_data = arguments[0]
        console.log res_data
        if res_data.face
            face = res_data.face
            target_width = 60
            target_height = 100
            target_x_offset = 180
            target_y_offset = 85
            img_scale_factor = ((target_width / face.width) + (target_height / face.height)) / 2
            img_width = Math.floor(res_data.image.width * img_scale_factor)
            face_x_offset = Math.floor(target_x_offset - (face.x * img_scale_factor)) - 10
            face_y_offset = Math.floor(target_y_offset - (face.y * img_scale_factor)) + 5
            $('.drop_ground').remove()
            $('body').prepend("""
                <div class="putzcard_wrapper">
                    <div class="putzcard stage">
                        <div class="img_wrapper">
                            <img src=""/>
                            <div class="img_overlay"></div>
                        </div>
                    </div>
                </div>
            """)
            reader = new FileReader()
            img_file = ns.face_image
            img_el = $('.putzcard img')
            reader.onload = ->
                img_el.attr 'src', reader.result
                img_el.css
                    width : img_width + "px"
                    height : 'auto'
                    left : face_x_offset
                    top : face_y_offset
            reader.readAsDataURL(img_file)
            console.log 'img loaded'
            face = res_data.face
        else
            $('.drop_ground .content').html 'Sorry, no face detected in image'



$ ->
    drop_ground = $('.drop_ground')
    ns.attachDropHandler drop_ground, ns.dropHandler
    ns.events('face_ajax_returned').subscribe ns.parseFaceDetectResponse
    ns.events('face_ajax_sent').subscribe ->
        drop_ground.off 'drop', ns.dropHandler
        drop_ground.children('.content').html 'Sending image...'
