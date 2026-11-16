var Clay=require('@rebble/clay');
var cities=require('./cities.json');
var defaults={Theme:0,Background:0,Foreground:0xFFAA00,Accent:0x555555,TimeFormat:0,DateFormat:1,ShowSeconds:0,MainCity:0,OtherCity:1,FlapOn:1};
var limits={Theme:2,TimeFormat:2,DateFormat:4,ShowSeconds:1,MainCity:cities.length-1,OtherCity:cities.length-1,FlapOn:1};
function integer(value,fallback,max){if(value===undefined||value===null||value===''||typeof value==='boolean'||typeof value==='object')return fallback;var n=Number(value);return isFinite(n)&&Math.floor(n)===n&&n>=0&&n<=max?n:fallback;}
function normalize(raw){raw=raw||{};var out={};Object.keys(defaults).forEach(function(key){var value=raw[key];if((key==='ShowSeconds'||key==='FlapOn')&&typeof value==='boolean')value=value?1:0;out[key]=integer(value,defaults[key],limits[key]===undefined?0xFFFFFF:limits[key]);});if(raw.Theme===undefined&&Number(raw.Palette)===6)out.Theme=2;return out;}
function select(key,label,value,options){return {type:'select',messageKey:key,label:label,defaultValue:String(value),options:options};}
var config=[
 {type:'heading',defaultValue:'World Timer — departure board'},
 {type:'text',defaultValue:'Both clocks follow the cities you choose, independently of the watch’s local time zone. Offline IANA2026f rules cover2020–2037. Future government rule changes need an app update.'},
 select('MainCity','Main city',0,cities.map(function(c){return {label:c.name+' · '+c.zone,value:String(c.id)};})),
 select('OtherCity','Other city',1,cities.map(function(c){return {label:c.name+' · '+c.zone,value:String(c.id)};})),
 {type:'toggle',messageKey:'FlapOn',label:'Split-flap minute transitions',defaultValue:true},
 {type:'text',defaultValue:'The signed difference is the Other city relative to Main, including DST. A separate day marker shows a calendar-day change.'},
 select('Theme','Theme',0,[{label:'Amber on black',value:'0'},{label:'Olive LCD',value:'1'},{label:'Custom colors',value:'2'}]),
 {type:'color',messageKey:'Background',label:'Custom background',defaultValue:'000000',sunlight:false,allowGray:true},
 {type:'color',messageKey:'Foreground',label:'Custom ink',defaultValue:'FFAA00',sunlight:false,allowGray:true},
 {type:'color',messageKey:'Accent',label:'Custom flap borders',defaultValue:'FFAA00',sunlight:false,allowGray:true},
 select('TimeFormat','Time format',0,[{label:'Watch default',value:'0'},{label:'12-hour',value:'1'},{label:'24-hour',value:'2'}]),
 select('DateFormat','Dates',1,[{label:'Off',value:'0'},{label:'SAT 07 NOV',value:'1'},{label:'YYYY-MM-DD',value:'2'},{label:'MM/DD/YYYY',value:'3'},{label:'DD/MM/YYYY',value:'4'}]),
 {type:'toggle',messageKey:'ShowSeconds',label:'Show seconds',defaultValue:false},
 {type:'submit',defaultValue:'Save to watch'}];
var clay=new Clay(config,null,{autoHandleEvents:false});
function migrateSaved(){var raw=localStorage.getItem('clay-settings');if(!raw)return null;var saved=normalize(JSON.parse(raw));localStorage.setItem('clay-settings',JSON.stringify(saved));return saved;}
function sendSaved(){try{var saved=migrateSaved();if(saved)Pebble.sendAppMessage(saved);}catch(e){console.log('Settings could not be loaded');}}
Pebble.addEventListener('ready',sendSaved);
Pebble.addEventListener('showConfiguration',function(){try{migrateSaved();}catch(e){console.log('Settings could not be migrated');}Pebble.openURL(clay.generateUrl());});
Pebble.addEventListener('webviewclosed',function(event){if(!event||!event.response||event.response==='CANCELLED')return;try{clay.getSettings(event.response,false);sendSaved();}catch(e){console.log('Settings were not saved');}});
module.exports={normalize:normalize,defaults:defaults,config:config};
