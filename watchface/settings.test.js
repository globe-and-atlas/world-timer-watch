var assert=require('assert'),Module=require('module'),path=require('path'),original=Module._load,config;
var keys={};require('./package.json').pebble.messageKeys.forEach(function(k,i){keys[k]=10000+i;});
var bundle=path.join(__dirname,'node_modules/@rebble/clay/src/js/index.js');
Module._load=function(name){if(name==='message_keys')return keys;if(name==='@rebble/clay'){var Actual=original.call(this,bundle);return function(items,custom,options){config=items;return new Actual(items,custom,options);};}return original.apply(this,arguments);};
var events={},storage={},sent=[];
global.localStorage={getItem:function(k){return storage[k]||null;},setItem:function(k,v){storage[k]=v;}};
global.Pebble={addEventListener:function(k,fn){(events[k]||(events[k]=[])).push(fn);},getAccountToken:function(){return 'test';},getWatchToken:function(){return 'test';},getActiveWatchInfo:function(){return {platform:'emery',model:'emery',language:'en_US',firmware:{major:4,minor:33,patch:1}};},sendAppMessage:function(v){sent.push(v);},openURL:function(url){assert(url.indexOf('data:text/html')===0);}};
var settings=require('./src/pkjs/index');function fire(k,v){(events[k]||[]).forEach(function(fn){fn(v);});}
assert.deepStrictEqual(settings.normalize({}),settings.defaults);assert.strictEqual(settings.defaults.Theme,0);
Object.keys(settings.defaults).forEach(function(k){var raw={};[null,'',-1,Infinity,3.2,{},undefined].forEach(function(v){raw[k]=v;assert.strictEqual(settings.normalize(raw)[k],settings.defaults[k]);});});
for(var i=0;i<40;i++)assert.strictEqual(settings.normalize({MainCity:String(i)}).MainCity,i);
assert.strictEqual(settings.normalize({OtherCity:40}).OtherCity,1);assert.strictEqual(settings.normalize({MainStart:24}).MainStart,undefined);
assert.strictEqual(settings.normalize({FlapOn:false}).FlapOn,0);assert.strictEqual(settings.normalize({ShowSeconds:true}).ShowSeconds,1);assert.strictEqual(settings.normalize({Palette:6,Background:85}).Theme,2);
fire('ready');assert.strictEqual(sent.length,0);fire('showConfiguration');['','CANCELLED','invalid'].forEach(function(v){fire('webviewclosed',{response:v});});assert.strictEqual(sent.length,0);
var raw={},expected={};Object.keys(settings.defaults).forEach(function(k){raw[k]={value:settings.defaults[k]};expected[k]=settings.defaults[k];});
raw.Theme.value='1';expected.Theme=1;raw.MainCity.value='2';expected.MainCity=2;raw.OtherCity.value='34';expected.OtherCity=34;raw.FlapOn.value=false;expected.FlapOn=0;
fire('webviewclosed',{response:encodeURIComponent(JSON.stringify(raw))});assert.deepStrictEqual(sent[0],expected);fire('ready');assert.deepStrictEqual(sent[1],expected);
assert.strictEqual(config.filter(function(c){return c.messageKey==='Theme';})[0].options.length,3);assert.strictEqual(config.filter(function(c){return c.messageKey==='OtherCity';})[0].options.length,40);
assert.deepStrictEqual(require('./package.json').pebble.messageKeys.slice(0,8),['Palette','Background','Foreground','Accent','TimeFormat','DateFormat','ShowSeconds','ZoneOffset']);
console.log('PASS: actual Clay Save/Cancel/reload, city bounds, themes, old custom migration and stable keys');

storage['clay-settings']=JSON.stringify({Palette:6,Background:85,Foreground:0xFFFFFF,Accent:0xFF5500,DateFormat:2});
fire('ready');assert.strictEqual(sent[sent.length-1].Theme,2);assert.strictEqual(JSON.parse(storage['clay-settings']).Theme,2);
fire('showConfiguration');assert.strictEqual(JSON.parse(storage['clay-settings']).Theme,2);assert.strictEqual(JSON.parse(storage['clay-settings']).Background,85);
console.log('PASS: legacy custom theme is migrated into Clay storage before editor opens');

['MainStart','MainEnd','OtherStart','OtherEnd','TravelOn'].forEach(function(key){assert.strictEqual(settings.defaults[key],undefined);assert.strictEqual(config.some(function(c){return c.messageKey===key;}),false);});assert.strictEqual(JSON.stringify(config).indexOf('Call windows'),-1);console.log('PASS: removed call-hours/map controls cannot reappear from saved settings');

storage['clay-settings']=JSON.stringify({Theme:1,MainCity:2,OtherCity:24,MainStart:22,MainEnd:7,OtherStart:0,OtherEnd:24,TravelOn:0});fire('ready');var migrated=JSON.parse(storage['clay-settings']);assert.strictEqual(migrated.MainCity,2);assert.strictEqual(migrated.OtherCity,24);assert.strictEqual(migrated.Theme,1);assert.strictEqual(migrated.FlapOn,1);assert.strictEqual(migrated.MainStart,undefined);assert.strictEqual(migrated.TravelOn,undefined);console.log('PASS: published city/theme settings survive migration while retired controls are removed');
