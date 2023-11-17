function close_dropdown(){
    $('.dropdown-menu-close').on('click', function(){
        $(this).closest('.dropdown-menu').prev().click()
    })
}

function on_change_country(){
    $('select[name=country_code]').on('change', function(){
        var lang_select_e = $(this).closest('form').find('select[name=language_code]')
        lang_select_e.prop('disabled', true)
        $.ajax({
            type:'GET',
            url: '/api-connector/df/languages/google/'+$(this).val(),
            success:function(res){
                option_html = ''
                $(res.output).each(function(index, val){
                    option_html += `<option value='${val.language_code}'>${val.language_name}</option>`
                })
                lang_select_e.html(option_html)
                lang_select_e.prop('disabled', false)
            }
        })
    })
}