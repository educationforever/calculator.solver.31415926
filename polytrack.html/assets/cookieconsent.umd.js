(function(global){
  'use strict';
  var STORE_KEY='cc_prefs_v1';
  var opts={};

  function loadPrefs(){
    try{ var s=localStorage.getItem(STORE_KEY); if(s) return JSON.parse(s);}catch(e){}
    return null;
  }
  function savePrefs(categories){
    try{ localStorage.setItem(STORE_KEY, JSON.stringify({ categories: categories })); }catch(e){}
  }

  function el(tag, attrs, children){
    var node=document.createElement(tag);
    if(attrs){Object.keys(attrs).forEach(function(k){
      if(k==='class') node.className=attrs[k];
      else if(k==='text') node.textContent=attrs[k];
      else if(k==='html') node.innerHTML=attrs[k];
      else node.setAttribute(k, attrs[k]);
    });}
    (children||[]).forEach(function(c){ if(typeof c==='string'){ node.appendChild(document.createTextNode(c)); } else if(c) node.appendChild(c); });
    return node;
  }

  function categoriesFromConfig(all){
    return Object.keys(all||{});
  }

  function accept(categories){
    savePrefs(categories);
    cleanupBanner();
    if(typeof opts.onAccept==='function'){
      try{ opts.onAccept({ categories: categories }); }catch(e){}
    }
  }

  var bannerEl, backdropEl;
  function cleanupBanner(){ if(bannerEl && bannerEl.parentNode) bannerEl.parentNode.removeChild(bannerEl); }
  function cleanupModal(){ if(backdropEl && backdropEl.parentNode) backdropEl.parentNode.removeChild(backdropEl); }

  function showBanner(){
    var lang = (opts.language && (opts.language.en || opts.language['zh-CN'])) || {};
    var t = lang.consentModal || { title:'We use cookies', acceptAllBtn:'Accept all', acceptNecessaryBtn:'Reject all' };
    bannerEl = el('div', {class:'cc-banner'}, [
      el('p', {html: '<strong>'+t.title+'</strong> · <a href="#" class="cc-link" id="cc-open-prefs">Cookie settings</a>'}),
      el('div', {class:'cc-actions'}, [
        el('button', {class:'cc-btn secondary', id:'cc-reject', text:t.acceptNecessaryBtn}),
        el('button', {class:'cc-btn', id:'cc-accept', text:t.acceptAllBtn})
      ])
    ]);
    document.body.appendChild(bannerEl);
    bannerEl.querySelector('#cc-open-prefs').addEventListener('click', function(e){ e.preventDefault(); showPreferencesModal(); });
    bannerEl.querySelector('#cc-accept').addEventListener('click', function(){
      var cats = categoriesFromConfig(opts.categories||{});
      accept(cats);
    });
    bannerEl.querySelector('#cc-reject').addEventListener('click', function(){
      var cats = categoriesFromConfig(opts.categories||{}).filter(function(c){ return c==='necessary'; });
      accept(cats);
    });
  }

  function showPreferencesModal(){
    cleanupModal();
    var lang = (opts.language && (opts.language.en || opts.language['zh-CN'])) || {};
    var t = lang.preferencesModal || { title:'Cookie settings', acceptAllBtn:'Accept all', savePreferencesBtn:'Save settings' };
    var current = loadPrefs();
    var analyticsOn = current ? current.categories.indexOf('analytics')>-1 : false;

    backdropEl = el('div', {class:'cc-modal-backdrop'}, [
      el('div', {class:'cc-modal'}, [
        el('h2', {text: t.title}),
        el('div', {class:'cc-row'}, [ el('span',{text:'Necessary'}), el('span',{text:'Always on'}) ]),
        el('div', {class:'cc-row'}, [
          el('label', {for:'cc-analytics', text:'Analytics'}),
          (function(){ var sw=el('div',{class:'cc-switch', id:'cc-analytics'}); sw.setAttribute('data-on', analyticsOn?'true':'false'); sw.addEventListener('click', function(){ sw.setAttribute('data-on', sw.getAttribute('data-on')==='true'?'false':'true'); }); return sw; })()
        ]),
        el('div', {class:'cc-actions'}, [
          el('button', {class:'cc-btn secondary', id:'cc-accept-all', text: t.acceptAllBtn}),
          el('button', {class:'cc-btn', id:'cc-save', text: t.savePreferencesBtn})
        ])
      ])
    ]);
    document.body.appendChild(backdropEl);
    backdropEl.addEventListener('click', function(e){ if(e.target===backdropEl){ cleanupModal(); }});
    document.getElementById('cc-accept-all').onclick=function(){ accept(categoriesFromConfig(opts.categories||{})); cleanupModal(); };
    document.getElementById('cc-save').onclick=function(){
      var cats=['necessary'];
      var sw=document.getElementById('cc-analytics');
      if(sw && sw.getAttribute('data-on')==='true') cats.push('analytics');
      accept(cats); cleanupModal();
    };
  }

  var API = {
    run: function(options){ opts = options || {}; var prefs = loadPrefs(); if(!prefs){ if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded', showBanner);} else { showBanner(); } } else { if(typeof opts.onAccept==='function'){ try{ opts.onAccept({ categories: prefs.categories }); }catch(e){} } }
    },
    showPreferences: function(){ showPreferencesModal(); }
  };

  global.CookieConsent = API;
})(window);

