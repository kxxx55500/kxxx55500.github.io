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
