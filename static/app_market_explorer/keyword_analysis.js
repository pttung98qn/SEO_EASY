function test_func(){
    alert('connect')
}

function load_analysis_history(){
    $.ajax({
        type:'GET',
        url: get_history_endpoint,
        success:function(res){
            var table = $('#history_table')
            table.find('tbody').html(res.result_data)
            table.attr('total-count',res.total_count)
            table.attr('current-count', res.current_count)
            table.attr('num-pages',res.num_pages)
            table.tableAction(
                {
                    load_data_url:get_history_endpoint,
                    more_action:[{
                        button:'<button class="btn btn-outline-danger">Test</button>',
                        action:test_func
                    }]
                }
            )
            
        }
    })
}