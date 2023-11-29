function research_submit(){
    $('#research-form .search-btn').on('click',function(){
        var search_text = $('#research-form input[name=keyword]').val().trim()
        if(search_text!=''){                
            $(this).replaceWith(`
            <button disabled class="btn btn-success btn-load form-control search-btn">
                <span class="d-flex align-items-center">
                    <span class="spinner-border flex-shrink-0" role="status">
                        <span class="visually-hidden"></span>
                    </span>
                    <span class="flex-grow-1 ms-2">
                        Loading...
                    </span>
                </span>
            </button>             
            `)
            $('#research-form').submit()
        }
    })
}