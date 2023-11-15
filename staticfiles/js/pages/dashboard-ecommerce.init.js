function getChartColorsArray(e){var t=document.getElementById(e);if(t){t=t.dataset.colors;if(t)return JSON.parse(t).map(e=>{var t=e.replace(/\s/g,"");return t.includes(",")?2===(e=e.split(",")).length?`rgba(${getComputedStyle(document.documentElement).getPropertyValue(e[0])}, ${e[1]})`:t:getComputedStyle(document.documentElement).getPropertyValue(t)||t});console.warn("data-colors attribute not found on: "+e)}}var totalRevenueChart="",totalEarningsChart="",averageDailySalesChart="",totalOrdersChart="",revenueOverviewChart="",realTimeSalesChart="",salesTrafficSourceChart="",onlineStoreChart="",chartBarChart="";function loadCharts(){(e=getChartColorsArray("average_daily_sales"))&&(r={series:[76],chart:{type:"radialBar",height:260,sparkline:{enabled:!0}},plotOptions:{radialBar:{startAngle:-90,endAngle:90,track:{background:"#e7e7e7",strokeWidth:"80%"},dataLabels:{name:{show:!1},value:{offsetY:-15,fontWeight:"bold",fontSize:"18px"}}}},grid:{padding:{top:-20}},fill:{type:"gradient",gradient:{shade:"light",shadeIntensity:.4,inverseColors:!1,opacityFrom:1,opacityTo:1,stops:[0,50,53,91]}},labels:["Average Results"],colors:e},""!=averageDailySalesChart&&averageDailySalesChart.destroy(),(averageDailySalesChart=new ApexCharts(document.querySelector("#average_daily_sales"),r)).render()),(e=getChartColorsArray("total_revenue"))&&(a={series:[{data:[24,43,51,66,49,33,48,66]}],chart:{type:"line",height:70,sparkline:{enabled:!0}},colors:e,stroke:{curve:"smooth",width:2},tooltip:{fixed:{enabled:!1},x:{show:!1},y:{title:{formatter:function(e){return""}}},marker:{show:!1}}},""!=totalRevenueChart&&totalRevenueChart.destroy(),(totalRevenueChart=new ApexCharts(document.querySelector("#total_revenue"),a)).render()),(e=getChartColorsArray("total_earnings"))&&(r={series:[{name:"Total Earnings",data:[.7,1,.8,1.4,2.3,3.2,3.6,4,5.1,4,3.1,4.3]}],chart:{height:70,type:"bar",toolbar:{show:!1},sparkline:{enabled:!0}},xaxis:{categories:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]},colors:e,yaxis:{labels:{show:!1,formatter:function(e){return e+"k"}}}},""!=totalEarningsChart&&totalEarningsChart.destroy(),(totalEarningsChart=new ApexCharts(document.querySelector("#total_earnings"),r)).render()),(e=getChartColorsArray("total_orders"))&&(a={series:[{data:[36,21,45,53,39,55,67,58]}],chart:{type:"line",height:70,sparkline:{enabled:!0}},colors:e,stroke:{curve:"stepline",width:2},tooltip:{fixed:{enabled:!1},x:{show:!1},y:{title:{formatter:function(e){return""}}},marker:{show:!1}}},""!=totalOrdersChart&&totalOrdersChart.destroy(),(totalOrdersChart=new ApexCharts(document.querySelector("#total_orders"),a)).render());function t(e){var t=document.querySelectorAll("button");Array.prototype.forEach.call(t,function(e){e.classList.remove("active")}),e.target.classList.add("active")}(e=getChartColorsArray("real_time_sales"))&&(r={chart:{height:275,type:"bar",stacked:!0,toolbar:{show:!1}},plotOptions:{bar:{horizontal:!1,columnWidth:"45%",endingShape:"rounded"}},dataLabels:{enabled:!1},stroke:{show:!0,width:1,colors:["transparent"]},legend:{show:!1},series:[{name:"Search Engine Traffic",data:[74,83,89,97,97,97,74]},{name:"Direct Traffic",data:[46,57,59,54,97,97,84]}],colors:e,xaxis:{categories:["Feb","Mar","Apr","May","Jun","Jul","Aug"]},yaxis:{show:!0},grid:{show:!0,padding:{right:0},borderColor:"#000",xaxis:{lines:{show:!0}},yaxis:{lines:{show:!1}}}},""!=realTimeSalesChart&&realTimeSalesChart.destroy(),(realTimeSalesChart=new ApexCharts(document.querySelector("#real_time_sales"),r)).render());var e,r,a=getChartColorsArray("world-map-line-markers");a&&(document.getElementById("world-map-line-markers").innerHTML="",new jsVectorMap({map:"world_merc",selector:"#world-map-line-markers",zoomOnScroll:!1,zoomButtons:!1,markers:[{name:"Greenland",coords:[72,-42]},{name:"Canada",coords:[56.1304,-106.3468]},{name:"Brazil",coords:[-14.235,-51.9253]},{name:"Serbia",coords:[44.0165,21.0059]},{name:"Russia",coords:[61,105]},{name:"United States",coords:[37.0902,-95.7129]}],regionStyle:{initial:{stroke:"#9599ad",strokeWidth:.25,fill:a,fillOpacity:1}},labels:{markers:{render(e,t){return e.name||e.labelName||"Not available"}}}})),(e=getChartColorsArray("revenue_overview"))&&(r={series:[{name:"Total Revenue",type:"area",data:[[13462776e5,31.46],[1346364e6,31.27],[13467096e5,31.43],[1346796e6,32.26],[13468824e5,32.79],[13469688e5,32.46],[1347228e6,32.13],[13473144e5,32.43],[13474008e5,32.42],[13474872e5,32.81],[13475736e5,33.34],[13478328e5,33.41],[13479192e5,32.57],[13480056e5,33.12],[1348092e6,34.53],[13481784e5,33.83],[13484376e5,33.41],[1348524e6,32.9],[13486104e5,32.53],[13486968e5,32.8],[13487832e5,32.44],[13490424e5,32.62],[13491288e5,32.57],[13492152e5,32.6],[13493016e5,32.68],[1349388e6,32.47],[13496472e5,32.23],[13497336e5,31.68],[134982e7,31.51],[13499064e5,31.78],[13499928e5,31.94],[1350252e6,32.33],[13503384e5,33.24],[13504248e5,33.44],[13505112e5,33.48],[13505976e5,33.24],[13508568e5,33.49],[13509432e5,33.31],[13510296e5,33.36],[1351116e6,33.4],[13512024e5,34.01],[1351638e6,34.02],[13517244e5,34.36],[13518108e5,34.39],[135207e7,34.24],[13521564e5,34.39],[13522428e5,33.47],[13523292e5,32.98],[13524156e5,32.9],[13526748e5,32.7],[13527612e5,32.54],[13528476e5,32.23],[1352934e6,32.64],[13530204e5,32.65],[13532796e5,32.92],[1353366e6,32.64],[13534524e5,32.84],[13536252e5,33.4],[13538844e5,33.3],[13539708e5,33.18],[13540572e5,33.88],[13541436e5,34.09],[135423e7,34.61],[13544892e5,34.7],[13545756e5,35.3],[1354662e6,35.4],[13547484e5,35.14],[13548348e5,35.48],[1355094e6,35.75],[13551804e5,35.54],[13552668e5,35.96],[13553532e5,35.53],[13554396e5,37.56],[13556988e5,37.42],[13557852e5,37.49],[13558716e5,38.09],[1355958e6,37.87],[13560444e5,37.71],[13563036e5,37.53],[13564764e5,37.55],[13565628e5,37.3],[13566492e5,36.9],[13569084e5,37.68],[13570812e5,38.34],[13571676e5,37.75],[1357254e6,38.13],[13575132e5,37.94],[13575996e5,38.14],[1357686e6,38.66],[13577724e5,38.62],[13578588e5,38.09],[1358118e6,38.16],[13582044e5,38.15],[13582908e5,37.88],[13583772e5,37.73],[13584636e5,37.98],[13588092e5,37.95],[13588956e5,38.25],[1358982e6,38.1],[13590684e5,38.32],[13593276e5,38.24],[1359414e6,38.52],[13595004e5,37.94],[13595868e5,37.83],[13596732e5,38.34],[13599324e5,38.1],[13600188e5,38.51],[13601052e5,38.4],[13601916e5,38.07],[1360278e6,39.12],[13605372e5,38.64],[13606236e5,38.89],[136071e7,38.81],[13607964e5,38.61],[13608828e5,38.63],[13612284e5,38.99],[13613148e5,38.77],[13614012e5,38.34],[13614876e5,38.55],[13617468e5,38.11],[13618332e5,38.59],[13619196e5,39.6]]},{name:"Total Earnings",type:"line",data:[[13462776e5,39.6],[1346364e6,38.59],[13467096e5,38.11],[1346796e6,38.55],[13468824e5,38.34],[13469688e5,38.77],[1347228e6,38.99],[13473144e5,38.63],[13474008e5,38.61],[13474872e5,38.81],[13475736e5,38.89],[13478328e5,38.64],[13479192e5,39.12],[13480056e5,38.07],[1348092e6,38.4],[13481784e5,38.51],[13484376e5,38.1],[1348524e6,38.34],[13486104e5,37.83],[13486968e5,37.94],[13487832e5,38.52],[13490424e5,38.24],[13491288e5,38.32],[13492152e5,38.1],[13493016e5,38.25],[1349388e6,37.95],[13496472e5,37.98],[13497336e5,37.73],[134982e7,37.88],[13499064e5,38.15],[13499928e5,38.16],[1350252e6,38.09],[13503384e5,38.62],[13504248e5,38.66],[13505112e5,38.14],[13505976e5,37.94],[13508568e5,38.13],[13509432e5,37.75],[13510296e5,38.34],[1351116e6,37.68],[13512024e5,36.9],[1351638e6,37.3],[13517244e5,37.55],[13518108e5,37.53],[135207e7,37.71],[13521564e5,37.87],[13522428e5,38.09],[13523292e5,37.49],[13524156e5,37.42],[13526748e5,37.56],[13527612e5,35.53],[13528476e5,35.96],[1352934e6,35.54],[13530204e5,35.75],[13532796e5,35.48],[1353366e6,35.14],[13534524e5,35.4],[13536252e5,35.3],[13538844e5,34.7],[13539708e5,34.61],[13540572e5,34.09],[13541436e5,33.88],[135423e7,33.18],[13544892e5,33.3],[13545756e5,33.4],[1354662e6,32.84],[13547484e5,32.64],[13548348e5,32.92],[1355094e6,32.65],[13551804e5,32.64],[13552668e5,32.23],[13553532e5,32.54],[13554396e5,32.7],[13556988e5,32.9],[13557852e5,32.98],[13558716e5,33.47],[1355958e6,34.39],[13560444e5,34.24],[13563036e5,34.39],[13564764e5,34.36],[13565628e5,34.02],[13566492e5,34.01],[13569084e5,33.4],[13570812e5,33.36],[13571676e5,33.31],[1357254e6,33.49],[13575132e5,33.24],[13575996e5,33.48],[1357686e6,33.44],[13577724e5,33.24],[13578588e5,32.33],[1358118e6,31.94],[13582044e5,31.78],[13582908e5,31.51],[13583772e5,31.68],[13584636e5,32.23],[13588092e5,32.47],[13588956e5,32.68],[1358982e6,32.6],[13590684e5,32.57],[13593276e5,32.62],[1359414e6,32.44],[13595004e5,32.8],[13595868e5,32.53],[13596732e5,32.9],[13599324e5,33.41],[13600188e5,34.53],[13601052e5,33.12],[13601916e5,32.57],[1360278e6,33.41],[13605372e5,35.34],[13606236e5,37.89],[136071e7,38.81],[13607964e5,38.61],[13608828e5,37.63],[13612284e5,38.99],[13613148e5,38.77],[13614012e5,38.34],[13614876e5,38.55],[13617468e5,34.43],[13618332e5,37.27],[13619196e5,35.46]]}],chart:{id:"area-datetime",type:"line",height:300,toolbar:{show:!1},zoom:{autoScaleYaxis:!0}},stroke:{width:2},colors:e,grid:{xaxis:{lines:{show:!1}},yaxis:{lines:{show:!1}},padding:{right:0}},yaxis:{tickAmount:4,min:25,max:45,labels:{formatter:function(e){return e+"k"}}},legend:{position:"top",horizontalAlign:"center"},dataLabels:{enabled:!1},markers:{size:0,style:"hollow"},xaxis:{type:"datetime",min:new Date("01 Sep 2012").getTime(),tickAmount:6},tooltip:{x:{format:"dd MMM yyyy"}},fill:{type:["gradient","solid"],gradient:{type:"vertical",shade:"light",shadeIntensity:1,inverseColors:!1,opacityFrom:.3,opacityTo:.1,stops:[0,100]}}},""!=revenueOverviewChart&&revenueOverviewChart.destroy(),(revenueOverviewChart=new ApexCharts(document.querySelector("#revenue_overview"),r)).render()),document.querySelector("#one_month").addEventListener("click",function(e){t(e),revenueOverviewChart.zoomX(new Date("28 Jan 2013").getTime(),new Date("27 Feb 2013").getTime())}),document.querySelector("#three_months").addEventListener("click",function(e){t(e),revenueOverviewChart.zoomX(new Date("01 Dec 2012").getTime(),new Date("27 Feb 2013").getTime())}),document.querySelector("#six_months").addEventListener("click",function(e){t(e),revenueOverviewChart.zoomX(new Date("01 Sep 2012").getTime(),new Date("27 Feb 2013").getTime())}),document.querySelector("#all").addEventListener("click",function(e){t(e),revenueOverviewChart.zoomX(new Date("29 Aug 2012").getTime(),new Date("27 Feb 2013").getTime())}),(a=getChartColorsArray("sales_traffic_source"))&&(r={series:[59,40,44,31],labels:["Facebook","Instagram","YouTube","Google Ads"],chart:{height:267,type:"donut"},legend:{show:!1},dataLabels:{dropShadow:{enabled:!1}},colors:a},""!=salesTrafficSourceChart&&salesTrafficSourceChart.destroy(),(salesTrafficSourceChart=new ApexCharts(document.querySelector("#sales_traffic_source"),r)).render()),(e=getChartColorsArray("online_store"))&&(r={series:[{name:"Desktops",data:[10,41,35,51,49,62]}],chart:{height:290,type:"line",zoom:{enabled:!1},toolbar:{show:!1}},markers:{size:4},dataLabels:{enabled:!1},stroke:{curve:"smooth"},colors:e,xaxis:{categories:["Jan","Feb","Mar","Apr","May","Jun"]}},""!=onlineStoreChart&&onlineStoreChart.destroy(),(onlineStoreChart=new ApexCharts(document.querySelector("#online_store"),r)).render());(a=getChartColorsArray("bar_chart"))&&(r={chart:{height:140,type:"bar",toolbar:{show:!1}},plotOptions:{bar:{horizontal:!0}},dataLabels:{enabled:!1},series:[{name:"Income & Expenses",data:[599,510]}],labels:["Income","Expense"],colors:a,grid:{padding:{top:-20,right:0}},xaxis:{categories:["Income","Expense"]}},""!=chartBarChart&&chartBarChart.destroy(),(chartBarChart=new ApexCharts(document.querySelector("#bar_chart"),r)).render())}window.addEventListener("resize",function(){setTimeout(()=>{loadCharts()},250)}),loadCharts(),document.addEventListener("DOMContentLoaded",function(){Array.from(document.querySelectorAll(".launch-widgets")).forEach(function(n){var e=(new Date).getTime()+1e4,s=new Date(e).getTime(),i=setInterval(function(){var e=(new Date).getTime(),e=s-e,t=Math.floor(e/864e5),r=Math.floor(e%864e5/36e5),a=Math.floor(e%36e5/6e4),o=Math.floor(e%6e4/1e3);n&&(n.innerHTML='<div class="countdownlist-item"><div class="count-title">Days</div><div class="count-num">'+t+'</div></div><div class="countdownlist-item"><div class="count-title">Hours</div><div class="count-num">'+r+'</div></div><div class="countdownlist-item"><div class="count-title">Minutes</div><div class="count-num">'+a+'</div></div><div class="countdownlist-item"><div class="count-title">Seconds</div><div class="count-num">'+o+"</div></div>"),e<0&&(clearInterval(i),document.getElementById("countDownText").innerHTML=`<div class="card-body text-center">
                <div">
                    <div class="my-5 pt-3">
                        <img src="https://img.themesbrand.com/judia/comingsoon.png" alt="" style="max-height: 181px;">
                    </div>
                    <h5 class="text-white pt-4 text-xl">We've Launched your Product</h5>
                    <p class="text-white text-opacity-50">Click the below button to view your product.</p>
                    <a href="/" class="text-white icon-link icon-link-hover mt-1">View Product <i class="bi bi-arrow-right"></i></a>
                </div>
            </div>`)},1e3)})});var options={valueNames:["order_date","order_id","shop","customer","products","amount","status","rating"]},contactList=new List("contactList",options).on("updated",function(e){0==e.matchingItems.length?document.getElementsByClassName("noresult")[0].style.display="block":document.getElementsByClassName("noresult")[0].style.display="none",0<e.matchingItems.length?document.getElementsByClassName("noresult")[0].style.display="none":document.getElementsByClassName("noresult")[0].style.display="block"}),sorttableDropdown=document.querySelectorAll(".sortble-dropdown");sorttableDropdown&&sorttableDropdown.forEach(function(r){r.querySelectorAll(".dropdown-menu .dropdown-item").forEach(function(t){t.addEventListener("click",function(){var e=t.innerHTML;r.querySelector(".dropdown-title").innerHTML=e})})});