
$(function () {


    //modify buttons style
    $.fn.editableform.buttons =
        '<button type="submit" class="btn btn-success editable-submit btn-sm waves-effect waves-light"><i class="mdi mdi-check"></i></button>' +
        '<button type="button" class="btn btn-danger editable-cancel btn-sm waves-effect waves-light"><i class="mdi mdi-close"></i></button>';


    //inline

    $('#inline-username').editable({
        type: 'text',
        pk: 1,
        name: 'username',
        title: 'Enter username',
        mode: 'inline',
        inputclass: 'form-control-sm',

        success: function(responsetxt, newValue) {           
            source = $(this).data('inline-username').input.sourceData;
            var selected = $.fn.editableutils.itemsByValue(newValue, source); 
            if (selected.length) {
                console.log(selected[0].value);
                console.log(selected[0].text);
            }           
        },
    });

    $('#inline-firstname').editable({
        validate: function (value) {
            alert(value)
            if ($.trim(value) == '') return 'This field is required';
        },
        mode: 'inline',
        inputclass: 'form-control-sm'
    });


    $('#inline-status').editable({
        mode: 'inline',
        inputclass: 'form-control-sm'
    });

    $('#inline-group').editable({
        showbuttons: false,
        mode: 'inline',
        inputclass: 'form-control-sm'
    });

    $('#inline-dob').editable({
        mode: 'inline',
        inputclass: 'form-control-sm'
    });

    $('#inline-comments').editable({
        showbuttons: 'bottom',
        mode: 'inline',
        inputclass: 'form-control-sm'
    });


});