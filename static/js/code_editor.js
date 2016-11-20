var isHover = true;
// jQuery paging plugin
// 分頁顯示元件
// Version 1.01 (08/14/2013)
// @requires jQuery v1.4.2 or later
// Copyright (c) 2013 Qi-Liang Wen 啟良
(function(k,p,n){k.fn.paging=function(v,w){var t=this,s={setOptions:function(b){this.a=k.extend(this.a||{lapping:0,perpage:10,page:1,refresh:{interval:10,url:null},format:"",onFormat:function(){},onSelect:function(){return!0},onRefresh:function(){}},b||{});this.a.lapping|=0;this.a.perpage|=0;null!==this.a.page&&(this.a.page|=0);1>this.a.perpage&&(this.a.perpage=10);this.k&&p.clearInterval(this.k);this.a.refresh.url&&(this.k=p.setInterval(function(b){k.ajax({url:b.a.refresh.url,success:function(g){if("string"===typeof g)try{g=k.parseJSON(g)}catch(f){return}b.a.onRefresh(g)}})},1E3*this.a.refresh.interval,this));this.l=function(b){for(var g=0,f=0,h=1,d={e:[],h:0,g:0,b:5,d:3,j:0,m:0},a,l=/[*<>pq\[\]().-]|[nc]+!?/g,k={"[":"first","]":"last","<":"prev",">":"next",q:"left",p:"right","-":"fill",".":"leap"},e={};a=l.exec(b);){a=""+a;if(n===k[a])if("("===a)f=++g;else if(")"===a)f=0;else{if(h){if("*"===a){d.h=1;d.g=0}else{d.h=0;d.g="!"===a.charAt(a.length-1);d.b=a.length-d.g;if(!(d.d=1+a.indexOf("c")))d.d=1+d.b>>1}d.e[d.e.length]={f:"block",i:0,c:0};h=0}}else{d.e[d.e.length]={f:k[a],i:f,c:n===e[a]?e[a]=1:++e[a]};"q"===a?++d.m:"p"===a&&++d.j}}return d}(this.a.format);return this},setNumber:function(b){this.o=n===b||0>b?-1:b;return this},setPage:function(b){function q(b,a,c){c=""+b.onFormat.call(a,c);l=a.value?l+c.replace("<a",'<a data-page="'+a.value+'"'):l+c}if(n===b){if(b=this.a.page,null===b)return this}else if(this.a.page==b)return this;this.a.page=b|=0;var g=this.o,f=this.a,h,d,a,l,r=1,e=this.l,c,i,j,m,u=e.e.length,o=u;f.perpage<=f.lapping&&(f.lapping=f.perpage-1);m=g<=f.lapping?0:f.lapping|0;0>g?(a=g=-1,h=Math.max(1,b-e.d+1-m),d=h+e.b):(a=1+Math.ceil((g-f.perpage)/(f.perpage-m)),b=Math.max(1,Math.min(0>b?1+a+b:b,a)),e.h?(h=1,d=1+a,e.d=b,e.b=a):(h=Math.max(1,Math.min(b-e.d,a-e.b)+1),d=e.g?h+e.b:Math.min(h+e.b,1+a)));for(;o--;){i=0;j=e.e[o];switch(j.f){case"left":i=j.c<h;break;case"right":i=d<=a-e.j+j.c;break;case"first":i=e.d<b;break;case"last":i=e.b<e.d+a-b;break;case"prev":i=1<b;break;case"next":i=b<a}r|=i<<j.i}c={number:g,lapping:m,pages:a,perpage:f.perpage,page:b,slice:[(i=b*(f.perpage-m)+m)-f.perpage,Math.min(i,g)]};for(l="";++o<u;){j=e.e[o];i=r>>j.i&1;switch(j.f){case"block":for(;h<d;++h)c.value=h,c.pos=1+e.b-d+h,c.active=h<=a||0>g,c.first=1===h,c.last=h==a&&0<g,q(f,c,j.f);continue;case"left":c.value=j.c;c.active=j.c<h;break;case"right":c.value=a-e.j+j.c;c.active=d<=c.value;break;case"first":c.value=1;c.active=i&&1<b;break;case"prev":c.value=Math.max(1,b-1);c.active=i&&1<b;break;case"last":(c.active=0>g)?c.value=1+b:(c.value=a,c.active=i&&b<a);break;case"next":(c.active=0>g)?c.value=1+b:(c.value=Math.min(1+b,a),c.active=i&&b<a);break;case"leap":case"fill":c.pos=j.c;c.active=i;q(f,c,j.f);continue}c.pos=j.c;c.last=c.first=n;q(f,c,j.f)}t.length&&(k("a",t.html(l)).click(function(a){a.preventDefault();a=this;do if("a"===a.nodeName.toLowerCase())break;while(a=a.parentNode);s.setPage(k(a).data("page"));if(s.n)p.location=a.href}),this.n=f.onSelect.call({number:g,lapping:m,pages:a,slice:c.slice},b));return this}};return s.setNumber(v).setOptions(w).setPage()}})(jQuery,this);

// jQuery image resize plugin
// 圖片縮放顯示
// Version 1.03 (07/09/2012)
// @requires jQuery v1.4.2 or later
// Copyright (c) 2012 Qi-Liang Wen 啟良
(function($){$.fn.ScaleImg=function(settings){settings=jQuery.extend({width:0,height:0},settings);return this.each(function(){$(this).css("position","relative").css("vertical-align","text-top");var par=$(this).parent().get(0).tagName;if(par=="A"){if($(this).parent().css('display')!="block"){$par=$(this).parent().parent()}else{$par=$(this).parent()}}else{$par=$(this).parent()}$par.css("vertical-align","text-top").css("text-align","left");var h=$par.height();var w=$par.width();$.fn.ScaleImg.Run($(this),w,h);try{$(this).load(function(){$.fn.ScaleImg.Run($(this),w,h)})}catch(e){}})};$.fn.ScaleImg.Run=function($this,parentWidth,parentHeight){var src=$this.attr("src");var img=new Image();img.src=src;var w=0;var h=0;var _doScaling=function(){if(img.width>0&&img.height>0){if(img.width/img.height>=parentWidth/parentHeight){if(img.width>parentWidth){w=parentWidth;h=(img.height*parentWidth)/img.width}else{w=img.width;h=img.height}}else{if(img.height>parentHeight){w=(img.width*parentHeight)/img.height;h=parentHeight}else{w=img.width;h=img.height}}}$this.width(w);$this.height(h)};_doScaling();var loading=$("<span>Loading..</span>");$this.hide();$this.after(loading);loading.remove();$this.show();var objHeight=$this.height();var objWidth=$this.width();if(objWidth>parentWidth){$this.css("left",(objWidth-parentWidth)/2)}else{$this.css("left",(parentWidth-objWidth)/2)}if(objHeight>parentHeight){$this.css("top",(objHeight-parentHeight)/2)}else{$this.css("top",(parentHeight-objHeight)/2)}}})(jQuery);

// yooliang general function
// 侑良通用函式
// Version 1.03 (08/18/2012)
// @requires jQuery v1.4.2 or later
// Copyright (c) 2012 Qi-Liang Wen 啟良
function json(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: false,dataType:"json",data:data,async:!1,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?showNotify(d.message):errorCallback(d.message)}})};
function json_async(url,data,successCallback,errorCallback){$.ajax({url:url,type:"POST",cache: false,dataType:"json",data:data,async:1,success:function(a){successCallback(a)},error:function(b,c,d){void 0==errorCallback?showNotify(d.message):errorCallback(d.message)}})};
function ajax(url,data,successCallback,errorCallback){$.ajax({url:url,type:"GET",cache: false,data:data,async:true,success:function(responseText){successCallback(responseText)},error:function(xhr,ajaxOptions,thrownError){if(errorCallback){errorCallback(xhr.responseText)}else{window.alert(thrownError.message)}}})};
function html2text(){$(".html_2_text").each(function(){var text=$(this).text();var old_length=$(this).text().length;var length=50;if($(this).data("word-count")!=undefined){try{length=parseInt($(this).data("word-count"))}catch(e){}}if(length>0){$(this).text(text.substring(0,length));if(old_length>=length){$(this).text($(this).text()+"...")}}$(this).show()})};
function yooliang_replace_url_param(url,name,newvalue){url=url.replace("#/","");var old="";var m=url.substring(0,url.indexOf("?"));var s=url.substring(url.indexOf("?"),url.length);var j=0;if(url.indexOf("?")>=0){var i=s.indexOf(name+"=");if(i>=0){j=s.indexOf("&",i);if(j>=0){old=s.substring(i+name.length+1,j);s=url.replace(name+"="+old,name+"="+newvalue)}else{old=s.substring(i+name.length+1,s.length);s=url.replace(name+"="+old,name+"="+newvalue)}}else{s=url+"&"+name+"="+newvalue}}else{s=url+"?"+name+"="+newvalue}return s};
var target_id = "";
var target_path = "";
var target_type = "";

function showNotify(msg){
    top.message.quick_info(msg);
}

var code_editor = null;
function show_page(){
    var text = $("#history option:selected").text() || "新文件";
    var record_key = $("#history").val() || "";
    var url = "/code/editor?customer=" + target_id + "&file_type=" + target_type + "&record_key=" + record_key;
    $("#page_viewer").load(url, function(){
        showNotify("已載入 " + text);
        $('.codemirror').each(function(){
            var editor_id = $(this).attr("id");
            if (editor_id == undefined){
                editor_id = $(this).attr("name");
                $(this).attr("id", editor_id);
            }
            var mode = target_type;
            if (target_type == "html"){
                mode = "text/html"
            }
            console.log(mode);
            code_editor = CodeMirror.fromTextArea(document.getElementById(editor_id), {
                mode: mode,
                lineNumbers: true,
                indentUnit: 4,
                matchBrackets: true,
                foldGutter: true,
                autofocus: true,
                extraKeys: {
                    "Ctrl-S": function(cm){
                        if (target_id != "") {
                            $("#btn_1").click();
                        }
                    }
                },
                extra_keywords: ["sql", "response"]
            });
            code_editor.on('change',function(cMirror){
                // get value right from instance
                $("#" + editor_id).val(cMirror.getValue());
                $("#" + editor_id).change();
            });
        });
    });
}

function selectTheme(){
    var theme = $("#theme-select option:selected").text();
    code_editor.setOption("theme", theme);
}

function after_save(data){
    showNotify("已儲存");
    load();
}

function load(callback){
    $("#history").html("");
    json_async("/admin/code/records?target=" + target_id + "&content_type=" + target_type, null, function(data){
        $.map(data.records, function(item, index){
            var t =  item.modified.isoformat.replace("T", " ").split(".")[0];
            $("#history").append("<option value='" + item.__key__ + "'>" + item.title + " - " + t + "</option>");
        });
        if (typeof callback === "function"){
            callback(data);
        }
    });
}

$(function(){
    target_id = $("body").data("target-id");
    target_path = $("body").data("path");
    target_type = "html";
    if (target_path.indexOf(".js") > 0){
        target_type = "javascript";
    }
    if (target_path.indexOf(".css") > 0){
        target_type = "css";
    }
    load(function(){
        if ($("#history option").length > 0){
            $("#history option").eq(0).prop('selected', 'selected');
            $("#history").change();
        }else{
            show_page();
        }
    });
    $("#history").change(show_page);
    $("#btn_1").click(function(e){
        e.preventDefault();
        var d = $("form").serialize();
        json_async("/admin/code/save" , "target=" + target_id + "&file_type=" + target_type + "&" + d, after_save, after_save);
    });
});