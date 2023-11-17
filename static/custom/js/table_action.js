(function($){
    "use strict";
    var L = $.tableAction = {
        version: "1.0.0",
        defaults: {
        },
        configVerify: function(config){
            
        },
        setup: function(table, config){
            var config = L.configVerify(config)
            L.createSelectedShow(table)
            L.bindEvents(table)
        },
        createSelectedShow:function(table){
            var element = `<div class="d-flex fs-sm table_selected_info">
                            <input type="checkbox" class="d-none" name="select_all">
                            <div class="p-1 selected_show" style="visibility: hidden;">0 selected</div>
                            <div class="p-1 link-info btn p-0 select_all" style="visibility: hidden;">select all</div>
                        </div>`
            table.before(element)
            L.table_selected_info = table.prevAll('.table_selected_info').first()
            L.select_all_button = L.table_selected_info.find('.select_all')
            L.selected_show = L.table_selected_info.find('.selected_show')

            L.table_total_count = table.attr('total-count')
            L.table_current_count = table.attr('current-count')
            L.select_all_checkbox = table.find('thead tr th input[type=checkbox]')

        },
        bindEvents: function(table){
            $(table).find('thead input[type="checkbox"]:first').on('click', L.tableActionSelectAll)
            L.tableActionShiftSelect(table)
            L.select_all_button.on('click',L.selectAllClick)
        },
        selectedShowAction:function(table){
            var input_list = table.find('tbody tr td input[type=checkbox]:checked')
            var input_list_lenght = input_list.length
            
            if(input_list_lenght==0){
                L.selected_show.css({'visibility':'hidden'})
            }
            else{
                L.selected_show.css({'visibility':''})
            }
            L.table_selected_info.find('.selected_show').text(input_list_lenght+' of '+L.table_total_count+' selected')

            if(input_list_lenght==L.table_current_count){
                L.select_all_checkbox.prop('checked',true)
                L.select_all_button.css({'visibility':''})
            }
            else{
                L.select_all_checkbox.prop('checked',false)
                L.select_all_button.css({'visibility':'hidden'})
            }
        },
        selectAllClick:function(){
            L.select_all_button.css({'visibility':'hidden'})
            L.selected_show.text('All '+L.table_total_count+' selected')
        },
        tableActionSelectAll:function(table){
            var table = $(this).closest('table')
            if($(this).is(':checked')){
                table.find('tbody tr input[type="checkbox"]:visible').prop('checked', true)
                table.find('tbody tr:visible').addClass('selected')
            }
            else{
                table.find('tbody tr input[type="checkbox"]:visible').prop('checked', false)
                table.find('tbody tr:visible').removeClass('selected')
            }
            L.selectedShowAction(table)
        },
        tableActionShiftSelect: function(table){
            let lastCheckedIndex = null
            const checkboxes = $(table).find('tbody input[type="checkbox"]')
            checkboxes.click(function(event) {
                $(this).closest('tr').toggleClass('selected')
                if (event.shiftKey && lastCheckedIndex !== null) {
                    const clickedIndex = checkboxes.index(this)
                    const start = Math.min(clickedIndex, lastCheckedIndex)
                    const end = Math.max(clickedIndex, lastCheckedIndex)
                    checkboxes.slice(start, end + 1).each(function() {
                        if($(this).is(':visible')){
                            $(this).prop('checked', checkboxes.eq(clickedIndex).prop('checked'))
                            const row = $(this).closest('tr')
                            row.toggleClass('selected', $(this).prop('checked'))
                        }
                    })
                    
                }
                L.selectedShowAction(table)
                lastCheckedIndex = checkboxes.index(this)
            })
        },
    };
    $.fn.tableAction = function(t){
        L.setup($(this), t)
    }
})(jQuery);