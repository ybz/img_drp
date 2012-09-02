window.putz ?= {}
window.putz.drop = ns =
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
$ ->
    drop_ground = $('.drop_ground')
    ns.attachDropHandler drop_ground, (e) ->
        data_transfer = e.originalEvent.dataTransfer
        files = data_transfer.files
        console.log 'a file was dropped, data_transfer ', data_transfer, ' files ', files
        console.log "you have seemed to drop #{files.length} files"
