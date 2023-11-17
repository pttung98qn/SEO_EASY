function load_analysis_history(){
    $.ajax({
        type:'GET',
        url: get_history_endpoint,
        success:function(res){
            $('#history_table tbody').html(res.result_data)
            $('#history_table').attr('total-count',res.total_count).attr('current-count', res.current_count)

            $('#history_table').tableAction()
        }
    })
}