(function($){undefined
    $.querycity = function(input,options){undefined
        var input = $(input);
        input.attr('autocomplete','off');
        if($.trim(input.val())=='' || $.trim(input.val())==options.defaultText){
            input.val(options.defaultText).css('color','#aaa');
        }
        var t_pop_focus = false;
        var t_suggest_focus = false;
        var t_suggest_page_click = false;
        $('body').append("<div id='pop_city_"+input.attr('id')+"' class='pop_city' style='display:none'><p class='pop_head'></p><ul class='list_label'></ul><div class='pop_city_container'></div></div>");
        $('body').append("<div id='suggest_city_"+input.attr('id')+"' class='list_city' style='display:none'><div class='list_city_head'></div><div class='list_city_container'></div><div class='page_break'></div></div>");
        var popMain = $("#pop_city_"+input.attr('id'))
        var popContainer = popMain.find('.pop_city_container');
        var labelMain = popMain.find('.list_label');
        var suggestMain = $("#suggest_city_"+input.attr('id'));
        popMain.bgIframe();
        suggestMain.bgIframe();
        popInit();
        resetPosition();     
       
        $(window).resize(function(){undefined
            resetPosition();
        });       
       
        input.focus(function(){undefined
            if(t_suggest_page_click){undefined
                t_suggest_page_click = false;
                return true;
            }
            suggestMain.hide();
      if($.trim($(this).val())==options.defaultText){undefined
       $(this).val('').css('color','#000');
      }
      popMain.show();
        }).click(function(){  
            if(t_suggest_page_click){undefined
                t_suggest_page_click = false;
                return;
            }
            suggestMain.hide();
      popMain.show();  
     }).blur(function(){    
      if(t_pop_focus == false){undefined
       popMain.hide();    
       if($.trim(input.val())=='' || $.trim(input.val())==options.defaultText){    
        input.val(options.defaultText).css('color','#aaa');
       }
      }
     });
        labelMain.find('a').live('click',function(){ 
      input.focus();//使焦点在输入框，避免blur事件无法触发
      t_pop_focus = true;
      var labelId = $(this).attr('id');
      labelMain.find('li a').removeClass('current');
      $(this).addClass('current');
      popContainer.find('ul').hide();
      $("#"+labelId+'_container').show();
     });
     popContainer.find('a').live('click',function(){undefined
      input.val($(this).html());
      popMain.hide();
     });
     popMain.mouseover(function(){ 
      t_pop_focus = true;
     }).mouseout(function(){ 
      t_pop_focus = false;
     });

        input.blur(function(){undefined
      if( t_suggest_focus == false ){undefined
       if($(this).val()==''){undefined
        $(this).val( suggestMain.find('.list_city_container a.selected').children('b').text());
       }
   suggestMain.hide();
      }
        }).keydown(function(event){undefined
            popMain.hide();
      event = window.event || event;
      var keyCode = event.keyCode || event.which || event.charCode;  
      if (keyCode == 37) {//左
                prevPage();   
            } else if (keyCode == 39) {//右
                nextPage();
            }else if(keyCode == 38){//上
                prevResult();
            }else if(keyCode == 40){//下
                 nextResult();
            }
     }).keypress(function(event){undefined
            event = window.event || event;
            var keyCode = event.keyCode || event.which || event.charCode;
            if(13 == keyCode){undefined
                if(suggestMain.find('.list_city_container a.selected').length > 0){undefined
                    input.val(suggestMain.find('.list_city_container a.selected').children('b').text());
                    suggestMain.hide();
                }
            }
        }).keyup(function(event){undefined
            event = window.event || event;
            var keyCode = event.keyCode || event.which || event.charCode;       
            if(keyCode != 13 && keyCode != 37 && keyCode != 39 && keyCode !=9 && keyCode !=38 && keyCode !=40 ){undefined
       //keyCode == 9是tab切换键
                queryCity();
            }
        });
     
        suggestMain.find('.list_city_container a').live('click',function(){undefined
            input.val($(this).children('b').text());
            suggestMain.hide();
        }).live('mouseover',function(){undefined
            t_suggest_focus = true;       
        }).live('mouseout',function(){undefined
            t_suggest_focus = false;
        });
        suggestMain.find('.page_break a').live('mouseover',function(){undefined
            t_suggest_focus = true;       
        }).live('mouseout',function(){undefined
            t_suggest_focus = false;
        });
     suggestMain.find('.page_break a').live('click',function(event){undefined
            t_suggest_page_click = true;
            input.click();
      if($(this).attr('inum') != null){undefined
       setAddPage($(this).attr('inum'));
      }
     });

        function nextPage(){undefined
              var add_cur= suggestMain.find(".page_break a.current").next();
                if (add_cur != null) {               
                    if ($(add_cur).attr("inum") != null) {undefined
                        setAddPage($(add_cur).attr("inum"));
                    }
                }
        }
        function prevPage(){undefined
                var add_cur = suggestMain.find(".page_break a.current").prev();
                if (add_cur != null) {undefined
                    if ($(add_cur).attr("inum") != null) {undefined
                        setAddPage($(add_cur).attr("inum"));
                    }
                }
        }
        function nextResult(){undefined
                  var t_index = suggestMain.find('.list_city_container a').index(suggestMain.find('.list_city_container a.selected')[0]);
                    suggestMain.find('.list_city_container').children().removeClass('selected');         
                    t_index += 1;
                    var t_end =  suggestMain.find('.list_city_container a').index( suggestMain.find('.list_city_container a:visible').filter(':last')[0]);
                    if(t_index > t_end ){undefined
                        t_index = suggestMain.find('.list_city_container a').index(suggestMain.find('.list_city_container a:visible').eq(0));
                    }
                    suggestMain.find('.list_city_container a').eq(t_index).addClass('selected');
        }
        function prevResult(){undefined
                
                     var t_index = suggestMain.find('.list_city_container a').index(suggestMain.find('.list_city_container a.selected')[0]);
                suggestMain.find('.list_city_container').children().removeClass('selected');
                t_index -= 1;
                var t_start = suggestMain.find('.list_city_container a').index(suggestMain.find('.list_city_container a:visible').filter(':first')[0]);
                if( t_index < t_start){undefined
                    t_index = suggestMain.find('.list_city_container a').index(suggestMain.find('.list_city_container a:visible').filter(':last')[0]);
                }
                suggestMain.find('.list_city_container a').eq(t_index).addClass('selected');     
        }
     function loadCity(){  
      var cityList = suggestMain.find('.list_city_container');  
      cityList.empty();
            if(options.hotList){undefined
                var hotList = options.hotList;
            }else{undefined
                var hotList = [0,1,2,3,4,5,6,7,8,9];
            }
      for(var item in hotList){undefined
       if(item>options.suggestLength){undefined
        return;
       }
       var _data = options.data[hotList[item]];
       cityList.append("<a href='javascript:void(0)' ><span>"+_data[2]+"</span><b>"+_data[1]+"</b></a>");
      }  
      suggestMain.find('.list_city_head').html(options.suggestTitleText);
            setAddPage(1);
      suggestMain.show();
      setTopSelect();
     }
     function queryCity(){undefined
            popMain.hide();
            var value = input.val().toLowerCase();
            if( value.length == 0){undefined
                loadCity();
                return;
            }
            var city_container = suggestMain.find('.list_city_container');       
      var isHave = false;
            var _tmp = new Array();
            for(var item in options.data){   
                var _data = options.data[item];  
                if(typeof (_data) != 'undefined'){undefined
                    if(_data[2].indexOf(value) >= 0 || _data[3].indexOf(value) >= 0 || _data[1].indexOf(value) >=0 || _data[0].indexOf(value) >=0 ){                       
                        isHave = true;
                        _tmp.push(_data);
                    }
                }
             }
;
      if(isHave){undefined
                city_container.empty();
                for(var item in _tmp){undefined
                var _data= _tmp[item];
                city_container.append("<a href='javascript:void(0)' style='display:none'><span>"+_data[2]+"</span><b>"+     _data[1] +"</b></a>");               
                }
       suggestMain.find('.list_city_head').html(value+",按拼音排序");
                setAddPage(1);
                setTopSelect()
      }else{undefined
       suggestMain.find('.list_city_head').html("<span class='msg'>对不起,找不到"+value+"</span>");
      }
            suggestMain.show();
     }
        function setAddPage(pageIndex){undefined
            suggestMain.find('.list_city_container a').removeClass('selected');
            suggestMain.find('.list_city_container').children().each(function(i){   
                var k = i+1;
                if(k> options.suggestLength*(pageIndex-1) && k <= options.suggestLength*pageIndex){undefined
                    $(this).css('display','block');
                }else{undefined
                    $(this).hide();   
                }
             });
            setTopSelect();
            setAddPageHtml(pageIndex);
        }
        function setAddPageHtml(pageIndex){undefined
            var cityPageBreak = suggestMain.find('.page_break');
            cityPageBreak.empty(); 
            if(suggestMain.find('.list_city_container').children().length > options.suggestLength){undefined
                var pageBreakSize = Math.ceil(suggestMain.find('.list_city_container').children().length/options.suggestLength); 
       if(pageBreakSize <= 1){undefined
        return;
       }   
                var start = end = pageIndex;
                for(var index = 0 ,num = 1 ; index < options.pageLength && num < options.pageLength; index++){undefined
                    if(start > 1){undefined
                        start--;num++;
                    }
                    if(end<pageBreakSize){undefined
                        end ++;num++;
                    }
                }
                if(pageIndex > 1){undefined
                    cityPageBreak.append("<a href='javascript:void(0)' inum='"+(pageIndex-1)+"'><-</a>");
                } 
                for(var i=start;i<=end;i++){undefined
                    if(i == pageIndex){undefined
                        cityPageBreak.append("<a href='javascript:void(0)' class='current' inum='"+(i)+"'>"+(i)+"</a");
                    }else{undefined
                        cityPageBreak.append("<a href='javascript:void(0)' inum='"+(i)+"'>"+(i)+"</a");
                    }       
             }        
       if (pageIndex<pageBreakSize) {undefined
                    cityPageBreak.append("<a href='javascript:void(0);' inum='"+ (i) +"'>-></a>");
                }
                cityPageBreak.show();          
            }else{undefined
                cityPageBreak.hide();   
            }
      return;
        }
     function setTopSelect(){  
      if(suggestMain.find('.list_city_container').children().length > 0 ){undefined
       suggestMain.find('.list_city_container').children(':visible').eq(0).addClass('selected');
      }
     }
        function onSelect(){undefined
            if( typeof options.onSelect == 'function'){undefined
                alert(1);
            }
        }
        function popInit(){undefined
            var index = 0;
            popMain.find('.pop_head').html(options.popTitleText);
            if(!options.tabs){undefined
                popContainer.append("<ul id='label_"+input.attr('id')+"_container' class='current'></ul>");
                labelMain.remove();
                for( var item in options.data){undefined
                      $("#label_"+input.attr('id')+"_container").append("<li><a href='javascript:void(0)'>"+options.data[item][1]+"</a></li>");
                }
                return;
            }
      for(var itemLabel in options.tabs){  
       index++;   
       if(index == 1){undefined
        popContainer.append("<ul id='label_"+input.attr('id')+index+"_container' class='current' data-type='"+itemLabel+"'></ul>");
        labelMain.append("<li><a id='label_"+input.attr('id')+index+"' class='current' href='javascript:void(0)'>"+itemLabel+"</a></li>");  
       }else{undefined
        popContainer.append("<ul style='display:none' id='label_"+input.attr('id')+index+"_container' data-type='"+itemLabel+"'></ul>");
        labelMain.append("<li><a id='label_"+input.attr('id')+index+"' href='javascript:void(0)'>"+itemLabel+"</a></li>");  
       }
       for(var item in options.tabs[itemLabel]){undefined
        var cityCode = options.tabs[itemLabel][item];
        if(!options.data[cityCode]){undefined
         break;
           }    
        $("#label_"+input.attr('id')+index+"_container").append("<li><a href='javascript:void(0)'>"+options.data[cityCode][1]+"</a></li>");
       }
      }   
        }
        function resetPosition(){undefined
            popMain.css({'top':input.position().top+input.outerHeight(),'left':input.position().left});
            suggestMain.css({'top':input.position().top+input.outerHeight(),'left':input.position().left});
        }
    }
    $.fn.querycity = function(options){undefined
        var defaults = {undefined
            'data'          : {},
            'tabs'          : '',
            'hotList'       : '',           
            'defaultText'   : '中文/拼音',
            'popTitleText'  : '请选择城市或输入城市名称的拼音或英文',
            'suggestTitleText' : '输入中文/拼音或↑↓选择',
            'suggestLength' : 10,
            'pageLength'    : 5,
            'onSelect'      : ''
        };
        var options = $.extend(defaults,options);
        this.each(function(){undefined
            new $.querycity(this,options);           
        });
        return this;
    };
})(jQuery);


(function($){undefined
$.fn.bgIframe = $.fn.bgiframe = function(s) {undefined
 if ( $.browser.msie && /6.0/.test(navigator.userAgent) ) {undefined
  s = $.extend({undefined
    top    : 'auto', // auto == .currentStyle.borderTopWidth
   left    : 'auto', // auto == .currentStyle.borderLeftWidth
   width   : 'auto', // auto == offsetWidth
   height  : 'auto', // auto == offsetHeight
   opacity : true,
   src     : 'javascript:false;'
  }, s || {});
  var prop = function(n){return n&&n.constructor==Number?n+'px':n;},
      html = '<iframe class="bgiframe"frameborder="0"tabindex="-1"src="'+s.src+'"'+
                 'style="display:block;position:absolute;z-index:-1;'+
                  (s.opacity !== false?'filter:Alpha(Opacity=\'0\');':'')+
            'top:'+(s.top=='auto'?'expression(((parseInt(this.parentNode.currentStyle.borderTopWidth)||0)*-1)+\'px\')':prop(s.top))+';'+
            'left:'+(s.left=='auto'?'expression(((parseInt(this.parentNode.currentStyle.borderLeftWidth)||0)*-1)+\'px\')':prop(s.left))+';'+
            'width:'+(s.width=='auto'?'expression(this.parentNode.offsetWidth+\'px\')':prop(s.width))+';'+
            'height:'+(s.height=='auto'?'expression(this.parentNode.offsetHeight+\'px\')':prop(s.height))+';'+
     '"/>';
  return this.each(function() {undefined
   if ( $('> iframe.bgiframe', this).length == 0 )
    this.insertBefore( document.createElement(html), this.firstChild );
  });
 }
 return this;
};
})(jQuery);