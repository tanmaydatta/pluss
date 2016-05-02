// $(function() {

//     $('#side-menu').metisMenu();

// });

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    $(window).bind("load resize", function() {
        topOffset = 50;
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
});
var substringMatcher = function(strs) {
    return function findMatches(q, cb) {
        var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(strs, function(i, str) {
            if (substrRegex.test(str)) {
                matches.push(str);
            }
        });

        cb(matches);
    };
};

function setFile(file_name) {
    $('#file').val(file_name);
}

function setFPoster(file_name) {
    $('#f_poster').val(file_name);
}
var URL='http://' + $(location).attr('host') + '/';


function edit_content(id) {
    var formData = new FormData();
    var hours = $('#hours').val();
    var minutes = $('#minutes').val();
    var seconds = $('#seconds').val();

    if (hours == "0" && minutes == "0" && seconds == "0") {
        var duration = '';
    }
    if ($('#select3').val() == "nothing selected") {
        $('#select3').val('');
    }

    if ($('#e_poster').val() == "choose poster") {
        $('#e_poster').val('');
    }
    if ($('#file').val() == "choose content") {
        $('#file').val('');
    }
    var data1 = {
        name: $('#name').val(),
        duration: hours + ':' + minutes + ':' + seconds,
        genre: $('#select3').val(),
        language: $('#language').val(),
        type: $('#content_type').val(),
        file: $('#file').val()
    }
    formData.append('name', $('#name').val());
    formData.append('duration', hours + ':' + minutes + ':' + seconds);
    formData.append('genre[]', $('#select3').val());
    formData.append('language', $('#language').val());
    formData.append('type', $('#content_type').val());
    formData.append('e_poster', $('#e_poster').val());
    formData.append('file_name', $('#file').val());
    formData.append('json', JSON.stringify(data1));
    if ($('#f_poster')[0].files.length == 1) {
        formData.append('f_poster',$('#f_poster')[0].files[0]);
    }   
    $.ajax({
        type: "POST",
        url: URL + 'content/edit/' + id,

        enctype: 'multipart/form-data',
        async: false,
        data: formData,
        success: function(result) {
            result = JSON.parse(result);
            if (result['status'] == "success") {
                alert(result['message']);
                if (result['metadata']) {
                    alert('metadata file created');
                } else {
                    alert('metadata file not created');
                }
            } else {
                alert(result['error']);
            }
        },
        error: function(xhr, status, error) {
            alert('request not send');
            
        },
        cache: false,
        contentType: false,
        processData: false
    });
}

function addContent() {
    var formData = new FormData();
    var hours = $('#hours').val();
    var minutes = $('#minutes').val();
    var seconds = $('#seconds').val();

    if (hours == "0" && minutes == "0" && seconds == "0") {
        var duration = '';
    }
    if ($('#select3').val() == "nothing selected") {
        $('#select3').val('');
    }
    if ($('#e_poster').val() == "select poster") {
        $('#e_poster').val('');
    }
    if ($('#file').val() == "choose content") {
        $('#file').val('');
    }
    var data1 = {
        name: $('#name').val(),
        duration: hours + ':' + minutes + ':' + seconds,
        genre: $('#select3').val(),
        language: $('#language').val(),
        type: $('#content_type').val(),
        file: $('#file').val()
    }
    formData.append('name', $('#name').val());
    formData.append('duration', hours + ':' + minutes + ':' + seconds);
    formData.append('genre[]', $('#select3').val());
    formData.append('language', $('#language').val());
    formData.append('type', $('#content_type').val());
    formData.append('e_poster', $('#e_poster').val());
    formData.append('file_name', $('#file').val());
    formData.append('download', $('#download').is(":checked"));
    formData.append('link', $('#link').val());
    formData.append('json', JSON.stringify(data1));
    if ($('#f_poster')[0].files.length == 1) {
        formData.append('f_poster',$('#f_poster')[0].files[0]);
    }   
    $.ajax({
        type: "POST",
        url: URL + 'content/insert/',
        enctype: 'multipart/form-data',
        async: false,
        data: formData,
        success: function(result) {
            result = JSON.parse(result);
            if (result['status'] == "success") {
                alert(result['message']);
                if (result['metadata']) {
                    alert('metadata file created');
                } else {
                    alert('metadata file not created');
                }
            } else {
                alert(result['error']);
            }
        },
        error: function(xhr, status, error) {
            alert('request not send');
        },
        cache: false,
        contentType: false,
        processData: false
    });
}


function delete_content(id) {
    $.ajax({
        type: "POST",
        url: URL + 'content/delete/' + id + '/',
       
        success: function(result) {
            result = JSON.parse(result);
            if (result['status'] == "success") {
                alert(result['message']);
                window.location.reload();
            } else {
                alert(result['error']);
            }
        },
        error: function(xhr, status, error) {
            alert('request not send');
        }
    });
    return true;

}

var ids = $('.poster-hover').map(function(index) {
    return this.id; 
});

$.each( ids, function(key,value ) {
    $('#' + value).popover({
        html: true,
        trigger: 'hover',
        // container: 'table',
        placement: function(tip, element) {
            var offset = $(element).offset();
            height = $(document).outerHeight();
            width = $(document).outerWidth();
            vert = 0.5 * height - offset.top;
            vertPlacement = vert > 0 ? 'bottom' : 'top';
            horiz = 0.5 * width - offset.left;
            horizPlacement = horiz > 0 ? 'right' : 'left';
            placement = Math.abs(horiz) > Math.abs(vert) ? horizPlacement : vertPlacement;
            return placement;
        },
        content: function() {
            return '<img class="img-thumbnail" src="/content/poster_image/' + value + '" />';
        }
    });
});

function showposterimage()
{
    var id = $('#e_poster').find('option:selected').attr('id');
    if (id)
    {
        $('#preview').attr('src',URL + 'poster/image/' + id);
        $('#preview').show();
    }
    else
    {
        $('#preview').hide();
    }
}

$(document).ready(function() {
    $('.bootstrap-select').css('width','100%');
    showposterimage();
    show_folder_poster_image();
});

var usedNames = {};
$("select[name='genre'] > option").each(function () {
    if(usedNames[this.text]) {
        $(this).remove();
    } else {
        usedNames[this.text] = this.value;
    }
});

function addfolder() {
    var formData = new FormData();
    if($('#e_poster').val()=="select poster")
    {
        $('#e_poster').val('');
    }
    if($('#f_poster').val()=="")
    {
        $('#f_poster').val('');
    }
    var data1 = {
        name: $('#name').val()
    }
    formData.append('name', $('#name').val());
    formData.append('e_poster', $('#e_poster').val());
    formData.append('json', JSON.stringify(data1));
    if ($('#f_poster')[0].files.length == 1) {
        formData.append('f_poster',$('#f_poster')[0].files[0]);
    }

    $.ajax({
        type: "POST",
        url: URL + 'folder/insert/',
        enctype: 'multipart/form-data',
        async: false,
        data: formData,
        // data: {
        //     name           : $('#name').val(),          
        //     e_poster       : $('#e_poster').val(),
        //     f_poster       : $('#f_poster').val(),
            
        // },
        success: function(result) 
        {
            result=JSON.parse(result);
            if (result['status'] == "success") 
            {
                alert(result['message']);
                if(result['metadata'])
                {
                    alert('metadata file created');
                }
                else
                {
                    alert('metadata file not created');
                }
            }
            else {
                 alert(result['error']);
            }
        },
        error: function(xhr, status, error) 
        {
         alert('request not send');
        } ,  
        cache: false,
        contentType: false,
        processData: false
    });
}



function editfolder(id) {
    var formData = new FormData();
    if ($('#e_poster').val()== "select poster")
    {
        $('#e_poster').val('');
    }
    var data1 = {
        fname: $('#name').val()
    }
    formData.append('fname', $('#name').val());
    formData.append('e_poster', $('#e_poster').val());
    formData.append('json', JSON.stringify(data1));
    if ($('#f_poster')[0].files.length == 1) {
        formData.append('f_poster',$('#f_poster')[0].files[0]);
    }    
    $.ajax({
        type: "POST",
        url: URL + 'folder/edit/' + id,
        enctype: 'multipart/form-data',
        async: false,
        data: formData,
        success: function(result) 
        {
            result=JSON.parse(result);
            if (result['status'] == "success") 
            {
                alert(result['message']);
                if(result['metadata'])
                {
                    alert('metadata file created');
                }
                else
                {
                    alert('metadata file not created');
                }
            }
            else {
                 alert(result['error']);
            }
        },
        error: function(xhr, status, error) 
        {
         alert('request not send');
        } ,
        cache: false,
        contentType: false,
        processData: false   
    });
}


function deleteFolder(id) {
    $.ajax({
        type: "POST",
        url: URL + 'folder/delete/' + id + '/',

        success: function(result) {
            result = JSON.parse(result);
            if (result['status'] == "success") {
                alert(result['message']);
                window.location.reload();
            } else {
                alert(result['error']);
            }
        },
        error: function(xhr, status, error) {
            alert('request not send');
        }
    });
    return true;

}

function show_folder_poster_image()
{
    var id = $('#e_poster').find('option:selected').attr('id');
    if (id)
    {
        $('#preview').attr('src',URL + 'folder/folder_image/' + id );
        $('#preview').show();
    }
    else
    {
        $('#preview').hide();
    }
}

var f_ids = $('.poster-hover-folder').map(function(index) {
    return this.id; 
});

$.each( f_ids, function(key,value ) {
    $('#' + value).popover({
        html: true,
        trigger: 'hover',
        placement: function(tip, element) {
            var offset = $(element).offset();
            height = $(document).outerHeight();
            width = $(document).outerWidth();
            vert = 0.5 * height - offset.top;
            vertPlacement = vert > 0 ? 'bottom' : 'top';
            horiz = 0.5 * width - offset.left;
            horizPlacement = horiz > 0 ? 'right' : 'left';
            placement = Math.abs(horiz) > Math.abs(vert) ? horizPlacement : vertPlacement;
            return placement;
        },
        content: function() {
            return '<img class="img-thumbnail" src="/folder/image/' + value + '" />';
        }
    });
});