# USTS Beamer Theme

[![Build and check fidelity](https://github.com/greenthree/usts-beamer-theme/actions/workflows/build.yml/badge.svg)](https://github.com/greenthree/usts-beamer-theme/actions/workflows/build.yml)

苏州科技大学非官方 Beamer 模板。v2 从用户提供的 `solution/usts-12-solution.tex` 和 `beamercolorthememycolor.sty` 源码重新提取，以原稿样式的 1:1 复刻为目标。

![模板预览](preview.png)

## 与原稿保持一致

主题直接加载 **Madrid**，再应用原稿的颜色配置和数学字体设置，不重新绘制标题页、标题栏、信息块或页脚。

- 默认 4:3 比例、11pt 字号。
- 学校蓝为 `RGB(0,140,215)`，即 `#008CD7`。
- 保留 Madrid 的圆角阴影封面、通栏标题、球形项目符号和圆角阴影信息块。
- 页脚保留三个等宽栏，顺序为作者与单位、报告简称、日期与页码。颜色由 Madrid 原生混色得到，不用手工 RGB 近似值替代。
- 提醒文字使用原稿的学校蓝。示例块保留 Madrid 默认绿色。
- 保留原稿实际显示的导航图标。原稿的 `\setbeamertemplate{导航符号}{}` 并不关闭 Beamer 的 `navigation symbols`。
- 封面沿用原校徽及 ACM 集训队标识、原缩放比例和图片后的 `25pt` 留白。

通用模板只替换报告内容与元数据：默认作者为「绿化三」，单位为「苏州科技大学物理科学与技术学院」。完整单位写成一行，以适应原稿封面的高度。

## 快速开始

下载仓库，以 [`template.tex`](template.tex) 开始制作报告。[`example.tex`](example.tex) 是完整语法示例，不需要其全部内容时不必复制整份示例。

主题文件、`.tex` 文件和 `assets/` 应位于同一目录。导言区的关键设置如下：

```tex
\documentclass{beamer}
\usetheme{USTS}
\usepackage{ctex}
\usepackage[T1]{fontenc}
\usepackage{graphicx}

\title[报告简称]{苏州科技大学\\报告标题}
\author[绿化三]{绿化三}
\institute[USTS]{苏州科技大学物理科学与技术学院\\\medskip}
\date{\today}
```

中文模板使用 **XeLaTeX**，CI 也使用该引擎。不要使用 pdfLaTeX 编译这两份中文文档。严格复刻以 XeLaTeX 为准，不承诺 LuaLaTeX 与原稿像素一致。

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error template.tex
latexmk -xelatex -interaction=nonstopmode -halt-on-error example.tex
```

也可以在编辑器中选择 XeLaTeX，至少编译两次，使页码与目录收敛。

## 封面

原稿的图片位于 `\titlepage` 之后的独立 `figure` 中。改成 `\titlegraphic` 会改变垂直布局，因此模板保留原写法：

```tex
\begin{frame}
  \titlepage
  \begin{figure}[htbp]
    \begin{center}
      \includegraphics[scale=0.18]{assets/usts-logo.jpg}$\ \ \ $
      \includegraphics[scale=0.32]{assets/acm-logo.png}
    \end{center}
  \end{figure}
  \vspace{25pt}
\end{frame}
```

ACM 标识仅为复刻原稿而保留。制作课程或学术报告时，可以删除第二个 `\includegraphics` 及其前面的数学空格，或替换为学院提供的标识。此时封面会随内容自然重新排版。

## 常用语法

`example.tex` 包含分级列表、普通块、提醒块、示例块、数学公式、三线表、图片、图文双栏、裁剪、定义与定理、证明、覆盖层、Python 代码及超链接。

嵌入图片：

```tex
\begin{figure}
  \centering
  \includegraphics[width=0.7\linewidth]{assets/photo.jpg}
  \caption{图片说明}
\end{figure}
```

只指定宽度或高度时，图片会保持原比例。裁剪顺序为左、下、右、上，默认单位为 bp，裁剪时必须加 `clip`：

```tex
\includegraphics[
  width=\linewidth,
  trim=25 20 25 20,
  clip
]{assets/photo.jpg}
```

含 `lstlisting` 的页面使用 `\begin{frame}[fragile]`。示例图片 `example-image-a`、`example-image-b` 来自 TeX Live 的 `mwe` 宏包，正式报告中应替换为自己的图片。

## 标准 Beamer 自定义

默认配置保持原稿样式。需要变更时，直接使用标准 Beamer 接口：

```tex
% 16:9 会改变原稿比例与封面布局，需重新检查内容是否适合
\documentclass[aspectratio=169]{beamer}

% 在 \usetheme{USTS} 后按需添加
\setbeamertemplate{navigation symbols}{} % 隐藏导航图标
\setbeamertemplate{footline}{}           % 隐藏页脚
\setbeamertemplate{footline}[frame number] % 仅显示页码
```

Madrid 页脚不自动缩小或截断文字。标题、作者或日期较长时，使用短元数据避免三栏溢出：

```tex
\title[项目汇报]{完整的项目研究与成果汇报标题}
\author[绿化三等]{绿化三 \and 李四 \and 王五}
\institute[USTS]{苏州科技大学物理科学与技术学院\\\medskip}
\date[2026-10]{2026 年 10 月}
```

未设置单位或显式写 `\institute[]{完整单位}` 时，Madrid 原生页脚不显示空括号。只写 `\institute{完整单位}` 时，Beamer 会同时将完整单位用于页脚。

主题不自动插入目录或章节过渡页。封面默认参与 frame 计数，覆盖层共用 frame 编号。若要隐藏某页的页眉页脚且不计数，使用 `[plain,noframenumbering]`。

### 字体与复刻范围

保留原稿的 `ctex`、`T1` 西文字体编码及 `onlymath` 衬线数学字体设置，不强制更换字体。中文字体由 `ctex` 按系统选择：本机 Windows 原稿使用微软雅黑，Linux 通常使用 Fandol。跨操作系统、字体版本或 Beamer 版本时，字形、换行和混色实现可能不同。

“像素一致”指在同一编译环境下，对相同内容分别应用原稿配置和 USTS 主题的结果。通用示例的文字不同，自然不会与原题解 PDF 的文字逐像素一致。

## 从 v1 迁移

v2 完整替换了 v1 的自定义布局与调色板。旧的 `footline=full/minimal/none` 选项、`usts-full/minimal/none` 模板和手动扩展的色名不再提供。

- 使用 `\usetheme{USTS}`。
- 页脚改用上面的标准 Beamer 接口。
- 使用 `USTSBlue` 或原稿色名 `mycolor`；派生色写为 `USTSBlue!75!black` 等混色。
- 原 16:9 文档可继续指定比例，但不属于原稿默认 4:3 版式。

## 复刻回归验证

安装 XeLaTeX、latexmk、Python 3 与 Poppler（`pdftoppm`、`pdftotext`），然后运行：

```bash
python tests/check_fidelity.py
```

脚本以独立保留的原始颜色文件和 Madrid 配置为基准，分别编译 4:3、16:9 测试文档，在 **144 dpi** 下对每页做严格像素比较，并检查标题、空单位、页脚及页面边界。两种比例各覆盖 11 页。测试输出位于被忽略的 `build/fidelity/`。

本地仍保留 `solution/` 时，还可以验证原稿所有页面，不改动原稿文件：

```bash
python tests/check_fidelity.py --source ../solution/usts-12-solution.tex
```

此项只替换原稿中的主题加载指令，保留完整正文、图片和元数据，比较原始配置与新主题的编译结果。完整原题解不作为通用模板分发。比较基准由源码完整编译得到，以避免旧 PDF 单轮编译后页码缓存尚未收敛的问题。

CI 编译 `template.tex`、`example.tex`，运行两种比例的复刻测试，并上传 PDF。

## 文件结构

```text
.
├── beamerthemeUSTS.sty       # Madrid + 原稿数学字体设置
├── beamercolorthemeUSTS.sty  # 原稿颜色配置
├── template.tex             # 可直接填写的报告模板
├── example.tex              # 常用语法示例
├── preview.png
├── assets/
│   ├── usts-logo.jpg         # 原 skd.jpg
│   ├── acm-logo.png          # 原 acm.png
│   └── README.md
├── tests/
│   ├── regression.tex
│   ├── check_fidelity.py
│   └── reference/beamercolorthememycolor.sty
└── .github/workflows/build.yml
```

## 许可与声明

主题代码以 [MIT License](LICENSE) 开源。Madrid 及其他 Beamer 组件直接使用 TeX 发行版中的实现，不复制或重许可其源码。

本项目为非官方模板，与苏州科技大学官方无隶属或授权关系。学校名称、校徽、ACM 标识等权利归各自权利人所有，素材不因项目采用 MIT License 而改变其权利归属。使用者应遵守相应视觉标识规范。

---

Unofficial USTS Beamer template extracted directly from the supplied LaTeX source. Uses the original Madrid layout and school blue. Compile with XeLaTeX.
