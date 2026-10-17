# 开发日志

## 2026-10-17　建站

- 方案：GitHub Pages 原生 Jekyll 构建（插件仅用白名单内的 jekyll-seo-tag、jekyll-sitemap），无需 Actions。
- 后台：Sveltia CMS（版本锁定 0.224.0），GitHub 后端，仅令牌登录（`auth_methods: [token]`），因此不需要 OAuth 服务器。
- 内容模型：`_works/<网址名>.md`（kind: short/long）；长篇章节 `_chapters/<作品>/<序号>.md`，网址 `/works/<作品>/<序号>/`。CMS 用 `path: "{{work}}/{{slug}}"` 生成章节路径。
- 正文：kramdown GFM + `hard_wrap`，再在 `_includes/prose.html` 里把 `<br />` 拆成段落、去掉段首全角空格 —— 兼容「单换行分段」和「空行分段」两种粘贴习惯。已验证。
- 字体：`Songti SC` → 本地思源宋体（Noto Serif CJK SC / Source Han Serif SC）→ Google Fonts 的 Noto Serif SC → 系统宋体。字体 CSS 以 `media="print" onload` 非阻塞加载，网络不通时不阻塞渲染。已验证：本地有 CJK 宋体时不会下载网络字体。
- 验证：本地 github-pages gem 构建通过；sitemap 不含 /admin、404；robots 屏蔽 /admin；手机 / 桌面、浅色 / 深色截图检查通过；后台页加载无配置错误。
- 修正：页眉字号小于正文导致 `em` 栏宽变窄、与正文不对齐 → 栏宽改为 `calc(var(--fs) * 34)`。
- 未在本地验证：后台实际读写仓库（需线上令牌）。

## 2026-10-17　上线

- 通过 gh 设备码登录完成部署。
- 提交统一使用 GitHub noreply 邮箱。
- 创建公开仓库 kxxx55500.github.io 并推送；Pages 自动开启（main / 根目录，HTTPS）。首次构建约 40 秒。
- 线上验证：所有页面 200，正文分段与本地一致，手机宽度无横向滚动。

## 2026-10-17　第一次改版（按用户反馈）

- 删除示例长篇「长河」及两章（「雨夜」用户已在后台删除）；站名改为「疗愈系奇幻写作」；「关于」只留一句。
- 配色：背景 #f7f5f0 → #fcfbf9（更白）；点缀色印章红 → 橄榄绿 #5f6b47，呼应插画。
- 尺寸：正文 19px → 18px（电脑）/ 17px（手机），每行 34 → 32 字；标题、留白整体收紧。
- 插画：首页「扉页」——电脑左图右文（4:6，图片 sticky），手机横幅 4:3 置顶（object-position 50% 5% 保留帽顶）。原图 2.2MB 存于 figures/（不发布），网页用 640/1000w WebP（140/250KB）；另裁 1200×630 og.jpg 作分享预览图。
- 发现并修复：后台富文本编辑器把 `***` 存成 `\* \* \*` → 显示成普通星号。prose.html 中将 `<p>* * *</p>` 也转为分隔线；编辑器开启 hr 按钮。
- 发现并修复：后台把留空的选填项存为 `''`，Liquid 中空字符串为真 → 首页出现空简介、SEO 描述退回全站简介。模板改为 strip 后判空；CMS 开启 `omit_empty_optional_fields`；手动去掉用户作品里两个空字段（不改正文）。
- 观察（未改）：两端对齐 + 避头尾规则在手机窄屏偶有字距被拉开的行（如引号开头的对话行），属中文排版常见现象；Safari 支持 hanging-punctuation 会好一些。
