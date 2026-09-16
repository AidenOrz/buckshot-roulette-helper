# -*- coding: utf-8 -*-
"""生成无头 node 测试：从仓库根目录的 HTML 中提取 <script>，加上浏览器 stub 后真实执行。

用法：
    python tests/mktest.py        # 生成 tests/test_vs.js 与 tests/test_ai.js
    node tests/test_vs.js
    node tests/test_ai.js
结果写入 tests/test_result_*.txt，断言全部通过时输出 RESULT: ALL PASS。
"""
import io, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 仓库根目录

STUB = r'''
function fakeEl(){return {innerHTML:'',textContent:'',value:'',title:'',children:[],style:{},
  classList:{add:function(){},remove:function(){},contains:function(){return true}},
  scrollIntoView:function(){},querySelector:function(){return null}};}
var __store={};
global.localStorage={getItem:function(k){return Object.prototype.hasOwnProperty.call(__store,k)?__store[k]:null},
  setItem:function(k,v){__store[k]=String(v)},removeItem:function(k){delete __store[k]}};
global.crypto={getRandomValues:function(a){for(var i=0;i<a.length;i++)a[i]=Math.floor(Math.random()*4294967296);return a}};
global.navigator={};
global.window={};
global.document={addEventListener:function(){},querySelector:function(){return fakeEl()},querySelectorAll:function(){return[]},
  body:{classList:{add:function(){},remove:function(){},contains:function(){return false}}},createElement:function(){return fakeEl()}};
'''

TEST_TAIL = r'''
;(function(){
  var out=[];
  var r=curRound();
  out.push('[1] round-start deal: player='+JSON.stringify(r.items.player)+' opponent='+JSON.stringify(r.items.opponent));
  r.items.player=['cigarette','beer','cigarette'];
  out.push('[2] hand set to '+JSON.stringify(r.items.player));
  useItem('player','cigarette',0,false);
  var ok1=JSON.stringify(r.items.player)===JSON.stringify(['beer','cigarette']);
  out.push('[3] after cigarette -> '+JSON.stringify(r.items.player)+' ok='+ok1);
  var bi=r.items.player.indexOf('beer');
  useItem('player','beer',bi,false);
  var ok2=JSON.stringify(r.items.player)===JSON.stringify(['cigarette']);
  out.push('[4] after beer -> '+JSON.stringify(r.items.player)+' chamberRem='+r.order.length+' ok='+ok2);
  var o0=r.items.opponent[0];
  var before=r.items.opponent.length;
  useItem('opponent',o0,0,true);
  var ok3=r.items.opponent.length===before-1;
  out.push('[5] opponent used '+o0+' silently -> '+JSON.stringify(r.items.opponent)+' ok='+ok3);
  out.push('[6] cigarette removed: '+ok1);
  out.push('[7] beer removed: '+ok2);
  out.push('[8] opponent item removed: '+ok3);
  var r2=curRound();
  r2.items.player=['dtrg','adr'];
  r2.items.opponent=['mag','beer'];
  r2.dbl.player=0;r2.hpMax=4;r2.hpO=4;
  useItem('player','dtrg',0,false);
  var ok4=(r2.dbl.player===1)&&JSON.stringify(r2.items.player)===JSON.stringify(['adr']);
  out.push('[9] dtrg buff set & consumed: '+ok4+' dbl='+r2.dbl.player+' hand='+JSON.stringify(r2.items.player));
  var hpB=r2.hpO;
  r2.order=['live','blank','blank'];r2.L=1;
  fire('other');
  var ok5=(r2.hpO===hpB-2)&&(r2.dbl.player===0);
  out.push('[10] double-damage shot: hpO '+hpB+'->'+r2.hpO+' ok='+ok5);
  undo();
  var ok6=(r2.hpO===hpB)&&(r2.dbl.player===1);
  out.push('[11] undo restores hp & buff: '+ok6);
  r2.items.player=['adr'];
  r2.items.opponent=['mag','beer'];
  r2.order=['live','blank','blank'];r2.L=1;
  useItem('player','adr',0,false,'beer');
  var ok7=(r2.items.opponent.length===1)&&(r2.items.opponent[0]==='mag')&&(r2.items.player.length===0)&&(!!r2.lastEject)&&(r2.lastEject.result==='live');
  out.push('[12] adr steals & force-uses: player='+JSON.stringify(r2.items.player)+' opponent='+JSON.stringify(r2.items.opponent)+' ejected='+(r2.lastEject&&r2.lastEject.result)+' ok='+ok7);
  r2.items.player=['adr'];
  r2.items.opponent=['dtrg'];
  r2.dbl.player=0;
  useItem('player','adr',0,false,'dtrg');
  var ok8=(r2.dbl.player===1)&&(r2.items.opponent.length===0)&&(r2.items.player.length===0);
  out.push('[13] stolen dtrg force-armed: dbl='+r2.dbl.player+' ok='+ok8);
  out.push((ok1&&ok2&&ok3&&ok4&&ok5&&ok6&&ok7&&ok8)?'RESULT: ALL PASS':'RESULT: FAIL');
  require('fs').writeFileSync(require('path').join(__dirname,'test_result___TAG__.txt'),out.join('\n'));
})();
'''

for name, tag in (("versus.html", "vs"), ("versus-ai.html", "ai")):
    with io.open(os.path.join(BASE, name), encoding="utf-8") as f:
        s = f.read()
    code = re.findall(r"<script>([\s\S]*?)</script>", s)[0]
    js = STUB + "\n" + code + "\n" + TEST_TAIL.replace("__TAG__", tag)
    p = os.path.join(BASE, "tests", "test_%s.js" % tag)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(js)
    print("wrote", p, len(js))
