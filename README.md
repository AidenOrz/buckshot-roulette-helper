# 🎲 Buckshot Roulette 桌面助手

单文件、零依赖的《恶魔轮盘 / Buckshot Roulette》手机向辅助网页。纯 vanilla JS，浏览器直接打开即玩，数据保存在本机 localStorage，不上传任何服务器。

## 三个工具

| 文件 | 说明 |
|---|---|
| `versus.html` | **对战版** — 双人共屏对局：随机 2/4/8 发装填（差 ≤2、至少各 1）、血条、道具、三局两胜 |
| `versus-ai.html` | **AI 版** — 单人三回合战役，需连赢 3 回合击败 AI，三档难度可选 |
| `tracker.html` | **记录版** — 手动录入弹数与开枪结果，辅助线下真实对局记账 |

## 道具（对战版 / AI 版）

🚬 香烟 +1♥ ｜ 💊 过期止痛药 50%+2♥ / 50%−1♥（可致死） ｜ ⛓ 手铐 跳过对方下次行动 ｜ 📱 手机 查随机一发（非下一发） ｜ 🔍 放大镜 查下一发 ｜ 🔄 逆转器 反转下一发 ｜ 🍺 啤酒 退掉下一发 ｜ 💉 兴奋剂 偷对方一个道具（自选并立即使用） ｜ 🔫 双发扳机 下一次开枪伤害 ×2

道具可在右上角 ⚙️ 设置中逐个启用/关闭。回合开局与弹仓打空重装时，双方各得 2 个道具。

## AI 版 · 地狱档特色

- 从**公开行为**推断你窥视了哪一发（放大镜/手机的使用是明牌）
- 用手铐反制你的双发扳机斩杀
- 用啤酒烧掉你已窥视的子弹，残血时退弹逃生
- 每次上弹后由玩家先手

AI 只读取「公开信息 + 自己的情报快照」，绝不偷看弹仓顺序；放大镜/手机结果双方互相保密。

## 运行

无需构建：浏览器直接打开对应 html 即可（手机 / 桌面均可，响应式布局，支持触控）。

## 回归测试（可选）

```bash
# 生成并运行无头测试（需要 node 与 python3）
python tests/mktest.py
node tests/test_vs.js
node tests/test_ai.js

# 语法检查（需要 pip install esprima）
python tests/checkjs.py
```

测试会从 html 中提取 `<script>`，stub 掉浏览器环境后真实执行游戏逻辑，断言装填规则、道具消耗、撤销还原、双发扳机、兴奋剂即用等 13 项行为。

## 许可

- 代码：[MIT](LICENSE)
- 图标：来自 [game-icons.net](https://game-icons.net/)（Lorc / Delapouite），遵循 [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)
