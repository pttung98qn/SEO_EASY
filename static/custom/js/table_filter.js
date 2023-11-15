(function($){
    "use strict";
    var L = $.tableFilter = {
        version: "1.0.0",
        defaults: {
            right_board:[],
            disable:[],
            hideFollowHide:true,
            stickyTable:true,
            stickyCss:{
                'top':'36px',
                'z-index':'1'
            },
            data_type:null,
            moreActionHtml:[],
            rightActionHtml:[],
            replaceActionHtml:[],
            customColCss:{},
        },
        configVerify: function(config){
            
            config = !config?L.defaults:config
            config.disable = !config.disable?L.defaults.disable:config.disable
            if(config.hideFollowHide!=false){
                config.hideFollowHide = !config.hideFollowHide?L.defaults.hideFollowHide:config.hideFollowHide
            }
            config.right_board = !config.right_board?L.defaults.right_board:config.right_board
            if(config.stickyTable!=false){
                config.stickyTable = !config.stickyTable ? L.defaults.stickyTable : config.stickyTable
            }
            config.stickyCss = !config.stickyCss ? L.defaults.stickyCss : config.stickyCss
            config.moreActionHtml = !config.moreActionHtml ? L.defaults.moreActionHtml : config.moreActionHtml
            config.rightActionHtml = !config.rightActionHtml ? L.defaults.rightActionHtml : config.rightActionHtml
            config.data_type = !config.data_type ? L.defaults.data_type : config.data_type
            config.customColCss = !config.customColCss ? L.defaults.customColCss : config.customColCss
            return config
        },
        css:{
            table:"tableFilter",
            stickyTable:'stickyTable'
        },
        icon:{
            copy:'<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"> <path d="M15.75 15.7493H20.25V3.74927H8.25V8.24927" stroke="#606060" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/> <path d="M15.75 8.24951H3.75V20.2495H15.75V8.24951Z" stroke="#606060" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/> </svg>',
            export:'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="20" viewBox="0 0 24 24" fill="none"> <g clip-path="url(#clip0_1236_4177)"> <path d="M14 3V7C14 7.26522 14.1054 7.51957 14.2929 7.70711C14.4804 7.89464 14.7348 8 15 8H19" stroke="#606060" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/> <path d="M18 16L21 19L18 22M11.5 21H7C6.46957 21 5.96086 20.7893 5.58579 20.4142C5.21071 20.0391 5 19.5304 5 19V5C5 4.46957 5.21071 3.96086 5.58579 3.58579C5.96086 3.21071 6.46957 3 7 3H14L19 8V13L11.5 21ZM14 19H21H14Z" stroke="#606060" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/> </g> <defs><clipPath id="clip0_1236_4177"><rect width="24" height="24" fill="white"/></clipPath></defs> </svg>',
            filterOff:'<svg class="filterOff" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none"> <path d="M6 12H18" stroke="#606060" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/> <path d="M2.25 7.5H21.75" stroke="#606060" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/> <path d="M9.75 16.5H14.25" stroke="#606060" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/> </svg>',
            filterOn:'<svg stroke="black" class="filterOn hidden" xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none"> <path d="M6 12H18" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/> <path d="M2.25 7.5H21.75" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/> <path d="M9.75 16.5H14.25" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/> </svg>',
            tick:'<svg class="" width="15px" height="15px" fill="#000000" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 123.97 123.97" xml:space="preserve"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <path d="M51.802,96.062c2.801,2.801,6.5,4.2,10.2,4.2s7.4-1.399,10.2-4.2l47.3-47.3c5.5-5.5,6.101-14.6,0.8-20.3 c-5.6-6.1-15.1-6.3-20.899-0.5l-30.4,30.3c-3.899,3.9-10.2,3.9-14.1,0l-30.3-30.3c-5.801-5.8-15.301-5.7-20.9,0.5 c-5.3,5.7-4.8,14.8,0.8,20.3L51.802,96.062z"></path> </g> </g></svg>'
        },
        regex:{},
        toNumber: function(input){
            return Number(input);
        },
        dataFormat: function(data, type){
            if(type=='str'){
                return data
            }
            else if(type=='num'){
                return L.toNumber(data)
            }
        },
        detectDataType: function(table, config){
            var tbody = $(table).find("tbody")[0]
            var f_tr = $(tbody).find('tr')[0]
            var tds = $(f_tr).find('td')
        
            var output = {}
            $.map(tds, function(td, index){
                if(config.data_type && config.data_type.hasOwnProperty(index)){
                    output[index] = config.data_type[index]
                }
                else{
                    var td_text = $(td).text()
                    var td_num = L.toNumber(td_text);
                    output[index] = !isNaN(td_num)?"num":"str"
                }
            })
            return output
        },
        sortMethod: {
            str:function(a,b){a = a.toLowerCase();b = b.toLowerCase(); return a.localeCompare(b)},
            num:function(a,b){return a - b}
        },
        sort: function(data_type){
            return L.sortMethod[data_type]
        },
        compareString: {
            contains:{title: "Text contains",is: function(input, td_value){return td_value.indexOf(input)>-1?true:false}},
            not_contain:{title: "Does not contain",is: function(input, td_value){return td_value.indexOf(input)==-1?true:false}},
            starts_with:{title: "Starts with",is: function(input, td_value){return td_value.indexOf(input)==0?true:false}},
            ends_with:{title: "Ends with",is: function(input, td_value){return td_value.indexOf(input)+input.length==td_value.length?true:false}},
            excactly:{title: "Is excactly",is: function(input, td_value){return td_value==input?true:false}},
            diferent:{title: "Is diferent",is: function(input, td_value){return td_value!=input?true:false}},
        },
        compareNumber: {
            contains: {title: "Text contains",is: function(input, td_value){return td_value.indexOf(input)>-1?true:false}},
            equal:{title: "Is equal to",is: function(input, td_value){td_value=L.toNumber(td_value);return input==td_value?true:false}},
            not_equal:{title: "Is not equal to",is: function(input, td_value){td_value=L.toNumber(td_value);return input!=td_value?true:false}},
            between:{title: "Is between",is: function(f_input, t_input, td_value){
                td_value=L.toNumber(td_value)
                if(!td_value){return false}
                if(!f_input && !t_input){return true}
                else if(!f_input){return td_value<=t_input?true:false}
                else if(!t_input){return td_value>=f_input?true:false}
                else{return td_value>=f_input&&td_value<=t_input?true:false}}
            },
            not_between:{title: "Is not between",is: function(f_input, t_input, td_value){
                td_value=L.toNumber(td_value);
                if(!td_value){return false}
                if(!f_input && !t_input){return true}
                else if(!f_input){return td_value>t_input?true:false}
                else if(!t_input){return td_value<f_input?true:false}
                else{return td_value<f_input||td_value>t_input?true:false}}
            },
            greater:{title: "Greater than",is: function(input, td_value){td_value=L.toNumber(td_value); return td_value>input?true:false}},
            greater_or_equal:{title: "Greater than or equal to",is: function(input, td_value){td_value=L.toNumber(td_value); return td_value>=input?true:false}},
            less:{title: "Less than",is: function(input, td_value){td_value=L.toNumber(td_value); return td_value<input?true:false}},
            less_or_equal:{title: "Less than or equal to",is: function(input, td_value){td_value=L.toNumber(td_value); return td_value<=input?true:false}},
        },
        compareDetect: function(data_type){
            if(data_type=='str'){
                return L.compareString
            }
            else if (data_type=='num'){
                return L.compareNumber
            }
        },
        setup: function(table, config){
            var config = L.configVerify(config)

            $(table).addClass(L.css.table)
            if(config.stickyTable==true){
                $(table).addClass(L.css.stickyTable)
                $(table).find('thead').css(config.stickyCss)
            }
            $(table).find('.FilterTr').remove()
            L.setupRowId(table)
            L.tableFilterRowCreate(table, config)
            if($(table).prev().hasClass('tableAction')){
                
            }
            else{
                L.tableActionBuild(table, config)
            }
            L.bindEvents(table)
        },
        setupRowId: function(table){
            var trs = $(table).find('tbody').first().find('tr')
            $.each(trs, function(index, item){$(item).attr('row-id', index)})
        },
        tableFilterRowCreate: function(table, config){
            var data_type = L.detectDataType(table, config)
            var thead = $(table).find("thead")[0]
            var tr = $(thead).find('tr')[0]
            var ths = $(tr).find('th, td')
            var new_tr = $('<tr class="FilterTr tablesorter-ignoreRow"></tr>')
            var new_td, c_css
            if(config.hideFollowHide==true){
                for(let i = 0;i<ths.length;i++){
                    if(config.disable.indexOf(i)>-1){
                        $(ths[i]).addClass('sorter-false')
                    }

                    c_css = config.customColCss.hasOwnProperty(i)?config.customColCss[i]:''
                    if($(ths[i]).is(':visible')){
                        new_td = config.disable.indexOf(i)>-1?$('<td class="'+c_css+'"></td>'):$('<td class="'+c_css+'">'+L.filterBoardBuild(i, data_type[i], config)+'</td>')
                    }
                    else{
                        new_td = config.disable.indexOf(i)>-1?$('<td class="d-none '+c_css+'"></td>'):$('<td class="d-none '+c_css+'">'+L.filterBoardBuild(i, data_type[i], config)+'</td>')
                    }
                    $(new_tr).append(new_td)
                }
            }
            else{
                for(let i = 0;i<ths.length;i++){
                    if(config.disable.indexOf(i)>-1){
                        $(ths[i]).addClass('sorter-false')
                    }
                    c_css = config.customColCss[i]?config.customColCss.hasOwnProperty(i):''
                    new_td = config.disable.indexOf(i)>-1?$('<td class="'+c_css+'"></td>'):$('<td class="'+c_css+'">'+L.filterBoardBuild(i, data_type[i], config)+'</td>')
                    $(new_tr).append(new_td)
                }
            }
            
            $(thead).append(new_tr)
        },
        inputElement:function(place_holder, type, class_name){
            return '<input class="'+class_name+'" type="'+type+'" placeholder="'+place_holder+'">'
        },
        rangeInputElement:function(type){
            return '<div class="rangeInput hidden">'+L.inputElement('from...', type, 'inputFrom')+L.inputElement('to...', type, 'inputTo')+'</div>'
        },
        compareTypeSelect:function(compareType){
            var options = ''
            $.each(compareType,function(key, value){options+= '<option value="'+key+'">'+value.title+'</option>'})
            return '<select class="compareSwitchType">'+options+'</select>'
        },
        stringInput: function(){return L.compareTypeSelect(L.compareString)+L.inputElement("text", "search...", "sigleInput")},
        numberInput: function(){
            return L.compareTypeSelect(L.compareNumber)+L.inputElement("number", "value...", "sigleInput")+L.rangeInputElement('number')
        },
        filterBoardBuild: function(column, data_type, config){
            var elements = data_type == 'str'?L.stringInput(data_type):L.numberInput(data_type)
            var right_css = config.right_board.indexOf(column)==-1?'left':'right'
            var filterReset = '<div class="filterReset hidden">X</div>'
            var filterIcon = '<div class="filterIcon">'+L.icon.filterOff+L.icon.filterOn+'</div>'
            var filterAction = '<div class="filterAction"><div class="filterCancel">Cancel</div> <div class="filterSubmit">OK</button></div>'
            var filterResultAction = '<div class="filterResultAction"><div class="selectAll">Sellect all</div><div class="ClearAll">Clear all</div></div>'
            var filterResult = '<div class="filterResult"></div>'
            var filterInput = '<div class="filterInput '+right_css+' hidden">'+elements+filterResultAction+filterResult+filterAction+'</div>'
            var mainBoard = '<div class="mainBoard">'+filterIcon+filterInput+'</div>'
            return '<div class="filterBoard" data-type='+data_type+' column-filter="'+column+'">'+mainBoard+filterReset+'</div>'
        },
        tableDetect: function(button){
            return $(button).closest('.tableAction').nextAll('table').first()
        },
        
        tableActionBuild: function(table, config){

            var cancel = '<button class="cancel hidden for_select">Cancel</button>'
            var copy = '<button class="copy for_select" disabled=true>'+L.icon.copy+'Copy</button>'
            var export_e = '<button class="export for_select" disabled=true>'+L.icon.export+'Export</button>'
            
            var moreAction = config.moreActionHtml.join('')
            var rightAction = config.rightActionHtml.join('')
            var actionBoard = '<div class="tableAction"><div class="leftAction">'+cancel+copy+export_e+moreAction+'</div><div class="rightAction">'+rightAction+'</div></div>'
            table.before(actionBoard)
        },
        bindEvents: function(table){
            $(table).find('.filterBoard .filterIcon').on("click", L.showFilterBoard)
            $(table).find('.filterBoard .filterIcon').hover(function(){L.filterOnOffIcon($(this).closest('.filterBoard'), 'on')}, function(){L.filterOnOffIcon($(this).closest('.filterBoard'), 'off')})
            $(table).find('.filterBoard .filterCancel').on("click", L.showFilterBoard)
            $(table).find('.filterBoard .filterSubmit').on("click", L.filterRun)
            $(table).find('.filterBoard[data-type="num"] .compareSwitchType').on("change", L.numberSwitchCompareType)
            $(table).find('.filterBoard[data-type="str"] .compareSwitchType').on("change", L.stringSwitchCompareType)
            $(table).find('.filterBoard input').on("input", L.filterSearch)
            $(table).find('.filterBoard .FilterSubmit').on("click", L.RunFilter)
            $(table).find('.filterBoard input').on('change', L.filterSearch)
            $(table).find('.filterBoard .filterResultAction div').on('click', L.filterResultActionClick)
            $(table).find('.filterBoard .filterReset').on('click', L.clearFilterClick)

            $(table).prev().find('.cancel').on('click', L.tableActionCancel)
            $(table).prev().find('.export').on('click', L.tableActionExport)
            $(table).prev().find('.copy').on('click', L.tableActionCopy)
            $(table).find('thead input[type="checkbox"]:first').on('click', L.tableActionSelectAll)

            $(table).on('update', function(){L.updateAll(table)})

            L.clickOutside(table)
            L.tableActionShiftSelect(table)
            // L.tableSelectRow(table)
        },

        clickOutside : function(table){
            var filterBoard = $('.filterBoard')
            var dropdown_group = $('.dropdown-group')
            $(document).on('click', function(event) {
                if (!filterBoard.is(event.target) && filterBoard.has(event.target).length === 0) {
                    $(filterBoard).find('.filterInput').addClass('hidden')
                }
                if (!dropdown_group.is(event.target) && dropdown_group.has(event.target).length === 0) {
                    $(dropdown_group).find('.dropdown-board').addClass('hidden')
                }
            });
            

        },
        // tableSelectRow: function(table){
        //     function selectRows(start, end) {
        //         const rows = table.find('tr').not('td tr');
        //         for (let i = 0; i < rows.length; i++) {
        //             if (i >= Math.min(start, end) && i <= Math.max(start, end)) {
        //                 $(rows[i]).addClass('selected')
        //                 $(rows[i]).find('input[type="checkbox"]').prop('checked', true);
        //             } else {
        //                 $(rows[i]).removeClass('selected')
        //                 $(rows[i]).find('input[type="checkbox"]').prop('checked', false);
        //             }
        //         }
        //         var tableAction = table.prev()
        //         $(tableAction).find('.cancel').removeClass('hidden')
        //         $(tableAction).find('button').prop('disabled',false)
        //         $(tableAction).find('.copy').html(L.icon.copy+'Copy')
        //     }
        //     let isDragging = false;
        //     let startRowIndex, endRowIndex;

        //     table.on('mousedown', 'tbody td', function(e){
        //         isDragging = true;
        //         startRowIndex = endRowIndex = e.target.parentNode.rowIndex;
        //         e.target.classList.add('selected');
        //     });

        //     table.on('mousemove', (e) => {
        //         if (isDragging) {
        //             endRowIndex = e.target.parentNode.rowIndex;
        //             if(endRowIndex!=startRowIndex){
        //                 selectRows(startRowIndex, endRowIndex);
        //             }
        //             e.preventDefault();
        //         }
        //     });
        //     document.addEventListener('mouseup', () => {
        //         isDragging = false;
        //     });
        // },
        tableActionOnOff: function(table){
            var tableAction = table.prev()
            tableAction.find('.copy').html(L.icon.copy+'Copy')
            if(table.find('tr.selected').length>0){
                tableAction.find('button.for_select').prop('disabled',false)
                tableAction.find('.cancel').removeClass('hidden')
            }
            else{
                tableAction.find('button.for_select').prop('disabled',true)
                tableAction.find('.cancel').addClass('hidden')
            }
        },
        tableActionCancel:function(){
            var table = L.tableDetect($(this))
            table.find('tr.selected').removeClass('selected')
            table.find('input[type="checkbox"]').prop('checked',false)

            L.tableActionOnOff(table)
        },
        tableHeadData:function(table){
            const head_data = []
            const head_tds = $(table).find('thead tr').first().find('th, td')
            head_tds.each(function(index, col){
                head_data.push($(this).text().trim())
            })
            return head_data
        },
        tableActionExport:function(){
            const table = L.tableDetect($(this))
            const rows = table.find('tr.selected')
            const csvRows = []
            const title = L.tableHeadData(table)

            csvRows.push(title.join(','))
            $.each(rows, function(index, element){
                const rowData = []
                $(element).find('th, td').each(function() {
                    rowData.push($(this).text().trim())
                })
                csvRows.push(rowData.join(','))
            })

            const csvContent = csvRows.join('\n')
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
            const csvUrl = URL.createObjectURL(blob)
            const downloadLink = $('<a>', {
                href: csvUrl,
                download: 'seoreporter_data.csv',
                style: 'display: none'
            })
            $('body').append(downloadLink)
            downloadLink[0].click()
            downloadLink.remove()
        },
        tableActionCopy:function(){
            const table = L.tableDetect($(this))

            const selectedRows = $(table).find('tr.selected')

            const rowData = [L.tableHeadData(table).join('\t')];

            selectedRows.each(function(index, row) {
                const cells = $(row).find('td');
                const rowValues = []
                cells.each(function() {
                    rowValues.push($(this).text().trim())
                })
                rowData.push(rowValues.join('\t'))
            });
            const clipboardData = rowData.join('\n')
            const dummyTextarea = $('<textarea>').val(clipboardData).appendTo('body').select();
            document.execCommand('copy');
            dummyTextarea.remove();
            $(this).html(L.icon.copy+'Copied')
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
            L.tableActionOnOff(table)
        },
        tableActionShiftSelect: function(table){
            $(document).ready(function() {
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
                    L.tableActionOnOff(table)
                    lastCheckedIndex = checkboxes.index(this)
                })
            })
        },
        filterOnOffIcon: function(filterBoard, on_off){
            var filterIcon = filterBoard.find('.filterIcon')
            if (on_off=='on'){
                $(filterIcon).find('.filterOff').addClass('hidden')
                $(filterIcon).find('.filterOn').removeClass('hidden')
            }
            else{
                $(filterIcon).find('.filterOff').removeClass('hidden')
                $(filterIcon).find('.filterOn').addClass('hidden')
            }
        },
        filterResetOnOff: function(filterBoard, on_off){
            var filterReset = filterBoard.find('.filterReset')
            if(on_off=='auto'){
                $(filterReset).toggleClass('hidden')
            }else if (on_off=='on'){
                $(filterReset).removeClass('hidden')
            }
            else{
                $(filterReset).addClass('hidden')
            }
        },
        showFilterBoard: function(){
            var filterBoard, filterInput
            filterBoard = $(this).closest('.filterBoard')
            filterInput = filterBoard.find('.filterInput')
            $('.filterBoard .filterInput').not(filterInput).addClass('hidden')
            $(filterInput).toggleClass('hidden')

            if($(filterInput).is(':visible') && $(filterInput).find('.filterResult .chooseItem').length==0){
                L.LoadPrevSearchResult($(this))
            }
        },
        numberSwitchCompareType: function(){
            var filterBoard, filterInput, input_value
            var option = $(this).val()
            filterBoard = $(this).closest('.filterBoard')
            filterInput = $(this).closest('.filterInput')

            if(option === 'between' || option === 'not_between'){
                $(filterInput).find('.rangeInput').removeClass('hidden')
                $(filterInput).find('.sigleInput').addClass('hidden')
                L.filterSearchRangeRun(filterBoard)
            }
            else{
                $(filterInput).find('.rangeInput').addClass('hidden')
                $(filterInput).find('.sigleInput').removeClass('hidden')
                input_value = $('.filterBoard .sigleInput').val()
                L.filterSearchRun(filterBoard)
            }
        },
        stringSwitchCompareType: function(){
            var filterBoard
            filterBoard = $(this).closest('.filterBoard')
            L.filterSearchRun(filterBoard)
        },
        getColumnValue: function(rows, column){
            return rows.map(function(row) {return $(row).find('td')[column].text()}).get()
        },
        filterResultActionClick:function(){
            var filterBoard, chooseItems, action
            filterBoard = $(this).closest('.filterBoard')
            chooseItems = $(filterBoard).find('.chooseItem:visible')
            action = $(this).attr('class')
            if(action=='selectAll'){
                chooseItems.addClass('active')
            }else{
                chooseItems.removeClass('active')
            }
        },
        SearchOn: function(filterResult){
            $(filterResult).html("<p>Loading...</p>")
        },
        prevItemClick: function(){
            $(this).toggleClass('active')
        },
        
        LoadPrevSearchResult:function(icon){
            var filterBoard,dataType, filterResult, value, trs, row_id_data, result_items, column, row_data
            filterBoard = $(icon).closest('.filterBoard')                
            dataType = filterBoard.attr('data-type')
            filterResult = $(filterBoard).find('.filterResult')
            column = filterBoard.attr('column-filter')
            L.SearchOn(filterResult)
            trs = filterBoard.closest('table').find('tbody').find('tr.main_row:visible, tr.main_row.f_hide__'+column)
            row_id_data = {}
            result_items = []
            $.each(trs, function(index, row){
                value = L.dataFormat($(row).find('td:eq('+column+')').text().toLowerCase().trim(), dataType)
                if(row_id_data.hasOwnProperty(value)){
                    row_id_data[value]['data'].push($(row).attr('row-id'))
                }
                else{
                    row_id_data[value] ={
                        data:[$(row).attr('row-id')],
                        active:$(row).hasClass('f_hide__'+column)==false?'active':''
                    }
                    result_items.push(value)
                }
            })            
            var options = ''
            var result_id, show_value, new_option
            var itemTick = '<div class="itemTick">'+L.icon.tick+'</div>'

            result_items.sort(L.sort(dataType))
            result_items.forEach(value=>{
                row_data = row_id_data[value]
                result_id = row_data.data.join(',')
                show_value = value==''?'(Blanks)':value
                show_value = '<div class="itemTitle">'+show_value+'</div>'
                new_option = '<div class="chooseItem '+row_data.active+'" row_id='+result_id+' content="'+value+'">'+itemTick+show_value+'</div>'
                options+=new_option
            })
            filterBoard.find(filterResult).first().html(options)
            $(filterResult).find('.chooseItem').on('click', L.prevItemClick)
        },

        filterSearch: function(){
            var filterBoard, type_select
            filterBoard = $(this).closest('.filterBoard')
            type_select = $(filterBoard).find('select').val()
            if(type_select!="between" && type_select!="not_between"){
                L.filterSearchRun(filterBoard)
            }
            else{
                L.filterSearchRangeRun(filterBoard)
            }
        },
        filterSearchRangeRun: function(filterBoard){
            var inputFrom, inputTo, compare_func, compare_option, chooseItems, data_type
            inputFrom = L.toNumber($(filterBoard).find('.inputFrom').val())
            inputTo = L.toNumber($(filterBoard).find('.inputTo').val())
            data_type = $(filterBoard).attr('data-type')
            compare_option = $(filterBoard).find('.compareSwitchType').val()
            compare_func = L.compareDetect(data_type)
            chooseItems = $(filterBoard).find('.chooseItem')
            var content
            compare_func = compare_func[compare_option]
            $.each(chooseItems, function(index, item){
                content = $(item).attr('content')
                if(compare_func.is(inputFrom,inputTo, content)==true){
                    $(item).removeClass('hidden')
                    $(item).addClass('active')
                }else{
                    $(item).addClass('hidden')
                    $(item).removeClass('active')
                }
            })
        },
        filterSearchRun: function(filterBoard){
            var input, compare_func, chooseItems, data_type, compare_option
            data_type = $(filterBoard).attr('data-type')
            compare_option = $(filterBoard).find('.compareSwitchType').val()
            input = $(filterBoard).find('input').first().val().toLowerCase()
            compare_func = L.compareDetect(data_type)
            compare_func = input==''?compare_func['contains']:compare_func[compare_option]

            chooseItems = $(filterBoard).find('.chooseItem')
            var content
            
            $.each(chooseItems, function(index, item){
                content = $(item).attr('content')
                if(compare_func.is(input, content)==true){
                    $(item).removeClass('hidden')
                    $(item).addClass('active')
                }
                else{
                    $(item).addClass('hidden')
                    $(item).removeClass('active')
                }
            })
        },
        filterRun: function(){
            var filterBoard, filterInput, filterResult,  hideRowId, tbody, trs, column, hide_css
            filterBoard = $(this).closest('.filterBoard')
            filterInput = $(filterBoard).find('.filterInput')
            filterResult = $(filterBoard).find('.filterResult')
            column = $(filterBoard).attr('column-filter')
            hide_css = 'f_hide__'+column
            hideRowId = []
            $.each($(filterBoard).find('.chooseItem:not(.active)'), function(index, item){
                hideRowId.push($(item).attr('row_id'))
            })
            hideRowId = hideRowId.join(',').split(',')
            
            tbody = $(this).closest('table').find('tbody').first()
            trs = tbody.find('tr').not('td tr')
            $.each(trs, function(index, tr){
                var rowId = $(this).attr('row-id')
                if($(tr).hasClass('detail_row')){
                    if($(tr).prev().hasClass(hide_css)){
                        $(tr).addClass(hide_css)
                    }
                    else{
                        $(tr).removeClass(hide_css)
                    }
                }
                else{
                    if($.inArray(rowId, hideRowId) == -1){
                        $(tr).removeClass(hide_css)
                    }else{
                        $(tr).addClass(hide_css)
                    }
                }
                
            })
            $(filterInput).addClass('hidden')
            $('.filterBoard .filterResult').not(filterResult).html('')
            L.filterResetOnOff(filterBoard, 'on')
            $('.filterBoard input').val("")

            if($(tbody).find('tr.'+hide_css).length==0){
                L.clearFilter(filterBoard)
            }
        },
        clearFilter: function(filterBoard){
            var column, trs, hide_css
            column = $(filterBoard).attr('column-filter')
            hide_css = 'f_hide__'+column
            trs = $(filterBoard).closest('table').find('tbody').first().find('tr.'+hide_css)
            trs.removeClass(hide_css)
            $('.filterBoard .filterResult').html('')
            L.filterResetOnOff(filterBoard, 'off')
            $('.filterBoard input').val("")
            $('.filterBoard .filterInput').addClass("hidden")
        },
        clearFilterClick: function(){
            var filterBoard = $(this).closest('.filterBoard')
            L.clearFilter(filterBoard)
        },
        updateAll:function(table){
            console.log("updateAll")
            L.setupRowId(table)
            L.tableActionShiftSelect(table)
        }
    };
    $.fn.tableFilter = function(t){
        L.setup($(this), t)
    }
})(jQuery);