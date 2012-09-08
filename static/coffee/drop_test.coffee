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
                ns.events('face_ajax_returned').publish arguments
        console.log 'sending file with params: ', ajax_params
        xhr = $.ajax ajax_params
        ns.events('face_ajax_sent').publish()


    

$ ->
    drop_ground = $('.drop_ground')
    ns.attachDropHandler drop_ground, ns.dropHandler
    ns.events('face_ajax_returned').subscribe ->
        console.log 'returned from post, arguments ', arguments
    ns.events('face_ajax_sent').subscribe ->
        drop_ground.off 'drop', ns.dropHandler
        drop_ground.children('.content').html 'Sending image...'
