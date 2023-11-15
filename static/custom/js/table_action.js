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
            L.bindEvents(table)
        },
        bindEvents: function(table){
            $(table).find('thead input[type="checkbox"]:first').on('click', L.tableActionSelectAll)
            L.tableActionShiftSelect(table)
        },
        tableActionSelectAll:function(){
            var table = $(this).closest('table')
            if($(this).is(':checked')){
                table.find('tbody tr input[type="checkbox"]:visible').prop('checked', true)
                table.find('tbody tr:visible').addClass('selected')
            }
            else{
                table.find('tbody tr input[type="checkbox"]:visible').prop('checked', false)
                table.find('tbody tr:visible').removeClass('selected')
            }
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
                lastCheckedIndex = checkboxes.index(this)
            })
        },
    };
    $.fn.tableAction = function(t){
        L.setup($(this), t)
    }
})(jQuery);