# 未名集 · 个人文学作品站

网址：<https://kxxx55500.github.io/>　后台：<https://kxxx55500.github.io/admin/>

基于 GitHub Pages + Jekyll 的纯静态站点；后台为 [Sveltia CMS](https://sveltiacms.app/)，在网页里写作，保存即提交到本仓库，约 1 分钟后网站自动更新。

## 后台登录（首次）

1. 打开 `/admin/`，点「使用访问令牌登录」。
2. 对话框里有生成令牌的链接（已预选好权限）；或自行到 GitHub → Settings → Developer settings → Fine-grained tokens 新建，只授权本仓库，权限 **Contents: Read and write**。
3. 粘贴令牌即可。令牌只保存在当前浏览器里；换设备需重新登录。

## 发布作品

- **短篇**：「作品」→ 新建，类型选「短篇」，正文写在「正文」里。
- **长篇**：先在「作品」里新建一个长篇（写简介即可），再到「章节」里逐章添加，选所属作品、填章节序号。
- 「网址名」用拼音或英文（如 `yu-ye`），保存后不可更改。
- 关闭「公开」即为草稿，网站上不显示。

写作小贴士：

- 段落之间回车即可；段首不必空两格，样式会自动缩进（手打的全角空格也会被去掉）。
- 场景切换写一行 `***`，会显示为「＊　＊　＊」。
- 段首不要用 4 个以上的半角空格，否则会被当成代码块。

## 修改站点信息

站名、副标题、署名、简介都在 `_config.yml` 顶部；「关于」页可在后台「页面」里改。

## 让 Google 收录

1. 打开 [Google Search Console](https://search.google.com/search-console)，添加「网址前缀」资源 `https://kxxx55500.github.io/`。
2. 验证方式选「HTML 标记」，把 `content="..."` 里的那串码填进 `_config.yml` 的 `webmaster_verifications.google`，提交后点验证。
3. 在「站点地图」里提交 `sitemap.xml`。之后新作品会自动出现在站点地图里。

## 本地预览（可选）

```bash
bundle install
bundle exec jekyll serve
```
