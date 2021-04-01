// Easy Responsive Tabs Plugin
// Author: Samson.Onna <Email : samson3d@gmail.com> 
(function (Rs ) {
    Rs .fn.extend({
        easyResponsiveTabs: function (options) {
            //Set the default values, use comma to separate the settings, example:
            var defaults = {
                type: 'default', //default, vertical, accordion;
                width: 'auto',
                fit: true,
                closed: false,
                tabidentify: '',
                activetab_bg: 'white',
                inactive_bg: '#F5F5F5',
                active_border_color: '#c1c1c1',
                active_content_border_color: '#c1c1c1',
                activate: function () {
                }
            }
            //Variables
            var options = Rs .extend(defaults, options);
            var opt = options, jtype = opt.type, jfit = opt.fit, jwidth = opt.width, vtabs = 'vertical', accord = 'accordion';
            var hash = window.location.hash;
            var historyApi = !!(window.history && history.replaceState);

            //Events
            Rs (this).bind('tabactivate', function (e, currentTab) {
                if (typeof options.activate === 'function') {
                    options.activate.call(currentTab, e)
                }
            });

            //Main function
            this.each(function () {
                var Rs respTabs = Rs (this);
                var Rs respTabsList = Rs respTabs.find('ul.resp-tabs-list.' + options.tabidentify);
                var respTabsId = Rs respTabs.attr('id');
                Rs respTabs.find('ul.resp-tabs-list.' + options.tabidentify + ' li').addClass('resp-tab-item').addClass(options.tabidentify);
                Rs respTabs.css({
                    'display': 'block',
                    'width': jwidth
                });

                if (options.type == 'vertical')
                    Rs respTabsList.css('margin-top', '3px');

                Rs respTabs.find('.resp-tabs-container.' + options.tabidentify).css('border-color', options.active_content_border_color);
                Rs respTabs.find('.resp-tabs-container.' + options.tabidentify + ' > div').addClass('resp-tab-content').addClass(options.tabidentify);
                jtab_options();
                //Properties Function
                function jtab_options() {
                    if (jtype == vtabs) {
                        Rs respTabs.addClass('resp-vtabs').addClass(options.tabidentify);
                    }
                    if (jfit == true) {
                        Rs respTabs.css({ width: '100%', margin: '0px' });
                    }
                    if (jtype == accord) {
                        Rs respTabs.addClass('resp-easy-accordion').addClass(options.tabidentify);
                        Rs respTabs.find('.resp-tabs-list').css('display', 'none');
                    }
                }

                //Assigning the h2 markup to accordion title
                var Rs tabItemh2;
                Rs respTabs.find('.resp-tab-content.' + options.tabidentify).before("<h2 class='resp-accordion " + options.tabidentify + "' role='tab'><span class='resp-arrow'></span></h2>");

                Rs respTabs.find('.resp-tab-content.' + options.tabidentify).prev("h2").css({
                    'background-color': options.inactive_bg,
                    'border-color': options.active_border_color
                });

                var itemCount = 0;
                Rs respTabs.find('.resp-accordion').each(function () {
                    Rs tabItemh2 = Rs (this);
                    var Rs tabItem = Rs respTabs.find('.resp-tab-item:eq(' + itemCount + ')');
                    var Rs accItem = Rs respTabs.find('.resp-accordion:eq(' + itemCount + ')');
                    Rs accItem.append(Rs tabItem.html());
                    Rs accItem.data(Rs tabItem.data());
                    Rs tabItemh2.attr('aria-controls', options.tabidentify + '_tab_item-' + (itemCount));
                    itemCount++;
                });

                //Assigning the 'aria-controls' to Tab items
                var count = 0,
                    Rs tabContent;
                Rs respTabs.find('.resp-tab-item').each(function () {
                    Rs tabItem = Rs (this);
                    Rs tabItem.attr('aria-controls', options.tabidentify + '_tab_item-' + (count));
                    Rs tabItem.attr('role', 'tab');
                    Rs tabItem.css({
                        'background-color': options.inactive_bg,
                        'border-color': 'none'
                    });

                    //Assigning the 'aria-labelledby' attr to tab-content
                    var tabcount = 0;
                    Rs respTabs.find('.resp-tab-content.' + options.tabidentify).each(function () {
                        Rs tabContent = Rs (this);
                        Rs tabContent.attr('aria-labelledby', options.tabidentify + '_tab_item-' + (tabcount)).css({
                            'border-color': options.active_border_color
                        });
                        tabcount++;
                    });
                    count++;
                });

                // Show correct content area
                var tabNum = 0;
                if (hash != '') {
                    var matches = hash.match(new RegExp(respTabsId + "([0-9]+)"));
                    if (matches !== null && matches.length === 2) {
                        tabNum = parseInt(matches[1], 10) - 1;
                        if (tabNum > count) {
                            tabNum = 0;
                        }
                    }
                }

                //Active correct tab
                Rs (Rs respTabs.find('.resp-tab-item.' + options.tabidentify)[tabNum]).addClass('resp-tab-active').css({
                    'background-color': options.activetab_bg,
                    'border-color': options.active_border_color
                });

                //keep closed if option = 'closed' or option is 'accordion' and the element is in accordion mode
                if (options.closed !== true && !(options.closed === 'accordion' && !Rs respTabsList.is(':visible')) && !(options.closed === 'tabs' && Rs respTabsList.is(':visible'))) {
                    Rs (Rs respTabs.find('.resp-accordion.' + options.tabidentify)[tabNum]).addClass('resp-tab-active').css({
                        'background-color': options.activetab_bg + ' !important',
                        'border-color': options.active_border_color,
                        'background': 'none'
                    });

                    Rs (Rs respTabs.find('.resp-tab-content.' + options.tabidentify)[tabNum]).addClass('resp-tab-content-active').addClass(options.tabidentify).attr('style', 'display:block');
                }
                //assign proper classes for when tabs mode is activated before making a selection in accordion mode
                else {
                   // Rs (Rs respTabs.find('.resp-tab-content.' + options.tabidentify)[tabNum]).addClass('resp-accordion-closed'); //removed resp-tab-content-active
                }

                //Tab Click action function
                Rs respTabs.find("[role=tab]").each(function () {

                    var Rs currentTab = Rs (this);
                    Rs currentTab.click(function () {

                        var Rs currentTab = Rs (this);
                        var Rs tabAria = Rs currentTab.attr('aria-controls');

                        if (Rs currentTab.hasClass('resp-accordion') && Rs currentTab.hasClass('resp-tab-active')) {
                            Rs respTabs.find('.resp-tab-content-active.' + options.tabidentify).slideUp('', function () {
                                Rs (this).addClass('resp-accordion-closed');
                            });
                            Rs currentTab.removeClass('resp-tab-active').css({
                                'background-color': options.inactive_bg,
                                'border-color': 'none'
                            });
                            return false;
                        }
                        if (!Rs currentTab.hasClass('resp-tab-active') && Rs currentTab.hasClass('resp-accordion')) {
                            Rs respTabs.find('.resp-tab-active.' + options.tabidentify).removeClass('resp-tab-active').css({
                                'background-color': options.inactive_bg,
                                'border-color': 'none'
                            });
                            Rs respTabs.find('.resp-tab-content-active.' + options.tabidentify).slideUp().removeClass('resp-tab-content-active resp-accordion-closed');
                            Rs respTabs.find("[aria-controls=" + Rs tabAria + "]").addClass('resp-tab-active').css({
                                'background-color': options.activetab_bg,
                                'border-color': options.active_border_color
                            });

                            Rs respTabs.find('.resp-tab-content[aria-labelledby = ' + Rs tabAria + '].' + options.tabidentify).slideDown().addClass('resp-tab-content-active');
                        } else {
                            console.log('here');
                            Rs respTabs.find('.resp-tab-active.' + options.tabidentify).removeClass('resp-tab-active').css({
                                'background-color': options.inactive_bg,
                                'border-color': 'none'
                            });

                            Rs respTabs.find('.resp-tab-content-active.' + options.tabidentify).removeAttr('style').removeClass('resp-tab-content-active').removeClass('resp-accordion-closed');

                            Rs respTabs.find("[aria-controls=" + Rs tabAria + "]").addClass('resp-tab-active').css({
                                'background-color': options.activetab_bg,
                                'border-color': options.active_border_color
                            });

                            Rs respTabs.find('.resp-tab-content[aria-labelledby = ' + Rs tabAria + '].' + options.tabidentify).addClass('resp-tab-content-active').attr('style', 'display:block');
                        }
                        //Trigger tab activation event
                        Rs currentTab.trigger('tabactivate', Rs currentTab);

                        //Update Browser History
                        if (historyApi) {
                            var currentHash = window.location.hash;
                            var tabAriaParts = Rs tabAria.split('tab_item-');
                            // var newHash = respTabsId + (parseInt(Rs tabAria.substring(9), 10) + 1).toString();
                            var newHash = respTabsId + (parseInt(tabAriaParts[1], 10) + 1).toString();
                            if (currentHash != "") {
                                var re = new RegExp(respTabsId + "[0-9]+");
                                if (currentHash.match(re) != null) {
                                    newHash = currentHash.replace(re, newHash);
                                }
                                else {
                                    newHash = currentHash + "|" + newHash;
                                }
                            }
                            else {
                                newHash = '#' + newHash;
                            }

                            history.replaceState(null, null, newHash);
                        }
                    });

                });

                //Window resize function                   
                Rs (window).resize(function () {
                    Rs respTabs.find('.resp-accordion-closed').removeAttr('style');
                });
            });
        }
    });
})(jQuery);

