(function($){
    "use strict";
    var L = $.tableAction = {
        version: "1.0.0",
        config: {
            more_action:[]
        },
        run_data:{page:1,sort:'',search:''},
        current_data:{page:1,sort:'',search:''},
        configVerify: function(config){
            $.each(config, function(key, value){
                L.config[key]=value
            })
        },
        setup: function(table, config){
            L.table = table

            L.table_total_count = L.table.attr('total-count')
            L.table_current_count = L.table.attr('current-count')
            L.table_num_pages = L.table.attr('num-pages')
            L.select_all_checkbox = L.table.find('thead tr th input[type=checkbox]')

            L.configVerify(config)
            L.createTableTop()
            L.createTableAction()
            L.createTablePaginator()
            L.bindEvents()
        },
        createTableTop:function(){
            var table_top = `
            <div class="d-flex mb-1 table_top">
                <div class="flex-grow-1">
                    <div class="d-flex fs-sm">
                        <input type="checkbox" class="d-none" name="select_all">
                        <div class="p-1 selected_show" style="visibility:hidden">0 selected</div>
                        <div class="p-1 link-info btn p-0 select_all" style="visibility:hidden">select all</div>
                    </div>
                </div>
                <div class="flex-shrink-0">
                    <div class="input-group">
                        <input name="table_search" type="text" class="form-control" placeholder="Search...">
                        <span class="input-group-text"></span>
                    </div>
                </div>
            </div>`
            
            L.table_top = $(table_top)
            L.table.before(L.table_top)

            L.select_all_button = L.table_top.find('.select_all')
            L.selected_show = L.table_top.find('.selected_show')
            L.table_search = L.table_top.find('input[name=table_search]')
        },
        createTableAction:function(){
            var table_action = `
            <div class="fixed-bottom table_action d-none">
                <div class="layout-width mb-2 card p-1 shadow-lg rounded">
                    <div class="d-flex gap-3 action_group">
                    </div>
                </div>
            </div>
            `
            L.table_action = $(table_action)
            L.table_top.before(L.table_action)
            L.action_group = L.table_action.find('.action_group')
            
            L.cancel_action = $('<div class="btn btn-danger cancel_action">cancel</div>')
            L.action_group.append(L.cancel_action)
            L.cancel_action.on('click', function(){
                L.table.find('input[type=checkbox]').prop('checked', false)
                L.selectedShowAction()
            })
            $(L.config.more_action).each(function(index, button){
                var new_action = $(button.button)
                L.action_group.append(new_action)
                new_action.on('click', button.action)
            })
        },
        createTablePaginator:function(){
            if(L.paginator){
                L.paginator.remove()
            }
            if(L.table_num_pages<=1){
                return 0
            }
            var button_group = ''
            if(L.table_num_pages<=5){
                for(var i=1;i<=L.table_num_pages;i++){
                    var active = i==1?'active':''
                    button_group+=`<div page="${i}" class="btn btn-light page-nav page-item ${active}">${i}</div>`
                }
                button_group = `<div class="btn-group paginator" role="group">${button_group}</div>`
            }
            else{
                for(var i=1;i<=L.table_num_pages;i++){
                    var active = i==1?'active':''
                    button_group+=`<li><div page=${i} class="dropdown-item page-nav page-item ${active}">Page ${i}</div></li>`
                }
                button_group = `
                <div class="btn-group paginator" role="group">
                    <button page=1 disabled type="button" class="btn btn-light btn-icon prev-page page-nav"><i class="ri-arrow-left-s-line fs-xl"></i></button>
                    <div class="btn-group" role="group">
                        <button value=1 type="button" class="btn btn-light dropdown-toggle select-page" data-bs-toggle="dropdown" aria-expanded="false">page 1</button>
                        <ul style="max-height: 250px;" class="overflow-scroll dropdown-menu" aria-labelledby="btnGroupDrop1">${button_group}</ul>
                    </div>
                    <button page=2 type="button" class="btn btn-icon btn-light next-page page-nav"><i class="ri-arrow-right-s-line fs-xl"></i></button>
                </div>`
            }
            L.paginator = $(button_group)
            L.table.after(L.paginator)
            L.prev_page = L.paginator.find('.prev-page')
            L.next_page = L.paginator.find('.next-page')
            L.select_page = L.paginator.find('.select-page')
        },
        bindEvents: function(){
            L.table.find('thead input[type="checkbox"]:first').on('click', L.tableActionSelectAll)
            L.tableActionShiftSelect()
            L.select_all_button.on('click',L.selectAllClick)
            L.table.find('th.sort').on('click', L.clickSortTh)

            L.search_timeout
            L.table_search.on('keyup', function(event){L.tableSearch(event)})
            if(L.paginator){
                L.paginator.find('.page-nav').on('click', L.clickPaginatorItem)
            }
            
        },

        loadData:function(){
            if(L.current_data.page==L.run_data.page 
                & L.current_data.search==L.run_data.search 
                & L.current_data.sort==L.run_data.sort){
                return 0
            }
            L.table.find('tbody td').addClass('text-muted')
            L.table.find('tbody btn').prop('disabled',true)
            L.table.find('tbody a').addClass('link-opacity-25')

            var reload_paginator = L.current_data.search==L.run_data.search?false:true
            L.run_data.page = L.current_data.page
            L.run_data.search = L.current_data.search
            L.run_data.sort = L.current_data.sort

            $.ajax({
                type: 'GET',
                url: L.config.load_data_url,
                data: L.current_data,
                success: function(res){
                    L.table.find('tbody').html(res.result_data)
                    L.table_total_count = res.total_count
                    L.table_current_count = res.current_count
                    L.table_num_pages = res.num_pages
                    L.tableActionShiftSelect()

                    if(reload_paginator){
                        L.createTablePaginator()
                        if(L.paginator){
                            L.paginator.find('.page-nav').on('click', L.clickPaginatorItem)
                        }
                    }
                }
            })
        },
        clickPaginatorItem:function(){
            var page = parseInt($(this).attr('page'))
            if(L.paginator.find('ul.dropdown-menu').length>0){
                var prev_disabled = page==1?true:false
                var next_disabled = page==L.table_num_pages?true:false
                L.prev_page.prop('disabled',prev_disabled)
                L.next_page.prop('disabled',next_disabled)

                L.next_page.attr('page', page+1)
                L.prev_page.attr('page', page-1)
                L.select_page.text('Page '+page).attr('value', page)

                if(!$(this).hasClass('page-item')){
                    L.paginator.find('.page-item').removeClass('active')
                    L.paginator.find(`.page-item[page=${page}]`).addClass('active')
                }
            }
            if($(this).hasClass('page-item')){
                L.paginator.find('.page-item').removeClass('active')
                $(this).addClass('active')
            }
            
            L.current_data.page = $(this).attr('page')

            L.loadData()
            L.select_all_checkbox.prop('checked', false)
            L.selected_show.css({'visibility':'hidden'})
            L.select_all_button.css({'visibility':'hidden'})
        },
        clickSortTh:function(){
            L.table.find('th.sort').not(this).removeClass('desc asc')
            if($(this).hasClass('desc') | $(this).hasClass('asc')){
                $(this).toggleClass('desc asc')
            }
            else{
                $(this).addClass('asc')
            }
            var diment = $(this).hasClass('desc')?'-':''
            L.current_data.sort = diment+$(this).attr('key')

            L.loadData()
        },
        selectedShowAction:function(){
            var input_list = L.table.find('tbody tr td input[type=checkbox]:checked')
            var input_list_lenght = input_list.length
            if(input_list_lenght==0){
                L.selected_show.css({'visibility':'hidden'})
                L.table_action.addClass('d-none')
            }
            else{
                L.selected_show.css({'visibility':''})
                L.table_action.removeClass('d-none')
            }
            L.table_top.find('.selected_show').text(input_list_lenght+' of '+L.table_total_count+' selected')

            if(input_list_lenght==L.table_current_count){
                L.select_all_checkbox.prop('checked',true)
                if(input_list_lenght<L.table_total_count){
                    L.select_all_button.css({'visibility':''})
                }
            }
            else{
                L.select_all_checkbox.prop('checked',false)
                L.select_all_button.css({'visibility':'hidden'})
            }
        },
        tableSearch: function(event){
            L.current_data.search = $(event.target).val().trim()
            if(event.which===13){
                L.current_data.page=1
                L.loadData()
            }
            clearTimeout(L.search_timeout);
            L.search_timeout = setTimeout(function() {
                L.current_data.page=1
                L.loadData()
            }, 1000);
        },
        selectAllClick:function(){
            L.select_all_button.css({'visibility':'hidden'})
            L.selected_show.text('All '+L.table_total_count+' selected')
        },
        tableActionSelectAll:function(){
            if($(this).is(':checked')){
                L.table.find('tbody tr input[type="checkbox"]:visible').prop('checked', true)
                L.table.find('tbody tr:visible').addClass('selected')
            }
            else{
                L.table.find('tbody tr input[type="checkbox"]:visible').prop('checked', false)
                L.table.find('tbody tr:visible').removeClass('selected')
            }
            L.selectedShowAction()
        },
        tableActionShiftSelect: function(){
            let lastCheckedIndex = null
            const checkboxes = L.table.find('tbody input[type="checkbox"]')
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
                L.selectedShowAction()
                lastCheckedIndex = checkboxes.index(this)
            })
        },
    };
    $.fn.tableAction = function(t){
        L.setup($(this), t)
    }
})(jQuery);