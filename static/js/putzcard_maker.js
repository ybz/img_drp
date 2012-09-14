// Generated by CoffeeScript 1.3.3
(function() {
  var ns, _ref;

  if ((_ref = window.putz) == null) {
    window.putz = {};
  }

  window.putz.drop = ns = {
    image_sent: false,
    event_list: {},
    events: function(id) {
      var callbacks, ev;
      ev = id && ns.event_list[id];
      if (!ev) {
        callbacks = $.Callbacks();
        ev = {
          publish: callbacks.fire,
          subscribe: callbacks.add,
          unsubscribe: callbacks.remove
        };
        if (id) {
          ns.event_list[id] = ev;
        }
      }
      return ev;
    },
    attachDropHandler: function(dom_el, handler) {
      var el;
      el = $(dom_el);
      console.log('attachFileDropHandler el: ', el);
      if (!el.length) {
        throw TypeError('invalid dom_el');
      }
      el.on('dragenter', false);
      el.on('dragover', false);
      return el.on('drop', function(e) {
        e.stopPropagation();
        e.preventDefault();
        return handler(e);
      });
    },
    dropHandler: function(ev) {
      var data_transfer, file, file_to_send, files, _i, _len;
      data_transfer = ev.originalEvent.dataTransfer;
      files = data_transfer.files;
      console.log('a file was dropped, data_transfer ', data_transfer, ' files ', files);
      console.log("x1 you have seemed to drop " + files.length + " files");
      if (!files) {
        return;
      }
      for (_i = 0, _len = files.length; _i < _len; _i++) {
        file = files[_i];
        if (!!file.type.match(/^image/)) {
          file_to_send = file;
          break;
        }
      }
      if (!file_to_send) {
        return;
      }
      console.log('got file to send ', file_to_send);
      return ns.sendImageForDetection(file_to_send);
    },
    sendImageForDetection: function(img_file) {
      var ajax_params, file_data, xhr;
      console.log('about to send an image for detection');
      file_data = new FormData();
      file_data.append('image', img_file);
      ajax_params = {
        url: putz.urls.face_detect_post,
        data: file_data,
        processData: false,
        contentType: false,
        type: 'POST',
        success: function() {
          return ns.events('face_ajax_returned').publish.apply(ns.events('face_ajax_returned'), arguments);
        }
      };
      console.log('sending file with params: ', ajax_params);
      ns.face_image = img_file;
      xhr = $.ajax(ajax_params);
      return ns.events('face_ajax_sent').publish();
    },
    parseFaceDetectResponse: function() {
      var face, face_x_offset, face_y_offset, img_el, img_file, img_scale_factor, img_width, reader, res_data, target_height, target_width, target_x_offset, target_y_offset;
      console.log('returned from post, arguments ', arguments);
      res_data = arguments[0];
      console.log(res_data);
      if (res_data.face) {
        face = res_data.face;
        target_width = 60;
        target_height = 100;
        target_x_offset = 180;
        target_y_offset = 85;
        img_scale_factor = ((target_width / face.width) + (target_height / face.height)) / 2;
        img_width = Math.floor(res_data.image.width * img_scale_factor);
        face_x_offset = Math.floor(target_x_offset - (face.x * img_scale_factor)) - 10;
        face_y_offset = Math.floor(target_y_offset - (face.y * img_scale_factor)) + 5;
        $('.drop_ground').remove();
        $('body').prepend("<div class=\"putzcard_wrapper\">\n    <div class=\"putzcard stage\">\n        <div class=\"img_wrapper\">\n            <img src=\"\"/>\n            <div class=\"img_overlay\"></div>\n        </div>\n    </div>\n</div>");
        reader = new FileReader();
        img_file = ns.face_image;
        img_el = $('.putzcard img');
        reader.onload = function() {
          img_el.attr('src', reader.result);
          return img_el.css({
            width: img_width + "px",
            height: 'auto',
            left: face_x_offset,
            top: face_y_offset
          });
        };
        reader.readAsDataURL(img_file);
        console.log('img loaded');
        return face = res_data.face;
      } else {
        return $('.drop_ground .content').html('Sorry, no face detected in image');
      }
    }
  };

  $(function() {
    var drop_ground;
    drop_ground = $('.drop_ground');
    ns.attachDropHandler(drop_ground, ns.dropHandler);
    ns.events('face_ajax_returned').subscribe(ns.parseFaceDetectResponse);
    return ns.events('face_ajax_sent').subscribe(function() {
      drop_ground.off('drop', ns.dropHandler);
      return drop_ground.children('.content').html('Sending image...');
    });
  });

}).call(this);